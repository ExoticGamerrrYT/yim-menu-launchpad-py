import os


def check_dirs():
    localappdata_folder = os.getenv("LOCALAPPDATA")
    exotic_folder = os.path.join(localappdata_folder, "Exotic")

    if not os.path.exists(exotic_folder):
        os.makedirs(exotic_folder)
