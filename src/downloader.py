try:
    import FunKiiUmod as fnk, settings
except Exception:
    pass

import _thread
import time
from logger import log

download_list = []
downloading = []


def download_games():
    global downloading
    global download_list
    while 1:
        time.sleep(1)
        if len(download_list) > 0:
            game = download_list[-1]
            if len(downloading) < settings.maxDownloads:
                download = threaded_download()
                download.setGame(game)
                downloading.append(download)
                _thread.start_new_thread(download.start, ())
                download_list.remove(game)


def add_game(game):
    download_list.append(game)


def cancel_download(listname):
    global download_list
    templist = list(download_list)
    for game in templist:
        if game.listname == listname:
            download_list.remove(game)
            game.status = "Canceled"
            game.downloadcallback()

    for download in downloading:
        if listname == download.getGame().listname:
            download.stop()


class threaded_download(object):
    def __init__(self):
        self.game = ""
        self.fnkdownload = ""

    def setGame(self, game):
        self.game = game

    def getGame(self):
        return self.game

    def stop(self):
        self.fnkdownload.stop()
        self.game.canceled = True

    def percentcallback(self):
        self.game.status = "Downloading: " + self.fnkdownload.percent
        self.game.downloadcallback()

    def start(self):
        global downloading
        log("downloading:" + self.game.listname)
        self.game.status = "Downloading"
        self.game.downloadcallback()
        try:
            process = fnk.process_title_id()
            process.setup(self.game.titleid, self.game.titlekey, self.game.name, self.game.region, settings.downloadDir,
                          settings.retry, self.game.ticket, settings.patchDEMO, settings.patchDLC, False, False)
            process.setLogger(log)
            process.setPercentCallback(self.percentcallback)
            self.fnkdownload = process
            process.start()
            downloading.remove(self)
            if self.game.canceled:
                self.game.status = "Canceled"
                self.game.downloadcallback()
                log("canceled download:" + self.game.listname)
            else:
                self.game.status = "Complete"
                self.game.downloadcallback()
                log("done downloading:" + self.game.listname)

        except Exception as e:
            self.game.status = "Failed"
            self.game.downloadcallback()
            if self in downloading:
                downloading.remove(self)
            log("download failed:" + self.game.listname)
            print(repr(e))


try:
    _thread.start_new_thread(download_games, ())
except:
    log("Error: unable to start thread")
