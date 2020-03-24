#!/usr/bin/env python3

'''
Собираем статистику локальных поисков за год
Вход: файл в формате: {query}\t{URL, соответствующий query}
Выход: статистика по локальным поискам за год

Кажется, в URL'е захардкожил id раздела. Не помню почему, нужно иметь в виду.
'''

import requests
import json
import timeit
import natsort
import re

start_time = timeit.default_timer()

houston_file = input('Enter query file: ')
results = input('Enter results file: ')
print()

query_url_1 = 'http://query-info.srv.loc/api/regexp?query=%5E'
#query_url_2 = query
query_url_3 = '%24&dirId=1085&withSubDirs=1&cityId=0&from=2019-01-01&to=2019-12-31'


with open(houston_file, 'r', encoding = 'utf8') as f:
    houston_list = f.read().splitlines()

result_list = []
i = 1
for query_url in houston_list:
    print(f'Doing {i} of {len(houston_list)}')
    query_url = query_url.strip()
    query_url = re.sub(r'^\d+\t', '', query_url, flags=re.IGNORECASE)
    query = query_url.split('\t')[0]
    query = query.replace('+', '%5C%2B').replace(' ', '+').replace('.', '%5C.').replace('\\', '%5C%5C')
    url = query_url_1 + query + query_url_3
    response = requests.get(url)
    query_json = json.loads(response.text)
    try:
        freq = query_json['queries'][0]['users']
    except:
        freq = 'АХТУНГ!!! ' + str(url)
    result_list.append((freq, query_url))
    i += 1

with open(results, 'w') as f:
    result_list = natsort.natsorted(result_list, reverse=True) #сортируем фразы по частотности. Использую natsort, так как дефолтная сортировка в натуральную сортировку не умеет
    for elem in result_list:
        freq = elem[0]
        query_url = elem[1]
        f.write(f'{freq}\t{query_url}\n')

stop_time = timeit.default_timer()
program_time = stop_time-start_time
program_time_hour = int(program_time // 3600)
program_time_min = int((program_time - program_time_hour*3600) // 60)
program_time_sec = int(program_time - program_time_min*60 - program_time_hour*3600)

print()
print('I have finished your dirty wish.')
print(f'It took {program_time_hour}:{program_time_min}:{program_time_sec} of my life, silly bastard.')
