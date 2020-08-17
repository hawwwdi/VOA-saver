#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pdfkit
import requests
import sys
from datetime import datetime
from os import mkdir
from tqdm import tqdm
from os.path import expanduser


MP3_URL = 'https://gandalf.ddo.jp/mp3/$.mp3'
PDF_URL = 'https://gandalf.ddo.jp/html/$.html'
SAVE_PATH = expanduser("~") + '/voa/'


def today():
    return datetime.today().strftime('%Y%m%d')[2:]


def save(mp3, html, date):
    savePath = rf'{SAVE_PATH}{date}/'
    try:
        mkdir(savePath)
        print('download pdf:')
        pdfkit.from_url(html, rf'{savePath}{date}.pdf')
        print('download mp3:')
        voice = requests.get(mp3, allow_redirects=True, stream=True)
        contentLength = int(voice.headers.get('content-length', 0))
        progress = tqdm(total=contentLength, unit='ib', unit_scale=True)
        with open(rf'{savePath}{date}.mp3', 'wb') as file:
            for data in voice.iter_content(1024):
                progress.update(len(data))
                file.write(data)
            progress.close()
        print('download complete')
    except FileExistsError:
        print('file already exists!')
        sys.exit()
    except:
        print('connection Lost!')
        sys.exit()
    pass


def get(date):
    mp3 = MP3_URL.replace("$", date)
    pdf = PDF_URL.replace("$", date)
    save(mp3, pdf, date)
    pass


if __name__ == "__main__":
    print("save to: ", SAVE_PATH)
    try:
        get(sys.argv[1])
    except IndexError:
        get(today())
    pass
