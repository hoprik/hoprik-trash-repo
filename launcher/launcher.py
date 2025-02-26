import os
import subprocess
import json
import platform
from uuid import uuid4
from launcher import helpers


def launch(java, minecraft_path, auth_player_name, version_name, game_directory, assets_root, assets_index_name, auth_uuid,
           auth_access_token, clientid, auth_xuid, user_type, version_type, natives_directory, launcher_name,
           launcher_version, classpath):
    if not os.path.exists(minecraft_path):
        raise FileNotFoundError(minecraft_path)

    # Формируем команду для запуска Minecraft
    command = [
        java,
        f"-Djava.library.path={natives_directory}",
        f"-Dminecraft.launcher.brand={launcher_name}",
        f"-Dminecraft.launcher.version={launcher_version}",
        "-cp",
        classpath,
        "net.minecraft.client.main.Main",
        "--username",
        auth_player_name,
        "--version",
        version_name,
        "--gameDir",
        game_directory,
        "--assetsDir",
        assets_root,
        "--assetIndex",
        assets_index_name,
        "--uuid",
        auth_uuid,
        "--accessToken",
        auth_access_token,
        "--clientId",
        clientid,
        "--xuid",
        auth_xuid,
        "--userType",
        user_type,
        "--versionType",
        version_type,
    ]
    try:
        subprocess.run(command)
    except Exception as e:
        print(f"Error on start Minecraft: {e}")

def get_natives_string(lib):
    if platform.architecture()[0] == "64bit":
        arch = "64"
    elif platform.architecture()[0] == "32bit":
        arch = "32"
    else:
        raise Exception("Architecture not supported")

    natives_file=""
    if not "natives" in lib:
        return natives_file

    if "windows" in lib["natives"] and platform.system() == 'Windows':
        natives_file = lib["natives"]["windows"].replace("${arch}", arch)
    elif "osx" in lib["natives"] and platform.system() == 'Darwin':
        natives_file = lib["natives"]["osx"].replace("${arch}", arch)
    elif "linux" in lib["natives"] and platform.system() == "Linux":
        natives_file = lib["natives"]["linux"].replace("${arch}", arch)
    else:
        raise Exception("Platform not supported")

    return natives_file


def get_classpath(minecraft_path, version):
    cp = []
    version_manifest = os.path.join(minecraft_path, 'versions', version, version + '.json')

    with open(version_manifest, 'r') as f:
        manifest = json.load(f)

    for i in manifest["libraries"]:
        if not helpers.should_use_library(i):
            continue

        if len(i["name"].split(":")) > 3:
            continue
        lib_domain, lib_name, lib_version = i["name"].split(":")
        jar_path = os.path.join(minecraft_path, "libraries", * lib_domain.split('.'), lib_name, lib_version)

        native = get_natives_string(i)
        jar_file = lib_name + "-" + lib_version + ".jar"
        if native != "":
            jar_file = lib_name + "-" + lib_version + "-" + native + ".jar"

        cp.append(os.path.join(jar_path, jar_file))

    cp.append(os.path.join(minecraft_path, "versions", version, f'{version}.jar'))

    return os.pathsep.join(cp)

def get_java_path(minecraft_path, version):
    version_manifest = os.path.join(minecraft_path, 'versions', version, version + '.json')
    
    with open(version_manifest, 'r') as f:
        manifest = json.load(f)

    return manifest['javaVersion']['component']

def launch_minecraft(minecraft_path, player, version):
    assets_dir = os.path.join(minecraft_path, 'assets')
    natives_dir = os.path.join(minecraft_path, 'natives')

    java_path = os.path.join(minecraft_path, 'jvm', get_java_path(minecraft_path, version), 'bin', 'java')

    # Запускаем Minecraft
    launch(
        java_path,
        minecraft_path,
        player,
        version,
        minecraft_path,
        assets_dir,
        '19',  
        str(uuid4()),
        '',
        '',
        '',
        'offline',
        'release',
        natives_dir,
        'mineos',
        '1.0',
        get_classpath(minecraft_path, version) 
    )