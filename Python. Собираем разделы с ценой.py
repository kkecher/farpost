#!/usr/bin/env python3

'''
Из списка урлов разделов оставляет только  те, в которых есть цена
Вход: список урлов разделов, полученных через «Python. Чтение структуры разделов из JSON.py», вида:
0	Фарпост	https://www.farpost.ru
4	Авто и мото	https://www.farpost.ru/auto
12	Продажа легковых автомобилей	https://www.farpost.ru/auto/sale

Выход: урезанный список только с разделами, в которых есть цена
'''

import requests
import re

#dir_file = input('Enter URL file: ')
#results = input('Enter results file: ')
dir_file = 'Вакансии. Список разделов.txt'
results = 'res'
print()

with open (dir_file, 'r') as f:
    dir_list = []
    for line in f:
        line = line.strip()
        dir_tuple = tuple(line.split('\t'))
        dir_list.append(dir_tuple)

dir_with_price_list = []
i = 1
for elem in dir_list:
    print(f'Doing {i} of {len(dir_list)} line')
    url = elem[2]
    source = requests.get(url)
    if 'data-url-label="cena"' in source.text:
        dir_with_price_list.append(elem)
    i += 1

with open (results, 'w') as f:
    for elem in dir_with_price_list:
        f.write(f'{elem[0]}\t{elem[1]}\t{elem[2]}\n')
