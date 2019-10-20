"""This class is used to make CRUD operations on the settings."""

import configparser
from src import logger

titleKeyURL = ""
filters = []
ticketOnly = ""
downloadDir = ""
patchDEMO = ""
patchDLC = ""
titleKeyNag = ""
maxDownloads = ""
retry = ""
dlKeysStartup = ""
dlRssStartup = ""
libraryDir = ""


def create_settings():
    """Create an empty settings file."""
    settings = configparser.RawConfigParser()
    settings.add_section("Settings")
    settings.set("Settings", "titleKeyURL", "http://vault.titlekeys.ovh")
    settings.set("Settings", "downloadDir", "")
    settings.set("Settings", "libraryDir", "")
    settings.set("Settings", "showUSA", "True")
    settings.set("Settings", "showJPN", "False")
    settings.set("Settings", "showEUR", "True")
    settings.set("Settings", "showDLC", "True")
    settings.set("Settings", "showUPDATE", "True")
    settings.set("Settings", "showDEMO", "False")
    settings.set("Settings", "showGAME", "True")
    settings.set("Settings", "ticketOnly", "False")
    settings.set("Settings", "patchDEMO", "True")
    settings.set("Settings", "patchDLC", "True")
    settings.set("Settings", "titleKeyNag", "False")
    settings.set("Settings", "maxDownloads", "1")
    settings.set("Settings", "retry", "3")
    settings.set("Settings", "dlKeysStartup", "3")
    settings.set("Settings", "dlRssStartup", "True")
    with open("settings.cfg", "w") as settingsfile:
        settings.write(settingsfile)


def read_settings():
    """Load settings from file."""
    settings = configparser.RawConfigParser()
    settings.read("settings.cfg")
    global titleKeyURL
    global downloadDir
    global libraryDir
    global ticketOnly
    global patchDEMO
    global patchDLC
    global filters
    global titleKeyNag
    global maxDownloads
    global retry
    global dlKeysStartup
    global dlRssStartup
    titleKeyURL = settings.get("Settings", "titleKeyURL")
    downloadDir = settings.get("Settings", "downloadDir")
    libraryDir = settings.get("Settings", "libraryDir")
    ticketOnly = settings.getboolean("Settings", "ticketOnly")
    patchDEMO = settings.getboolean("Settings", "patchDEMO")
    patchDLC = settings.getboolean("Settings", "patchDLC")
    titleKeyNag = settings.getboolean("Settings", "titleKeyNag")
    maxDownloads = settings.getint("Settings", "maxDownloads")
    retry = settings.getint("Settings", "retry")
    dlKeysStartup = settings.getint("Settings", "dlKeysStartup")
    dlRssStartup = settings.getboolean("Settings", "dlRssStartup")

    if settings.getboolean("Settings", "showUSA"):
        filters.append("USA")

    if settings.getboolean("Settings", "showJPN"):
        filters.append("JPN")

    if settings.getboolean("Settings", "showEUR"):
        filters.append("EUR")

    if settings.getboolean("Settings", "showDLC"):
        filters.append("DLC")

    if settings.getboolean("Settings", "showUPDATE"):
        filters.append("UPDATE")

    if settings.getboolean("Settings", "showDEMO"):
        filters.append("DEMO")

    if settings.getboolean("Settings", "showGAME"):
        filters.append("GAME")

    logger.log("Settings loaded")


def save_settings():
    """Write settings to file."""
    settings = configparser.RawConfigParser()
    settings.add_section("Settings")
    settings.set("Settings", "titleKeyURL", titleKeyURL)
    settings.set("Settings", "downloadDir", downloadDir)
    settings.set("Settings", "libraryDir", libraryDir)
    settings.set("Settings", "ticketOnly", ticketOnly)
    settings.set("Settings", "patchDEMO", patchDEMO)
    settings.set("Settings", "patchDLC", patchDLC)
    settings.set("Settings", "titleKeyNag", titleKeyNag)
    settings.set("Settings", "titleKeyNag", titleKeyNag)
    settings.set("Settings", "maxDownloads", maxDownloads)
    settings.set("Settings", "retry", retry)
    settings.set("Settings", "dlKeysStartup", dlKeysStartup)
    settings.set("Settings", "dlRssStartup", dlRssStartup)

    if "USA" in filters:
        settings.set("Settings", "showUSA", "True")
    else:
        settings.set("Settings", "showUSA", "False")

    if "JPN" in filters:
        settings.set("Settings", "showJPN", "True")
    else:
        settings.set("Settings", "showJPN", "False")

    if "EUR" in filters:
        settings.set("Settings", "showEUR", "True")
    else:
        settings.set("Settings", "showEUR", "False")

    if "DLC" in filters:
        settings.set("Settings", "showDLC", "True")
    else:
        settings.set("Settings", "showDLC", "False")

    if "UPDATE" in filters:
        settings.set("Settings", "showUPDATE", "True")
    else:
        settings.set("Settings", "showUPDATE", "False")

    if "DEMO" in filters:
        settings.set("Settings", "showDEMO", "True")
    else:
        settings.set("Settings", "showDEMO", "False")

    if "GAME" in filters:
        settings.set("Settings", "showGAME", "True")
    else:
        settings.set("Settings", "showGAME", "False")

    with open("settings.cfg", "w") as settingsfile:
        settings.write(settingsfile)
        logger.log("Settings saved")


def set_title_key_url(url):
    """Set the title key url"""
    global titleKeyURL
    titleKeyURL = url


try:
    with open("settings.cfg") as settingsfile:
        read_settings()
except FileNotFoundError as e:
    logger.log("No config file, so one is being created")
    create_settings()
    read_settings()
