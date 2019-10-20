"""This is a utility class to help with misc tasks"""

import urllib.request
from src.logger import *
import binascii
import os
import zipfile
from src import FunKiiUmod as fnk, settings

funkiiu_url = "https://raw.githubusercontent.com/llakssz/FunKiiU/master/FunKiiUmod.py"
wiiutdb_url = "http://www.gametdb.com/wiiutdb.zip"


def download_funkiiu():
    try:
        urllib.request.urlretrieve(funkiiu_url, "FunKiiUmod.py")
        log("FunKiiU successfully downloaded.")
    except Exception as error:
        log(error)


def unpack_zip(zip_name):
    try:
        zip_ref = zipfile.ZipFile(zip_name, 'r')
        zip_ref.extractall(os.curdir)
        zip_ref.close()
        os.remove(zip_name)
    except Exception as e:
        log('Error:' + e)


class Game(object):
    def __init__(self):
        self.name = ""
        self.titlekey = ""
        self.titleid = ""
        self.region = ""
        self.type = ""
        self.ticket = False
        self.listname = ""
        self.description = ""
        self.size = ""
        self.status = ""
        self.canceled = False
        self.downloadcallback = ""
        self.gameid = ""


def download_titlekeys_json():
    log("Attempting to download titlekey json...")
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(settings.titleKeyURL +
                           "/json/", "titlekeys.json")
        log("titlekeys.json successfully downloaded.")
    except Exception as error:
        log(repr(error))


def download_titlekeys_rss():
    log("Attempting to download titlekey rss...")
    try:
        urllib.request.urlretrieve(settings.titleKeyURL +
                           "/rss", "titlekeysrss.xml")
        log("titlekeysrss.xml successfully downloaded.")
    except Exception as error:
        log("Failed to download rss feed:" + repr(error))


def download_wiiutdb():
    log("Attempting to download wiiutdb.zip")
    try:
        urllib.request.urlretrieve(wiiutdb_url, "wiiutdb.zip")
        log("wiiutdb.zip successfully downloaded.")
        unpack_zip("wiiutdb.zip")
        log("wiiutdb.xml extracted")
    except Exception as error:
        log(repr(error))


def decode_titleid(titleid):
    content_type = ""
    if titleid[4:8] == '0000':
        content_type = 'GAME'
    elif titleid[4:8] == '000c':
        content_type = 'DLC'
    elif titleid[4:8] == '000e':
        content_type = 'UPDATE'
    elif titleid[4:8] == '0002':
        content_type = 'DEMO'
    return content_type


def get_title_size(titleid):
    baseurl = 'http://ccs.cdn.c.shop.nintendowifi.net/ccs/download/{}'.format(
        titleid)
    TK = fnk.TK
    if not fnk.download_file(baseurl + '/tmd', 'title.tmd', 1):
        log('ERROR: Could not download TMD...')
        return fnk.bytes2human(0)
    else:
        with open('title.tmd', 'rb') as f:
            tmd = f.read()
        content_count = int(binascii.hexlify(tmd[TK + 0x9E:TK + 0xA0]), 16)
        os.remove('title.tmd')

        total_size = 0
        for i in range(content_count):
            c_offs = 0xB04 + (0x30 * i)
            c_id = binascii.hexlify(tmd[c_offs:c_offs + 0x04]).decode()
            total_size += int(binascii.hexlify(
                tmd[c_offs + 0x08:c_offs + 0x10]), 16)
        return fnk.bytes2human(total_size)
