#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'artic_to_album'

from telegram_util import AlbumResult as Result
from googletrans import Translator as TransGoogle
trans_google = TransGoogle()

def getTitle(soup):
    title = soup.find('strong', class_='title')
    print(title)
    return title.text

def getImg(soup):
    img = soup.find('img', {'data-srcset': True})
    return img['data-srcset'].split(', ')[-1].split()[0]

def translate(text):
    return text
    return trans_google.translate(text, dest='zh-CN').text

def getUrl(soup):
    return soup.find('a')['href']

def get(soup):
    result = Result()
    img = getImg(soup)
    if not img.endswith('/full/843,/0/default.jpg'):
        return result
    result.imgs = [img]
    result.url = getUrl(soup)
    cap_html_v2 = translate(getTitle(soup))
    return result