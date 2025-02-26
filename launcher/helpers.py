import platform
import requests
import os

def download_file(url, output_path, name=None):
    local_filename = f'{output_path}/{url.split('/')[-1] if name is None else name}'
    total_bytes = 0  # Initialize a counter for total bytes downloaded

    if os.path.exists(local_filename):
        return local_filename

    if not os.path.exists(output_path):
        mkdir_is_not_exists(output_path)

    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:  # Ensure that the chunk is not empty
                    f.write(chunk)
                    total_bytes += len(chunk)  # Increment the total bytes by the size of the chunk
                    print(f"Downloaded { total_bytes / (1024 * 1024):.2f} megabytes of {url.split('/')[-1]}")

    # Calculate the size in megabytes
    total_megabytes = total_bytes / (1024 * 1024)  # Convert bytes to megabytes
    print(f"Downloaded {local_filename} ({total_megabytes:.2f} MB)")

    return local_filename


def mkdir_is_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def should_use_library(lib):
    def rule_says_yes(rule):
        use_lib = None

        if rule["action"] == "allow":
            use_lib = False
        elif rule["action"] == "disallow":
            use_lib = True

        if "os" in rule:
            for key, value in rule["os"].items():
                os = platform.system()
                if key == "name":
                    if value == "windows" and os != 'Windows':
                        return use_lib
                    elif value == "osx" and os != 'Darwin':
                        return use_lib
                    elif value == "linux" and os != 'Linux':
                        return use_lib
                elif key == "arch":
                    if value == "x86" and platform.architecture()[0] != "32bit":
                        return use_lib

        return not use_lib

    if not "rules" in lib:
        return True

    shoulduse_library = False
    for i in lib["rules"]:
        if rule_says_yes(i):
            return True

    return shoulduse_library

def is_native_library(lib):
    return "rules" in lib