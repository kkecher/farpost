#!/usr/bin/env python3

'''
Собирает локальные поиски для списка id разделов
Вход: файл с id / Название / URL раздела, полученый по «Python. Чтение структуры разделов из JSON.py»
Выход: ТОП1000 локальных поисков по разделам
'''

import requests
import json

#dirs_id_file = input('Enter file with dirs: ')
#results = input('Enter results file: ')
dirs_id_file = 'Теги. Разделы.txt'
results = 'res'
print()

query_url_1 = 'http://query-info.srv.loc/api/most_popular?dirId='
#query_url_2 = dir_id
query_url_3 = '&cityId=0&dateFrom=2019-12-01&dateTo=2019-12-31&previousDateFrom=2019-11-01&previousDateTo=2019-11-30'

with open(dirs_id_file, 'r', encoding = 'cp1251') as f:
    dirs_dict = {}
    for line in f:
        line = line.strip()
        line_list = line.split('\t')
        line_tuple = tuple(line_list)
        dirs_dict[line_tuple] = ()

#Получаем ТОП1000 запросов для каждого id раздела
query_dict = {}
i = 1
for dir_tuple in dirs_dict:
    print(f'Doing {i} of {len(dirs_dict)}')
    dir_id = dir_tuple[0]
    url = query_url_1 + dir_id + query_url_3
    response = requests.get(url)
    query_json = json.loads(response.text)
    for elem in query_json:
        query = elem['query']
        freq = elem['currentPeriodUsers']
        query_freq_tuple = (query, freq)
        query_dict.setdefault(dir_tuple, []).append(query_freq_tuple)
    i += 1

#Записываем в файл id / URL / название раздела и соответствующие ему поиски
with open(results, 'w') as f:
    i = 0
    for dir_tuple, query_freq_list in query_dict.items():
        dir_id = dir_tuple[0]
        dir_name = dir_tuple[1]
        dir_url = dir_tuple[2]
        f.write(f'{dir_name} | {dir_url} | {dir_id}\n')
        f.write(f'{"-"*50}\n')
        for query_freq_tuple in query_freq_list:
            query = query_freq_tuple[0]
            freq = query_freq_tuple[1]
            f.write(f'{query}\t{freq}\n')
        f.write('\n'*2)
