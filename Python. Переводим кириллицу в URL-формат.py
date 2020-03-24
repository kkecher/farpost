#!/usr/bin/env python3

import urllib.parse
import requests
import re



with open('res', 'r', encoding = 'utf8') as f:
    urls = f.readlines()

new_urls = []
for url in urls:
    url = url.replace('ё', 'е')
    is_cyr = 0
    new_url = ''
    cyr_world = ''
    for letter in url:
        if ord(letter) in range(1040,1104):
            cyr_world += letter
            is_cyr = 1
        elif is_cyr == 1:
            cyr_world = requests.compat.quote_plus(cyr_world.encode('cp1251'))
            new_url += cyr_world+letter
            is_cyr = 0
            cyr_world = ''
        else:
            new_url += letter
    if is_cyr == 1:
        cyr_world = urllib.parse.quote(cyr_world)
        new_url += cyr_world
        cyr_world = ''
    new_urls.append(new_url)

with open('result', 'w') as f:
    for url in new_urls:
        f.write(str(url))
