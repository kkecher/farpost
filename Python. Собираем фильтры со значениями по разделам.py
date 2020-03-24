#!/usr/bin/env python3

'''
Собирает все фильтры со значениями, содержащиеся в разделах. Есть мусорные урлы, поэтому потом нужна ручная чистка
Вход: файл со списком разделов, полученный в Python. Собираем URL'ы из API Хьюстона.py
Выход: файл со списком фильтров и значений по разделам
'''

import requests
import re

dirs_file = input('Enter dirs file: ')
result = input('Enter result file: ')

with open(dirs_file, 'r', encoding='utf8') as f:
    dirs_list = f.read().splitlines()

res_dict= {}
i = 1
for dir_url in dirs_list:
    print(f'Doing {i} of {len(dirs_list)}')
    response = requests.get(dir_url)
    filters = re.findall(r'({"name":.*?(?:}}|]}))', response.text)
    res_dict[dir_url] = filters
    i += 1

with open(result, 'w') as f:
    for dir_url, filters in res_dict.items():
        f.write(f'{dir_url}\n{"-"*50}\n')
        for elem in filters:
            f.write(elem + '\n')
        f.write('\n')
