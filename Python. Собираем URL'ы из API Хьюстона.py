#!/usr/bin/env python3

'''
Собирает урлы с поисками по фразам в разделах, которые вернул API Хьюстона
Вход: список фраз
Выход: набор поисковых урлов в разделах, которые вернул Хьюстон

Тут используется файл соответствий id раздела - URL раздела, полученый по «Python. Чтение структуры разделов из JSON.py»
'''

import requests
import json

#keywords_file = input('Enter file with keywords: ')
#results = input('Enter results file: ')
keywords_file = 'Теги. Локальные поиски v4.txt'
results = 'res'

dirs = 'Теги. Разделы.txt'
print()

houston_url = 'http://farpost.ru/backend/search-suggest/expertise?q='

try:
    with open(keywords_file, 'r', encoding = 'utf8') as f:
        cyr_keywords = f.read().splitlines()
except:
    with open(keywords_file, 'r', encoding = 'cp1251') as f:
        cyr_keywords = f.read().splitlines()

#Кодируем кириллицу в URL-формат, иначе выпадает ошибка. По буквам, потому что иначе спецсимволы превращаются в тыкву.
keywords_list = []
for cyr_keyword in cyr_keywords:
    cyr_keyword = cyr_keyword.replace('ё', 'е')
    cyr_keyword = cyr_keyword.replace(' ', '%20')
    cyr_keyword = cyr_keyword.replace('%', '%25')
    is_cyr = 0
    keyword_url = ''
    cyr_world = ''
    for letter in cyr_keyword:
        if ord(letter) in range(1040,1104):
            cyr_world += letter
            is_cyr = 1
        elif is_cyr == 1:
            cyr_world = requests.compat.quote_plus(cyr_world.encode('utf8'))
            keyword_url += cyr_world+letter
            is_cyr = 0
            cyr_world = ''
        else:
            keyword_url += letter
    if is_cyr == 1:
        cyr_world = requests.compat.quote_plus(cyr_world.encode('utf8'))
        keyword_url += cyr_world
        cyr_world = ''
    keywords_list.append((cyr_keyword, keyword_url))

#Собираем словарь соответствий id раздела - URL раздела из файла «Теги. Разделы.txt»
dir_dict = {}
with open(dirs, 'r') as f:
    for line in f:
        line = line.strip()
        line = line.split('\t')
        dir_id = line[0]
        dir_url = line[2]
        dir_dict[dir_id] = dir_url


#Получаем id разделов из Хьюстона для каждой фразы
keywords_id_dict = {}
i = 1
for keyword_url_tuple in keywords_list:
    try:
        keyword_url = keyword_url_tuple[1]
        print(f'Doing {i} of {len(keywords_list)}')
        url = houston_url + keyword_url
        response = requests.get(url)
        houston_json = json.loads(response.text)
        if houston_json['suggestions'] == []: #если Хьюстон не вернул никаких разделов, то записываем 0 (корень Фарпоста)
            dir_id = 0
            keywords_id_dict.setdefault(keyword_url_tuple, []).append(dir_id)
        else:
            for elem in houston_json['suggestions']:
                dir_id = elem['directoryId']
                keywords_id_dict.setdefault(keyword_url_tuple, []).append(dir_id)
        i += 1
    except:
        keywords_id_dict.setdefault(keyword_url_tuple, []).append('АХТУНГ!!!')

with open('res', 'w') as f:
    for keyword_url_tuple, dir_ids in keywords_id_dict.items():
        cyr_keyword = keyword_url_tuple[0]
        cyr_keyword = cyr_keyword.replace('%20', ' ')
        keyword_url = keyword_url_tuple[1]
        for dir_id in dir_ids:
            if dir_id == 'АХТУНГ!!!':
                dir_url = 'АХТУНГ!!!'
                search_url = dir_url
            else:
                dir_url = dir_dict[str(dir_id)]
                search_url = dir_url + '/?query=' + str(keyword_url)
            f.write(f'{cyr_keyword}\t{search_url}\n')
