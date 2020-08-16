#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pdfkit
import requests
import bs4
import sys
import time
from datetime import datetime
from os import mkdir
from fire import Fire
from tqdm import tqdm
from os.path import expanduser

URL = 'https://gandalf.ddo.jp/'
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


def get(date=today()):
    try:
        req = requests.get(URL)
        soup = bs4.BeautifulSoup(req.text, 'lxml')
        links = soup.select('table tbody tr td')
        index = [i for i in range(len(links))
                 if str(date) in links[i].text and i % 3 == 2][0]
        save(links[index - 2].a['href'], links[index].a['href'], date)
    except IndexError:
        print(f'any file found in date: {date} ')
    except:
        print('connection Lost!')
        sys.exit()
    pass


if __name__ == "__main__":
    print("save to: ", SAVE_PATH)
    Fire(get)
    pass
