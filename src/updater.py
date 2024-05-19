import os
import requests


def check_dirs():
    appdata_folder = os.getenv("APPDATA")
    exotic_folder = os.path.join(appdata_folder, "Exotic")

    if not os.path.exists(exotic_folder):
        os.makedirs(exotic_folder)
    return exotic_folder


def get_release_info(url):
    url = r"https://api.github.com/repos/YimMenu/YimMenu/releases/tags/nightly"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # print(data)
        release_name = data["name"]
        published_at = data["published_at"]
        return release_name, published_at
    else:
        return None, None


release_name, published_at = (
    get_release_info()
)  # This will assing respectively with the return

"""
if release_name:
    print(f"Release '{release_name}' of  was published on {published_at}.")
else:
    print(f"Failed to fetch information for release  of .")
"""


def download_file(save_path, url):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"File downloaded successfully and saved at {save_path}.")
    else:
        print(f"Failed to download the file from {url}.")


url = r"https://github.com/YimMenu/YimMenu/releases/download/nightly/YimMenu.dll"
download_folder = check_dirs()
download_path = os.path.join(download_folder, "YimMenu.dll")
