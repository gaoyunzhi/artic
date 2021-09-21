#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
from telegram_util import log_on_fail
from telegram.ext import Updater
import plain_db
import cached_url
from bs4 import BeautifulSoup
import album_sender
import artic_to_album

MAX_COUNT = 20

with open('credential') as f:
    credential = yaml.load(f, Loader=yaml.FullLoader)

existing = plain_db.loadKeyOnlyDB('existing')
tele = Updater(credential['bot_token'], use_context=True)
debug_group = tele.bot.get_chat(credential['debug_group'])
channel = tele.bot.get_chat(credential['channel'])

@log_on_fail(debug_group)
def run():
    soup = BeautifulSoup(cached_url.get('https://www.artic.edu/collection'), 'html.parser')
    count = 0
    for item in soup.find_all('li', class_='m-listing'):
        album = artic_to_album.get(item, existing)
        if album.empty():
            continue
        count += 1
        album_sender.send_v2(channel, album)
        existing.add(album.url)
        if count >= MAX_COUNT:
            break

if __name__ == '__main__':
    run()