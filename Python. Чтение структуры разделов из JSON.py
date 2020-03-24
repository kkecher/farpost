#!/usr/bin/env python3

'''
Собирает список id, название и URL разделов из JSON
Вход: ничего
Выход: список разделов с id, названиями и урлами
'''

import requests
import json

result = input('Enter result file: ')

url = 'https://www.farpost.ru/export/dirs_with_attributes'
response = requests.get(url) 
dir_json = json.loads(response.text)

dir_list = []
def get_dirs_attr(dir_json, dir_url = ''):
    dir_id = dir_json['id']
    dir_title = dir_json['title']
    if dir_id == '0':
        dir_url = 'https://www.farpost.ru'
    else:
        dir_url += '/' + dir_json['urlPart']
    dir_attr = (dir_id, dir_title, dir_url)
    dir_list.append(dir_attr)
    for children in dir_json['children']:
        try:
            get_dirs_attr(children, dir_url)
        except Exception:
            continue

get_dirs_attr(dir_json)

with open(result, 'w') as f:
    for elem in dir_list:
        f.write(f'{elem[0]}\t{elem[1]}\t{elem[2]}\n')
