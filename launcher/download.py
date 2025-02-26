import os.path
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from launcher import config, errors, helpers


def download_version_manifest(version: str = None, minecraft_dir=f'{os.getcwd()}/.minecraft') -> [dict, str]:
    _version = version
    if version is None:
        _version = "latest"

    versions_req = requests.get(config.VERSION_MANIFEST_URL)
    if versions_req.status_code != 200:
        raise ConnectionError('Failed to check version manifest')

    manifest_versions = versions_req.json()
    if _version == 'latest':
        _version = manifest_versions['latest']['release']

    for version in manifest_versions['versions']:
        if version['id'] == _version:
            helpers.download_file(version['url'], os.path.join(minecraft_dir, 'versions', _version))
            manifest_req = requests.get(version['url'])
            if manifest_req.status_code != 200:
                raise ConnectionError('Failed to get version manifest')
            version = manifest_req.json()
            return version, _version

    raise errors.VersionNotFoundError('Version not found')


def download_minecraft_jar(version: dict, version_id: str, minecraft_dir=f'{os.getcwd()}/.minecraft') -> None:
    jar_path = version['downloads']['client']['url']
    helpers.download_file(jar_path, os.path.join(minecraft_dir, 'versions', version_id), version_id+".jar")


def download_libraries_and_make_native_files(version: dict, minecraft_dir=f'{os.getcwd()}/.minecraft') -> None:
    libraries_dir = os.path.join(minecraft_dir, 'libraries')
    natives_dir = os.path.join(minecraft_dir, 'natives')
    libraries = version['libraries']
    for library in libraries:
        if not helpers.should_use_library(library):
            continue
        library_download = library['downloads']['artifact']
        helpers.download_file(library_download['url'], os.path.join(libraries_dir, '/'.join(library_download['path'].split('/')[:-1])))

        if helpers.is_native_library(library):
            with zipfile.ZipFile(os.path.join(libraries_dir, library_download['path']), 'r') as zip_ref:
                zip_ref.extractall(natives_dir)


def download_assets(version: dict, minecraft_dir=f'{os.getcwd()}/.minecraft') -> None:
    assets_dir = os.path.join(minecraft_dir, 'assets')
    assets_index_url = version['assetIndex']['url']

    # Получаем индекс ресурсов
    assets_index_req = requests.get(assets_index_url)
    if assets_index_req.status_code != 200:
        raise ConnectionError('Failed to get assets index')

    # Сохраняем индекс ресурсов
    helpers.download_file(assets_index_url, os.path.join(assets_dir, 'indexes'))
    assets_index = assets_index_req.json()
    assets_objects: dict = assets_index['objects']

    # Создаем директорию для объектов, если она не существует
    objects_dir = os.path.join(assets_dir, 'objects')

    # Используем ThreadPoolExecutor для параллельного скачивания
    with ThreadPoolExecutor(max_workers=10) as executor:  # Вы можете настроить max_workers
        futures = []
        for asset in assets_objects.values():
            asset_hash = asset['hash']
            first_chars = asset_hash[:2]
            local_path = os.path.join(objects_dir, first_chars)
            url = f'{config.RESOURCES_URL}{first_chars}/{asset_hash}'
            futures.append(executor.submit(helpers.download_file, url, local_path))

        # Обрабатываем завершенные задачи
        for future in as_completed(futures):
            try:
                result = future.result()  # Получаем результат, если нужно
                print(f"Downloaded: {result}")
            except Exception as e:
                print(f"Error downloading file: {e}")


def download_java(version: dict, minecraft_dir=f'{os.getcwd()}/.minecraft') -> None:
    java_ver = version['javaVersion']['component']
    components_req = requests.get(config.JVM_META_URL)
    if components_req.status_code != 200:
        raise ConnectionError('Failed to get JVM meta')
    components = components_req.json()
    java_url_component = components['linux'][java_ver][0]['manifest']['url']
    java_url_component_req = requests.get(java_url_component)
    if java_url_component_req.status_code != 200:
        raise ConnectionError('Failed to get JVM manifest')
    java_url_component_json = java_url_component_req.json()
    files_java: dict = java_url_component_json['files']

    jvm_dir = os.path.join(minecraft_dir, 'jvm', java_ver)

    # Используем ThreadPoolExecutor для параллельного скачивания
    with ThreadPoolExecutor(max_workers=10) as executor:  # Вы можете настроить max_workers
        futures = []
        for key, file in files_java.items():
            if 'downloads' not in file:
                continue
            local_path = os.path.join(jvm_dir, '/'.join(key.split('/')[:-1]))
            print(file)
            url = file['downloads']['raw']['url']
            futures.append(executor.submit(helpers.download_file, url, local_path))

        # Обрабатываем завершенные задачи
        for future in as_completed(futures):
            try:
                result = future.result()
                print(f"Downloaded: {result}")
            except Exception as e:
                print(f"Error downloading file: {e}")
