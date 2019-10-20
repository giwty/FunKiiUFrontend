#!/usr/bin/python

""" 
FunKiiUmod

Original FunKiiU by llakssz https://github.com/llakssz/FunKiiU

"""

from __future__ import unicode_literals, print_function

__VERSION__ = 2.2

import base64
import binascii
import hashlib
import json
import os
import re
import sys
import zlib
from math import floor
import shutil
import urllib.request

try:
    from urllib.request import urlopen
    from urllib.error import URLError, HTTPError
except ImportError:
    from urllib2 import urlopen, URLError, HTTPError

try:
    real_input = raw_input  # Python2
except NameError:
    real_input = input  # Python3


def b64decompress(d): return zlib.decompress(base64.b64decode(d))


SYMBOLS = {
    'customary': ('B', 'KB', 'MB', 'GB', 'T', 'P', 'E', 'Z', 'Y'),
}

BLANK_CONFIG = {'keysite': 'http://titlekeys.ovh'}
MAGIC = binascii.a2b_hex('00010003704138EFBBBDA16A987DD901326D1C9459484C88A2861B91A312587AE70EF6237EC50E1032DC39DDE89A96A8E859D76A98A6E7E36A0CFE352CA893058234FF833FCB3B03811E9F0DC0D9A52F8045B4B2F9411B67A51C44B5EF8CE77BD6D56BA75734A1856DE6D4BED6D3A242C7C8791B3422375E5C779ABF072F7695EFA0F75BCB83789FC30E3FE4CC8392207840638949C7F688565F649B74D63D8D58FFADDA571E9554426B1318FC468983D4C8A5628B06B6FC5D507C13E7A18AC1511EB6D62EA5448F83501447A9AFB3ECC2903C9DD52F922AC9ACDBEF58C6021848D96E208732D3D1D9D9EA440D91621C7A99DB8843C59C1F2E2C7D9B577D512C166D6F7E1AAD4A774A37447E78FE2021E14A95D112A068ADA019F463C7A55685AABB6888B9246483D18B9C806F474918331782344A4B8531334B26303263D9D2EB4F4BB99602B352F6AE4046C69A5E7E8E4A18EF9BC0A2DED61310417012FD824CC116CFB7C4C1F7EC7177A17446CBDE96F3EDD88FCD052F0B888A45FDAF2B631354F40D16E5FA9C2C4EDA98E798D15E6046DC5363F3096B2C607A9D8DD55B1502A6AC7D3CC8D8C575998E7D796910C804C495235057E91ECD2637C9C1845151AC6B9A0490AE3EC6F47740A0DB0BA36D075956CEE7354EA3E9A4F2720B26550C7D394324BC0CB7E9317D8A8661F42191FF10B08256CE3FD25B745E5194906B4D61CB4C2E000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000526F6F7400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001434130303030303030330000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007BE8EF6CB279C9E2EEE121C6EAF44FF639F88F078B4B77ED9F9560B0358281B50E55AB721115A177703C7A30FE3AE9EF1C60BC1D974676B23A68CC04B198525BC968F11DE2DB50E4D9E7F071E562DAE2092233E9D363F61DD7C19FF3A4A91E8F6553D471DD7B84B9F1B8CE7335F0F5540563A1EAB83963E09BE901011F99546361287020E9CC0DAB487F140D6626A1836D27111F2068DE4772149151CF69C61BA60EF9D949A0F71F5499F2D39AD28C7005348293C431FFBD33F6BCA60DC7195EA2BCC56D200BAF6D06D09C41DB8DE9C720154CA4832B69C08C69CD3B073A0063602F462D338061A5EA6C915CD5623579C3EB64CE44EF586D14BAAA8834019B3EEBEED3790001000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100042EA66C66CFF335797D0497B77A197F9FE51AB5A41375DC73FD9E0B10669B1B9A5B7E8AB28F01B67B6254C14AA1331418F25BA549004C378DD72F0CE63B1F7091AAFE3809B7AC6C2876A61D60516C43A63729162D280BE21BE8E2FE057D8EB6E204242245731AB6FEE30E5335373EEBA970D531BBA2CB222D9684387D5F2A1BF75200CE0656E390CE19135B59E14F0FA5C1281A7386CCD1C8EC3FAD70FBCE74DEEE1FD05F46330B51F9B79E1DDBF4E33F14889D05282924C5F5DC2766EF0627D7EEDC736E67C2E5B93834668072216D1C78B823A072D34FF3ECF9BD11A29AF16C33BD09AFB2D74D534E027C19240D595A68EBB305ACC44AB38AB820C6D426560C000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000526F6F742D43413030303030303033000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000143503030303030303062000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000137A080BA689C590FD0B2F0D4F56B632FB934ED0739517B33A79DE040EE92DC31D37C7F73BF04BD3E44E20AB5A6FEAF5984CC1F6062E9A9FE56C3285DC6F25DDD5D0BF9FE2EFE835DF2634ED937FAB0214D104809CF74B860E6B0483F4CD2DAB2A9602BC56F0D6BD946AED6E0BE4F08F26686BD09EF7DB325F82B18F6AF2ED525BFD828B653FEE6ECE400D5A48FFE22D538BB5335B4153342D4335ACF590D0D30AE2043C7F5AD214FC9C0FE6FA40A5C86506CA6369BCEE44A32D9E695CF00B4FD79ADB568D149C2028A14C9D71B850CA365B37F70B657791FC5D728C4E18FD22557C4062D74771533C70179D3DAE8F92B117E45CB332F3B3C2A22E705CFEC66F6DA3772B000100010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010004919EBE464AD0F552CD1B72E7884910CF55A9F02E50789641D896683DC005BD0AEA87079D8AC284C675065F74C8BF37C88044409502A022980BB8AD48383F6D28A79DE39626CCB2B22A0F19E41032F094B39FF0133146DEC8F6C1A9D55CD28D9E1C47B3D11F4F5426C2C780135A2775D3CA679BC7E834F0E0FB58E68860A71330FC95791793C8FBA935A7A6908F229DEE2A0CA6B9B23B12D495A6FE19D0D72648216878605A66538DBF376899905D3445FC5C727A0E13E0E2C8971C9CFA6C60678875732A4E75523D2F562F12AABD1573BF06C94054AEFA81A71417AF9A4A066D0FFC5AD64BAB28B1FF60661F4437D49E1E0D9412EB4BCACF4CFD6A3408847982000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000526F6F742D43413030303030303033000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000158533030303030303063000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000137A0894AD505BB6C67E2E5BDD6A3BEC43D910C772E9CC290DA58588B77DCC11680BB3E29F4EABBB26E98C2601985C041BB14378E689181AAD770568E928A2B98167EE3E10D072BEEF1FA22FA2AA3E13F11E1836A92A4281EF70AAF4E462998221C6FBB9BDD017E6AC590494E9CEA9859CEB2D2A4C1766F2C33912C58F14A803E36FCCDCCCDC13FD7AE77C7A78D997E6ACC35557E0D3E9EB64B43C92F4C50D67A602DEB391B06661CD32880BD64912AF1CBCB7162A06F02565D3B0ECE4FCECDDAE8A4934DB8EE67F3017986221155D131C6C3F09AB1945C206AC70C942B36F49A1183BCD78B6E4B47C6C5CAC0F8D62F897C6953DD12F28B70C5B7DF751819A98346526250001000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
TIKTEM = binascii.a2b_hex('00010004d15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11a000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000526f6f742d434130303030303030332d585330303030303030630000000000000000000000000000000000000000000000000000000000000000000000000000feedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedface010000cccccccccccccccccccccccccccccccc00000000000000000000000000aaaaaaaaaaaaaaaa00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010014000000ac000000140001001400000000000000280000000100000084000000840003000000000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')

TK = 0x140


def bytes2human(n, f='%(value).2f %(symbol)s', symbols='customary'):
    n = int(n)
    if n < 0:
        raise ValueError("n < 0")
    symbols = SYMBOLS[symbols]
    prefix = {}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i + 1) * 10
    for symbol in reversed(symbols[1:]):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return f % locals()
    return f % dict(symbol=symbols[0], value=n)


RE_16_HEX = re.compile(r'^[0-9a-f]{16}$', re.IGNORECASE)
RE_32_HEX = re.compile(r'^[0-9a-f]{32}$', re.IGNORECASE)

check_title_id = RE_16_HEX.match
check_title_key = RE_32_HEX.match


def retry(count):
    for i in range(1, count + 1):
        if i > 1:
            print("*Attempt {} of {}".format(i, count))
        yield i


def progress_bar(part, total, length=10, char='#', blank=' ', left='[', right=']'):
    percent = int((float(part) / float(total) * 100) % 100)
    bar_len = int((float(part) / float(total) * length) % length)
    bar = char * bar_len
    blanks = blank * (length - bar_len)
    return '{}{}{}{} {} of {}, {}%'.format(
        left, bar, blanks, right, bytes2human(
            part), bytes2human(total), percent
    ) + ' ' * 20


def download_file(url, outfname, retry_count=3, ignore_404=False, expected_size=None, chunk_size=0x4096):
    for _ in retry(retry_count):
        try:
            hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
            req = urllib.request.Request(url, headers=hdr)
            infile = urllib.request.urlopen(req)
            # start of modified code
            if os.path.isfile(outfname):
                statinfo = os.stat(outfname)
                diskFilesize = statinfo.st_size
            else:
                diskFilesize = 0
            try:
                print('-Downloading {}.\n-File size is {}.\n-File in disk is {}.'.format(
                    outfname, expected_size, diskFilesize))
            except UnicodeEncodeError:
                print('-Downloading {}.\n-File size is {}.\n-File in disk is {}.'.format(
                    repr(outfname), expected_size, diskFilesize))

            # if not (expected_size is None):
            if expected_size != diskFilesize:
                with open(outfname, 'wb') as outfile:
                    downloaded_size = 0
                    while True:
                        buf = infile.read(chunk_size)
                        if not buf:
                            break
                        downloaded_size += len(buf)
                        if expected_size and len(buf) == chunk_size:
                            print(' Downloaded {}'.format(progress_bar(
                                downloaded_size, expected_size)), end='\r')
                        outfile.write(buf)
            else:
                print('-File skipped.')
                downloaded_size = statinfo.st_size
            # end of modified code

            if expected_size is not None:
                if int(os.path.getsize(outfname)) != expected_size:
                    print('Content download not correct size\n')
                    continue
                else:
                    print('Download complete: {}\n'.format(
                        bytes2human(downloaded_size)) + ' ' * 40)
        except HTTPError as e:
            if e.code == 404 and ignore_404:
                # We are ignoring this because its a 404 error, not a failure
                return True
        except URLError:
            print('Could not download file...\n')
        else:
            return True
    return False


def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except IOError:
        save_config(BLANK_CONFIG)
        return BLANK_CONFIG.copy()


def save_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, f)


def get_keysite():
    config = load_config()
    return config.get('keysite')


def patch_ticket_dlc(tikdata):
    tikdata[TK + 0x164:TK + 0x210] = b64decompress(
        'eNpjYGQQYWBgWAPEIgwQNghoADEjELeAMTNE8D8BwEBjAABCdSH/')


def patch_ticket_demo(tikdata):
    tikdata[TK + 0x124:TK + 0x164] = bytes([0x00] * 64)


def make_ticket(title_id, title_key, title_version, fulloutputpath, patch_demo=False, patch_dlc=False):
    tikdata = bytearray(TIKTEM)
    tikdata[TK + 0xA6:TK + 0xA8] = title_version
    tikdata[TK + 0x9C:TK + 0xA4] = binascii.a2b_hex(title_id)
    tikdata[TK + 0x7F:TK + 0x8F] = binascii.a2b_hex(title_key)
    # not sure what the value at 0xB3 is... mine is 0 but some i see 5.
    # or 0xE0, the reserved data is...?
    typecheck = title_id[4:8]
    if typecheck == '0002' and patch_demo:
        patch_ticket_demo(tikdata)
    elif typecheck == '000c' and patch_dlc:
        patch_ticket_dlc(tikdata)
    open(fulloutputpath, 'wb').write(tikdata)


def safe_filename(filename):
    keep = ' ._'
    return re.sub(r'_+', '_', ''.join(c if (c.isalnum() or c in keep) else '_' for c in filename)).strip('_ ')


class process_title_id(object):
    def __init__(self):
        self.run = True
        self.logger = None
        self.title_id = ""
        self.title_key = ""
        self.name = None
        self.region = None
        self.output_dir = None
        self.retry_count = 3
        self.onlinetickets = False
        self.patch_demo = False
        self.patch_dlc = False
        self.simulate = False
        self.tickets_only = False
        self.percent = ""
        self.percentcallback = ""

    def setup(self, title_id, title_key, name=None, region=None, output_dir=None, retry_count=3, onlinetickets=False, patch_demo=False, patch_dlc=False, simulate=False, tickets_only=False):
        self.title_id = title_id
        self.title_key = title_key
        self.name = name
        self.region = region
        self.output_dir = output_dir
        self.retry_count = retry_count
        self.onlinetickets = onlinetickets
        self.patch_demo = patch_demo
        self.patch_dlc = patch_dlc
        self.simulate = simulate
        self.tickets_only = tickets_only

    def setLogger(self, logger):
        self.logger = logger

    def setPercentCallback(self, callback):
        self.percentcallback = callback

    def log(self, msg):
        if self.logger != None:
            self.logger(msg)
        else:
            print(msg)

    def stop(self):
        self.run = False

    def download_file(self, url, outfname, retry_count=3, ignore_404=False, expected_size=None, chunk_size=0x4096):
        for _ in retry(retry_count):
            try:
                infile = urlopen(url)
                # start of modified code
                if os.path.isfile(outfname):
                    statinfo = os.stat(outfname)
                    diskFilesize = statinfo.st_size
                else:
                    diskFilesize = 0
                try:
                    self.log('-Downloading {}.\n-File size is {}.\n-File in disk is {}.'.format(
                        outfname, expected_size, diskFilesize))
                except UnicodeEncodeError:
                    self.log('-Downloading {}.\n-File size is {}.\n-File in disk is {}.'.format(
                        repr(outfname), expected_size, diskFilesize))

                # if not (expected_size is None):
                if expected_size != diskFilesize:
                    with open(outfname, 'wb') as outfile:
                        downloaded_size = 0
                        while True:
                            if not self.run:
                                return False
                            buf = infile.read(chunk_size)
                            if not buf:
                                break
                            downloaded_size += len(buf)
                            if expected_size and len(buf) == chunk_size:
                                self.log(' Downloaded {}'.format(progress_bar(
                                    downloaded_size, expected_size)))
                            outfile.write(buf)
                else:
                    self.log('-File skipped.')
                    downloaded_size = statinfo.st_size
                # end of modified code

                if expected_size is not None:
                    if int(os.path.getsize(outfname)) != expected_size:
                        self.log('Content download not correct size\n')
                        continue
                    else:
                        self.log('Download complete: {}\n'.format(
                            bytes2human(downloaded_size)) + ' ' * 40)
            except HTTPError as e:
                if e.code == 404 and ignore_404:
                    # We are ignoring this because its a 404 error, not a
                    # failure
                    return True
            except URLError:
                self.log('Could not download file...\n')
            else:
                return True
        return False

    def start(self):
        if self.name:
            dirname = '{} - {} - {}'.format(self.title_id,
                                            self.region, self.name)
        else:
            dirname = self.title_id

        typecheck = self.title_id[4:8]
        if typecheck == '000c':
            dirname = dirname + ' - DLC'
        elif typecheck == '000e':
            dirname = dirname + ' - Update'

        rawdir = os.path.join('install', safe_filename(dirname))

        if self.simulate:
            self.log('Simulate: Would start work in in: "{}"'.format(rawdir))
            return

        self.log('Starting work in: "{}"'.format(rawdir))

        if self.output_dir is not None:
            rawdir = os.path.join(self.output_dir, rawdir)

        if not os.path.exists(rawdir):
            os.makedirs(os.path.join(rawdir))

        # download stuff
        self.log('Downloading TMD...')

        baseurl = 'http://ccs.cdn.c.shop.nintendowifi.net/ccs/download/{}'.format(
            self.title_id)
        tmd_path = os.path.join(rawdir, 'title.tmd')
        if not download_file(baseurl + '/tmd', tmd_path, self.retry_count):
            self.log('ERROR: Could not download TMD...')
            self.log(
                'MAYBE YOU ARE BLOCKING CONNECTIONS TO NINTENDO? IF YOU ARE, DON\'T...! :)')
            self.log('Skipping title...')
            shutil.rmtree(rawdir, ignore_errors=True)
            return

        with open(os.path.join(rawdir, 'title.cert'), 'wb') as f:
            f.write(MAGIC)

        with open(tmd_path, 'rb') as f:
            tmd = f.read()

        title_version = tmd[TK + 0x9C:TK + 0x9E]

        # get ticket from keysite, from cdn if game update, or generate ticket
        if typecheck == '000e':
            print(
                '\nThis is an update, so we are getting the legit ticket straight from Nintendo.')
            if not download_file(baseurl + '/cetk', os.path.join(rawdir, 'title.tik'), self.retry_count):
                self.log('ERROR: Could not download ticket from {}'.format(
                    baseurl + '/cetk'))
                self.log('Skipping title...')
                shutil.rmtree(rawdir, ignore_errors=True)
                return
        elif self.onlinetickets:
            keysite = get_keysite()
            tikurl = '{}/ticket/{}.tik'.format(keysite, self.title_id)
            if not download_file(tikurl, os.path.join(rawdir, 'title.tik'), self.retry_count):
                self.log(
                    'ERROR: Could not download ticket from {}'.format(tikurl))
                self.log('Skipping title...')
                shutil.rmtree(rawdir, ignore_errors=True)
                return
        else:
            make_ticket(self.title_id, self.title_key, title_version, os.path.join(
                rawdir, 'title.tik'), self.patch_demo, self.patch_dlc)

        if self.tickets_only:
            self.log('Ticket, TMD, and CERT completed. Not downloading contents.')
            return

        self.log('Downloading Contents...')
        content_count = int(binascii.hexlify(tmd[TK + 0x9E:TK + 0xA0]), 16)


        total_size = 0
        for i in range(content_count):
            c_offs = 0xB04 + (0x30 * i)
            total_size += int(binascii.hexlify(
                tmd[c_offs + 0x08:c_offs + 0x10]), 16)
        self.log('Total size is {}\n'.format(bytes2human(total_size)))

        #todo:dsfsdfs
        for i in range(content_count):
            c_offs = 0xB04 + (0x30 * i)
            c_id = binascii.hexlify(tmd[c_offs:c_offs + 0x04]).decode()
            c_type = binascii.hexlify(tmd[c_offs + 0x06:c_offs + 0x8])
            expected_size = int(binascii.hexlify(
                tmd[c_offs + 0x08:c_offs + 0x10]), 16)
            self.log('Downloading {} of {} for {}.'.format(
                i + 1, content_count, dirname))
            outfname = os.path.join(rawdir, c_id + '.app')
            outfnameh3 = os.path.join(rawdir, c_id + '.h3')

            if not self.download_file('{}/{}'.format(baseurl, c_id), outfname, self.retry_count, expected_size=expected_size):
                self.log(
                    'ERROR: Could not download content file... Skipping title')
                shutil.rmtree(rawdir, ignore_errors=True)
                return
            if not self.download_file('{}/{}.h3'.format(baseurl, c_id), outfnameh3, self.retry_count, ignore_404=True):
                self.log('ERROR: Could not download h3 file... Skipping title')
                shutil.rmtree(rawdir, ignore_errors=True)
                return

            self.percent = str(
                int((float(i + 1) / float(content_count)) * 100)) + "%"
            if self.percentcallback != "":
                self.percentcallback()

        self.log('Title download complete in "{}"\n'.format(dirname))


def log(output):
    if sys.stdout.encoding != None:
        print(output.encode(sys.stdout.encoding, errors='replace'))
    else:
        print(output.encode("utf-8", errors='replace'))
