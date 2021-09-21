#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'artic_to_album'

from telegram_util import AlbumResult as Result
from googletrans import Translator as TransGoogle
trans_google = TransGoogle()

def getTitle(soup):
    title = soup.find('strong', class_='title')
    return title.text

def getImg(soup):
    img = soup.find('img', {'data-srcset': True})
    return img['data-srcset'].split(', ')[-1].split()[0]

def translate(text):
    return trans_google.translate(text, dest='zh-CN').text

def getUrl(soup):
    return soup.find('a')['href']

def get(soup, existing):
    img = getImg(soup)
    url = getUrl(soup)
    if not img.endswith('/full/843,/0/default.jpg'):
        return Result()
    if existing.contain(url):
        return Result()

    result = Result()    
    result.imgs = [img]
    result.url = url
    result.cap_html_v2 = translate(getTitle(soup))
    return result