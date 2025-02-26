import os
import threading
from launcher import download, launcher

def download_minecraft(version = None, minecraft_dir=f'{os.getcwd()}/.minecraft'):
    version_manifest, version_id = download.download_version_manifest(version, minecraft_dir)
    threading.Thread(target=download.download_minecraft_jar, args=(version_manifest, version_id)).start()
    threading.Thread(target=download.download_libraries_and_make_native_files, args=(version_manifest, minecraft_dir)).start()
    download.download_assets(version_manifest, minecraft_dir)
    download.download_java(version_manifest, minecraft_dir)

def start_minecraft(minecraft_dir=f'{os.getcwd()}/.minecraft', version='1.21.4', username='root'):
    launcher.launch_minecraft(minecraft_dir, username, version)
