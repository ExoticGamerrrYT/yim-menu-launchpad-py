import os
import requests
import json

RELEASE_URL = r"https://api.github.com/repos/YimMenu/YimMenu/releases/tags/nightly"
DOWNLOAD_URL = (
    r"https://github.com/YimMenu/YimMenu/releases/download/nightly/YimMenu.dll"
)


def check_dirs():
    # Check for Exotic folder
    appdata_folder = os.getenv("APPDATA")
    exotic_folder = os.path.join(appdata_folder, "Exotic")

    if not os.path.exists(exotic_folder):
        os.makedirs(exotic_folder)

    # Check for settings.json
    settings_file = os.path.join(exotic_folder, "settings.json")

    if not os.path.exists(settings_file):
        with open(settings_file, "w") as file:
            json.dump({"date": "None"}, file, indent=4)

    return exotic_folder, settings_file


def get_release_info(url):
    # This gets the value of the "published_at" key
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        published_at = data["published_at"]
        return published_at
    else:
        return None, None


def download_file(save_path, url):
    # This downloads the .dll
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            file.write(response.content)


def download_if_needed():
    """
    This is the main function, it will check the directories, so it creates them if needed. Then
    it will open the settings file and get the value from the date key. Finally it compares the dates
    and if they are different it will update the value of the date key, save the new value and download the dll.
    """
    check_dirs()
    download_folder, settings_file = check_dirs()
    download_path = os.path.join(download_folder, "YimMenu.dll")
    with open(settings_file, "r") as file:
        data = json.load(file)
    previous_date = data["date"]
    new_date = get_release_info(RELEASE_URL)

    if previous_date != new_date:
        data["date"] = new_date
        with open(settings_file, "w") as file:
            json.dump(data, file, indent=4)
        download_file(download_path, DOWNLOAD_URL)
        return True

    return False
