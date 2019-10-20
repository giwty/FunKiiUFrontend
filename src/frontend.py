#!/usr/bin/python


from src.util import *
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
from src.logger import log
from src.settings import *
import json
import os
import _thread
import xml.etree.ElementTree
from src import FunKiiUmod as fnk, fileUtil, downloader

gamelist_array = []
download_list = []
current_selected = ""
current_selected_download = ""


def save_settings():
    settings.set_title_key_url(url_input.get())
    settings.save_settings()
    check_tilekey_json()
    refresh_gamelist()
    #_thread.start_new_thread(update_rss, ())


def toggle_dlkeys():
    if dlKeys_chk.get() == 1:
        settings.dlKeysStartup = True
    else:
        settings.dlKeysStartup = False


def toggle_dlrss():
    if dlRss_chk.get() == 1:
        settings.dlRssStartup = True
    else:
        settings.dlRssStartup = False


def toggle_ticket_only():
    if ticketonly_chk.get() == 1:
        settings.ticketOnly = True
    else:
        settings.ticketOnly = False
    refresh_gamelist()


def toggle_patch_demo():
    if patchdemo_chk.get() == 1:
        settings.patchDEMO = True
    else:
        settings.patchDEMO = False


def toggle_patch_dlc():
    if patchdlc_chk.get() == 1:
        settings.patchDLC = True
    else:
        settings.patchDLC = False


def toggle_show_usa():
    if showusa_chk.get() == 1:
        if "USA" not in settings.filters:
            settings.filters.append("USA")
    else:
        if "USA" in settings.filters:
            settings.filters.remove("USA")
    refresh_gamelist()


def toggle_show_jpn():
    if showjpn_chk.get() == 1:
        if "JPN" not in settings.filters:
            settings.filters.append("JPN")
    else:
        if "JPN" in settings.filters:
            settings.filters.remove("JPN")
    refresh_gamelist()


def toggle_show_eur():
    if showeur_chk.get() == 1:
        if "EUR" not in settings.filters:
            settings.filters.append("EUR")
    else:
        if "EUR" in settings.filters:
            settings.filters.remove("EUR")
    refresh_gamelist()


def toggle_show_dlc():
    if showdlc_chk.get() == 1:
        if "DLC" not in settings.filters:
            settings.filters.append("DLC")
    else:
        if "DLC" in settings.filters:
            settings.filters.remove("DLC")
    refresh_gamelist()


def toggle_show_update():
    if showupdate_chk.get() == 1:
        if "UPDATE" not in settings.filters:
            settings.filters.append("UPDATE")
    else:
        if "UPDATE" in settings.filters:
            settings.filters.remove("UPDATE")
    refresh_gamelist()


def toggle_show_demo():
    if showdemo_chk.get() == 1:
        if "DEMO" not in settings.filters:
            settings.filters.append("DEMO")
    else:
        if "DEMO" in settings.filters:
            settings.filters.remove("DEMO")
    refresh_gamelist()


def toggle_show_game():
    if showgame_chk.get() == 1:
        if "GAME" not in settings.filters:
            settings.filters.append("GAME")
    else:
        if "GAME" in settings.filters:
            settings.filters.remove("GAME")
    refresh_gamelist()


def update_max_downloads(e):
    settings.maxDownloads = int(max_download_drop.get())


def update_max_retry(e):
    settings.retries = int(retry_drop.get())


root = Tk()
root.title("FunKiiU Frontend")
root.minsize(width=800, height=600)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
note = Notebook(root)
note.columnconfigure(0, weight=1)
note.rowconfigure(0, weight=1)
note.grid(sticky=NSEW)

# search_tab stuff here


def refresh_download_listbox():
    downloadlist.delete(0, END)
    for game in download_list:
        downloadlist.insert(0, game.listname + " - " + game.status)


def download_games():
    if current_selected != "" and current_selected not in download_list:
        if current_selected.size == "0.00 B":
            messagebox.showwarning(
                "Can't Download", "The file size is 0.00 B\n can't download game")
        else:
            download_list.append(current_selected)
            current_selected.status = "Queued"
            current_selected.downloadcallback = refresh_download_listbox
            downloader.add_game(current_selected)
            refresh_download_listbox()


search_tab = Frame(note)

search_tab.columnconfigure(0)
search_tab.columnconfigure(1, weight=2)
search_tab.columnconfigure(2)
search_tab.columnconfigure(3, weight=1)
search_tab.rowconfigure(0, weight=8)
search_tab.rowconfigure(1, weight=1)

searchlist = Listbox(search_tab)
searchlist.grid(row=0, column=0, sticky="nsew", columnspan=3)
searchlist.columnconfigure(0, weight=1)
searchlist.rowconfigure(0, weight=1)

yscroll = Scrollbar(searchlist, command=searchlist.yview, orient=VERTICAL)
yscroll.grid(row=0, column=1, sticky='ns')
searchlist.configure(yscrollcommand=yscroll.set)

search_label = Label(search_tab, text="Search: ")
search_label.grid(row=1, column=0, sticky=W)

search_input = Entry(search_tab)
search_input.grid(row=1, column=1, sticky=EW)


def clear_search():
    search_input.delete(0, END)
    e = None
    search_games(e)


clr_srch_btn = Button(search_tab, text="Clear", command=clear_search)
clr_srch_btn.grid(row=1, column=2, sticky=E)


def search_games(e):
    searchlist.delete(0, END)
    templist = [x for x in gamelist_array if search_input.get().lower()
                in x.listname.lower()]
    templist.sort(key=lambda game: game.listname, reverse=True)
    for game in templist:
        if game.region in filters and decode_titleid(game.titleid) in filters:
            if settings.ticketOnly and str(game.ticket) == "False":
                pass
            else:
                searchlist.insert(0, game.listname)


search_input.bind('<KeyRelease>', search_games)

infobox = Text(search_tab, height=10, width=30)
infobox.grid(row=0, column=3, sticky="nsew")

dl_btn = Button(search_tab, text="Download", command=download_games)
dl_btn.grid(row=1, column=3)


def search_select(e):
    global current_selected
    infobox.config(state="normal")
    infobox.delete("1.0", END)
    for game in gamelist_array:
        if game.listname == str(searchlist.get(searchlist.curselection())):
            current_selected = game
            game.size = get_title_size(game.titleid)
            infobox.insert(END, "Name: " + game.name + "\n")
            infobox.insert(END, "Region: " + game.region + "\n")
            infobox.insert(END, "Type: " + game.type + "\n")
            infobox.insert(END, "TitleID: " + game.titleid + "\n")
            infobox.insert(END, "TitleKey: " + game.titlekey + "\n")
            infobox.insert(END, "Online Ticket: " + str(game.ticket) + "\n")
            infobox.insert(END, "Size: " + game.size + "\n")
            if game.description != "":
                infobox.insert(END, "Description: " + game.description)
            infobox.config(state="disabled")


searchlist.bind('<ButtonRelease-1>', search_select)


# downloads tab
downloads_tab = Frame(note)

downloads_tab.columnconfigure(0, weight=1)
downloads_tab.columnconfigure(1, weight=1)
downloads_tab.rowconfigure(0, weight=1)

downloadlist = Listbox(downloads_tab, height=20, width=20)
downloadlist.grid(row=0, column=0, sticky=NSEW, columnspan=2)

downloadlist.columnconfigure(0, weight=1)
downloadlist.rowconfigure(0, weight=1)
yscroll = Scrollbar(downloadlist, command=downloadlist.yview, orient=VERTICAL)
yscroll.grid(row=0, column=1, sticky='ns')
downloadlist.configure(yscrollcommand=yscroll.set)


def download_select(e):
    if len(downloadlist.curselection()) > 0:
        global current_selected_download
        current_selected_download = " - ".join(
            str(downloadlist.get(downloadlist.curselection())).split(" - ")[0:3])


downloadlist.bind('<ButtonRelease-1>', download_select)


def cancel_selected():
    downloader.cancel_download(current_selected_download)


rmv_btn = Button(downloads_tab, text="Cancel Selected",
                 command=cancel_selected)
rmv_btn.grid(row=1, column=0, sticky=NE)


def clear_complete():
    downloadlist.delete(0, END)
    templist = list(download_list)
    for game in templist:
        if game.status != "Complete" and game.status != "Canceled" and game.status != "Failed":
            downloadlist.insert(0, game.listname + " - " + game.status)
        else:
            download_list.remove(game)


clr_btn = Button(downloads_tab, text="Clear Complete", command=clear_complete)
clr_btn.grid(row=1, column=1, sticky=NW)


spacer_label2 = Label(downloads_tab, text="")
spacer_label2.grid(row=3, column=0, sticky=NSEW, columnspan=2)

#library_tab stuff here
library_tab = Frame(note)

library_tab.columnconfigure(0)
library_tab.columnconfigure(1, weight=2)
library_tab.columnconfigure(2)
library_tab.columnconfigure(3, weight=1)
library_tab.rowconfigure(0, weight=8)
library_tab.rowconfigure(1, weight=1)

librarylist = Listbox(library_tab)
librarylist.grid(row=0, column=0, sticky="nsew", columnspan=3)
librarylist.columnconfigure(0, weight=1)
librarylist.rowconfigure(0, weight=1)

yscroll = Scrollbar(librarylist, command=librarylist.yview, orient=VERTICAL)
yscroll.grid(row=0, column=1, sticky='ns')
librarylist.configure(yscrollcommand=yscroll.set)

search_library_label = Label(library_tab, text="Search: ")
search_library_label.grid(row=1, column=0, sticky=W)

search_library_input = Entry(library_tab)
search_library_input.grid(row=1, column=1, sticky=EW)

def search_library(e):
    librarylist.delete(0, END)
    templist = [x for x in fileUtil.list_files(settings.libraryDir) if search_library_input.get().lower()
                in x.lower()]
    templist.sort(key=lambda game: game, reverse=True)
    for game in templist:
        librarylist.insert(0, game)

search_library_input.bind('<KeyRelease>', search_library)

def clear_library_search():
    search_library_input.delete(0, END)
    e = None
    search_library(e)


clr_srch_lbr_btn = Button(library_tab, text="Clear", command=clear_library_search)
clr_srch_lbr_btn.grid(row=1, column=2, sticky=E)

library_infobox = Text(library_tab, height=10, width=30)
library_infobox.grid(row=0, column=3, sticky="nsew")

def refresh_librarylist():
    librarylist.delete(0, END)
    for file in fileUtil.list_files(settings.libraryDir):
        librarylist.insert(0,file)


# settings_tab stuff here
settings_tab = Frame(note)
settings_tab.rowconfigure(0, weight=1)
settings_tab.rowconfigure(1, weight=1)
settings_tab.rowconfigure(2, weight=1)
settings_tab.rowconfigure(3, weight=1)
settings_tab.rowconfigure(4, weight=1)
settings_tab.rowconfigure(5, weight=1)
settings_tab.rowconfigure(6, weight=1)
settings_tab.rowconfigure(7, weight=1)
settings_tab.rowconfigure(8, weight=1)
settings_tab.rowconfigure(9, weight=1)
settings_tab.rowconfigure(10, weight=1)
settings_tab.rowconfigure(11, weight=1)
settings_tab.rowconfigure(12, weight=1)
settings_tab.rowconfigure(13, weight=1)
settings_tab.rowconfigure(14, weight=1)
settings_tab.rowconfigure(14, weight=1)


settings_tab.columnconfigure(0, weight=1)
settings_tab.columnconfigure(1, weight=1)
settings_tab.columnconfigure(2, weight=1)
settings_tab.columnconfigure(3, weight=1)


url_label = Label(settings_tab, text="Title Key Website: (http://xxxx.xxxxxxxxx.gq)")
url_label.grid(row=0, column=0, sticky=EW)
url_input = Entry(settings_tab, width=20)
url_input.grid(row=0, column=1, sticky=EW)


def update_tilekey_json():
    if settings.titleKeyURL != "":
        site = settings.titleKeyURL
        download_titlekeys_json()
        load_titlekeys()
        refresh_gamelist()

    else:
        log("Title key site not set in settings")


update_btn = Button(settings_tab, text="Download", command=update_tilekey_json)
update_btn.grid(row=0, column=3, sticky=W)

dlKeys_chk = IntVar()
dlKeys_checkbox = Checkbutton(
    settings_tab, text="Download titlekeys on startup", command=toggle_dlkeys, variable=dlKeys_chk)
dlKeys_checkbox.grid(row=1, column=0, sticky=W)
if settings.dlKeysStartup:
    dlKeys_chk.set(1)

dlRss_chk = IntVar()
dlRss_checkbox = Checkbutton(
    settings_tab, text="Download Rss on startup", command=toggle_dlrss, variable=dlRss_chk)
dlRss_checkbox.grid(row=2, column=0, sticky=W)
if settings.dlRssStartup:
    dlRss_chk.set(1)

downloaddir_label = Label(settings_tab, text="Download Folder:")
downloaddir_label.grid(row=3, column=0, sticky=EW)

downloaddir_input = Entry(settings_tab, width=20)
downloaddir_input.grid(row=3, column=1, sticky=EW, columnspan=2)

def set_download_rirectory():
    dir = filedialog.askdirectory()
    if dir != ():
        settings.downloadDir = dir
        downloaddir_input.delete(0, END)
        downloaddir_input.insert(0, settings.downloadDir)
        


browse_btn = Button(settings_tab, text="Browse",
                    command=set_download_rirectory)
browse_btn.grid(row=3, column=3, sticky=W)

librarydir_label = Label(settings_tab, text="Library Folder:")
librarydir_label.grid(row=4, column=0, sticky=EW)

librarydir_input = Entry(settings_tab, width=20)
librarydir_input.grid(row=4, column=1, sticky=EW, columnspan=2)

def set_library_directory():
    dir = filedialog.askdirectory()
    if dir != ():
        settings.libraryDir = dir
        librarydir_input.delete(0, END)
        librarydir_input.insert(0, settings.libraryDir)
        refresh_librarylist()


browse_lib_btn = Button(settings_tab, text="Browse",
                    command=set_library_directory)
browse_lib_btn.grid(row=4, column=3, sticky=W)

retry_label = Label(settings_tab, text="Download Retries")
retry_label.grid(row=5, column=0, sticky=EW)

retry_drop = Combobox(settings_tab, state="readonly", width=5, values=range(5))
retry_drop.set(settings.retry)
retry_drop.bind("<<ComboboxSelected>>", update_max_retry)
retry_drop.grid(row=5, column=1, sticky=W)

max_download_label = Label(settings_tab, text="Max multiple downloads:")
max_download_label.grid(row=6, column=0, sticky=EW)

max_download_drop = Combobox(
    settings_tab, state="readonly", width=5, values=range(1, 6))
max_download_drop.set(settings.maxDownloads)
max_download_drop.bind("<<ComboboxSelected>>", update_max_downloads)
max_download_drop.grid(row=6, column=1, sticky=W)

ticketonly_chk = IntVar()
ticketonly_checkbox = Checkbutton(
    settings_tab, text="Only show games with tickets", command=toggle_ticket_only, variable=ticketonly_chk)
ticketonly_checkbox.grid(row=7, column=0, sticky=W)
if settings.ticketOnly:
    ticketonly_chk.set(1)

patchdemo_chk = IntVar()
patchdemo_checkbox = Checkbutton(
    settings_tab, text="Patch demos to remove any play count limits", command=toggle_patch_demo, variable=patchdemo_chk)
patchdemo_checkbox.grid(row=8, column=0, sticky=W)
if settings.patchDEMO:
    patchdemo_chk.set(1)

patchdlc_chk = IntVar()
patchdlc_checkbox = Checkbutton(
    settings_tab, text="Patch DLC to unlock all pieces of DLC", command=toggle_patch_dlc, variable=patchdlc_chk)
patchdlc_checkbox.grid(row=8, column=1, sticky=W)
if settings.patchDLC:
    patchdlc_chk.set(1)


region_label = Label(settings_tab, text="Region Filters:")
region_label.grid(row=9, column=0, sticky=W)

showusa_chk = IntVar()
showusa_checkbox = Checkbutton(
    settings_tab, text="USA", command=toggle_show_usa, variable=showusa_chk)
showusa_checkbox.grid(row=10, column=0, sticky=W)
if "USA" in settings.filters:
    showusa_chk.set(1)

showjpn_chk = IntVar()
showjpn_checkbox = Checkbutton(
    settings_tab, text="JPN", command=toggle_show_jpn, variable=showjpn_chk)
showjpn_checkbox.grid(row=10, column=1, sticky=W)
if "JPN" in settings.filters:
    showjpn_chk.set(1)

showeur_chk = IntVar()
showeur_checkbox = Checkbutton(
    settings_tab, text="EUR", command=toggle_show_eur, variable=showeur_chk)
showeur_checkbox.grid(row=10, column=2, sticky=W)
if "EUR" in settings.filters:
    showeur_chk.set(1)

region_label = Label(settings_tab, text="Type Filters:")
region_label.grid(row=11, column=0, sticky=W)

showdlc_chk = IntVar()
showdlc_checkbox = Checkbutton(
    settings_tab, text="DLC", command=toggle_show_dlc, variable=showdlc_chk)
showdlc_checkbox.grid(row=12, column=0, sticky=W)
if "DLC" in settings.filters:
    showdlc_chk.set(1)

showupdate_chk = IntVar()
showupdate_checkbox = Checkbutton(
    settings_tab, text="Update", command=toggle_show_update, variable=showupdate_chk)
showupdate_checkbox.grid(row=12, column=1, sticky=W)
if "UPDATE" in settings.filters:
    showupdate_chk.set(1)

showdemo_chk = IntVar()
showdemo_checkbox = Checkbutton(
    settings_tab, text="Demo", command=toggle_show_demo, variable=showdemo_chk)
showdemo_checkbox.grid(row=12, column=2, sticky=W)
if "DEMO" in settings.filters:
    showdemo_chk.set(1)

showgame_chk = IntVar()
showgame_checkbox = Checkbutton(
    settings_tab, text="GAME", command=toggle_show_game, variable=showgame_chk)
showgame_checkbox.grid(row=12, column=3)
if "GAME" in settings.filters:
    showgame_chk.set(1)

downloaddir_input.delete(0, END)
if settings.downloadDir == "":
    settings.downloadDir = os.getcwd()
    downloaddir_input.insert(0, settings.downloadDir)
else:
    downloaddir_input.insert(0, settings.downloadDir)

save_btn = Button(settings_tab, text="Save", command=save_settings)
save_btn.grid(row=13, column=0, columnspan=5)
spacer = Label(settings_tab).grid(row=14, column=0)

# log_tab
log_tab = Frame(note)
log_tab.rowconfigure(0, weight=1)
log_tab.columnconfigure(0, weight=1)
logbox = Text(log_tab)
logbox.grid(row=0, column=0, sticky="nsew")
logbox.columnconfigure(0, weight=1)
logbox.rowconfigure(0, weight=1)
yscroll = Scrollbar(logbox, command=logbox.yview, orient=VERTICAL)
yscroll.grid(row=0, column=1, sticky='ns')
logbox.configure(yscrollcommand=yscroll.set)
logbox.config(state="disabled")

# rss_tab
rss_tab = Frame(note)
rss_tab.rowconfigure(0)
rss_tab.rowconfigure(1, weight=1)
rss_tab.columnconfigure(0, weight=1)

rssbox = Text(rss_tab)
rssbox.grid(row=1, column=0, sticky="nsew")
rssbox.columnconfigure(0, weight=1)
rssbox.rowconfigure(1, weight=1)
yscroll = Scrollbar(rssbox, command=rssbox.yview, orient=VERTICAL)
yscroll.grid(row=1, column=1, sticky='ns')
rssbox.configure(yscrollcommand=yscroll.set)
rssbox.config(state="disabled")


def update_rss():
    if settings.titleKeyURL != "":
        site = settings.titleKeyURL
        download_titlekeys_rss()
        if os.path.isfile("titlekeysrss.xml"):
            e = xml.etree.ElementTree.parse('titlekeysrss.xml').getroot()
            rssbox.config(state="normal")
            rssbox.delete("1.0", END)
            rssbox.insert("1.0", "Last Build Date: " +
                          e.find("channel").find("lastBuildDate").text + "\n")
            for item in e.find("channel").findall("item"):
                rssbox.insert(END, "------------------" + "\n")
                for child in item:
                    if child.text != None:
                        rssbox.insert(END, child.tag +
                                      ":" + child.text + "\n")
            rssbox.config(state="disabled")

# about_tab stuff here
about_tab = Frame(note)
about_tab.rowconfigure(0, weight=1)
about_tab.columnconfigure(0, weight=1)
aboutbox = Text(about_tab)
aboutbox.grid(row=0, column=0, sticky="nsew")
try:
    with open("about.txt") as about:
        for line in about:
            aboutbox.insert(END, line)
    aboutbox.config(state="disabled")
except Exception as e:
    log("about.txt not found")
    aboutbox.config(state="disabled")


def handler():
    root.destroy()


def enrich_gamelist():
    log("Attempting to enrich game data")
    global gamelist_array
    temp_gamelist_array = []

    if not os.path.isfile('titlekeys.json'):
        download_titlekeys_json()
    with open('titlekeys.json') as jsonfile:
        parsed_json = json.load(jsonfile)
        for record in parsed_json:
            gameupdate = Game()
            if record["name"] is not None:
                gameupdate.name = (record["name"]).replace("\n", " ")
            if record["titleKey"] is not None:
                gameupdate.titlekey = record["titleKey"]
            if record["region"] is not None:
                gameupdate.region = record["region"]
            if record["titleID"] is not None:
                gameupdate.titleid = record["titleID"]
                gameupdate.type = decode_titleid(record["titleID"])
            gameupdate.listname = gameupdate.name + " - " + \
                gameupdate.type + " - " + gameupdate.region
            if record["ticket"] == "1":
                gameupdate.ticket = True
            else:
                gameupdate.ticket = False
            if gameupdate.name != "":
                temp_gamelist_array.append(gameupdate)

    if os.path.isfile("wiiutitles.json"):
        with open('wiiutitles.json') as jsonfile:
            parsed_json = json.load(jsonfile)
            for record in parsed_json:
                titleid = record["titleid"].replace("-", "")
                gameid = record["gameid"]
                if gameid != "":
                    for game in temp_gamelist_array:
                        if titleid == game.titleid:
                            game.gameid = gameid.split("-")[2]

    if not os.path.isfile("wiiutdb.xml"):
        download_wiiutdb()
    e = xml.etree.ElementTree.parse('wiiutdb.xml').getroot()
    for item in e.findall("game"):
        for child in item:
            if child.text != None:
                if child.tag == "locale" and child.attrib["lang"] == "EN" and child.find("synopsis").text != None:
                    description = child.find("synopsis").text
                if child.tag == "id":
                    id = child.text
        for game in temp_gamelist_array:
            if game.gameid != "":
                if game.gameid in id:
                    game.description = description
                    game.id = id

    gamelist_array = list(temp_gamelist_array)
    gamelist_array.sort(key=lambda game: game.listname)
    log("Game data updated with data from wiiutdb")


def load_titlekeys():
    global gamelist_array
    gamelist_array = []
    try:
        with open('titlekeys.json') as jsonfile:
            parsed_json = json.load(jsonfile)
            for record in parsed_json:
                game = Game()
                if record["name"] is not None:
                    game.name = (record["name"]).replace("\n", " ")
                if record["titleKey"] is not None:
                    game.titlekey = record["titleKey"]
                if record["region"] is not None:
                    game.region = record["region"]
                if record["titleID"] is not None:
                    game.titleid = record["titleID"]
                if record["titleID"] is not None:
                    game.type = decode_titleid(record["titleID"])
                game.listname = game.name + " - " + game.type + " - " + game.region
                if record["ticket"] == "1":
                    game.ticket = True
                else:
                    game.ticket = False
                if game.name != "":
                    gamelist_array.append(game)
        gamelist_array.sort(key=lambda game: game.listname)
    except IOError as e:
        log("Unable to load titlekeys")


def check_tilekey_json():
    if settings.titleKeyURL != "":
        if not os.path.isfile("titlekeys.json"):
            site = settings.titleKeyURL
            _thread.start_new(update_tilekey_json, ())

        else:
            load_titlekeys()
            refresh_gamelist()
    else:
        log("Title key site not set in settings")


def update_tilekey_json():
    if settings.titleKeyURL != "":
        site = settings.titleKeyURL
        download_titlekeys_json()
        load_titlekeys()
        refresh_gamelist()

    else:
        log("Title key site not set in settings")


def refresh_gamelist():
    searchlist.delete(0, END)
    templist = list(gamelist_array)
    templist.reverse()
    for game in templist:
        if game.region in filters and decode_titleid(game.titleid) in filters:
            if settings.ticketOnly and str(game.ticket) == "False":
                pass
            else:
                searchlist.insert(0, game.listname)


def initialize_funkiiu_config():
    try:
        with open('config.json') as jsonconfig:
            log("config exists")
    except Exception as e:
        site = settings.titleKeyURL
        print('Correct key site, now saving...')
        config = fnk.load_config()
        #config['keysite'] = site
        #fnk.save_config(config)
        #print('done saving, you are good to go!')


def update_log_tab():
    while 1:
        time.sleep(2)
        try:
            if len(logs) > 0:
                loglist = get_logs()
                logbox.config(state="normal")
                for log in loglist:
                    logbox.insert("1.0", log + "\n")
                logbox.config(state="disabled")
        except:
            pass


note.add(search_tab, text="Search")
note.add(downloads_tab, text="Downloads")
note.add(library_tab, text="Library")
note.add(settings_tab, text="Settings")
note.add(rss_tab, text="RSS")
note.add(log_tab, text="Logs")
note.add(about_tab, text="About")

root.protocol("WM_DELETE_WINDOW", handler)

# initialization steps

url_input.insert(0, settings.titleKeyURL)
check_tilekey_json()
refresh_gamelist()
refresh_librarylist()
initialize_funkiiu_config()
#_thread.start_new_thread(update_rss, ())
_thread.start_new_thread(enrich_gamelist, ())


if settings.titleKeyNag:
    messagebox.showinfo(
        "Title Keys", "Before you can download any games\nYou will need to add the url from that title keys website\nin the settings and save.")
    settings.titleKeyNag = False
    note.select(settings_tab)
    url_input.focus_force()
    save_settings()


_thread.start_new_thread(update_log_tab, ())


try:
    root.mainloop()
except (KeyboardInterrupt, SystemExit) as e:
    print (e.message)
    sys.exit()
