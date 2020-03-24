#!/usr/bin/env python3

'''
Собирает имена и их синонимы из peoplenames.ru
Вход: исходный URK
Выход: список имен и их URL'ов
'''

import requests
import re

#url_list = input('Enter file with URLs: ')
#result = input('Enter result file: ')

url_template = 'http://peoplenames.ru/male?page='
result = 'res_peoplename_men'

i = 1
with open (result, 'w') as f:
    for i in range(1, 469):
        temp_names = []
        print (f'Doing {i} of 468 urls')
        url = url_template + str(i)
        source_code = requests.get(url)
        source_code = source_code.text
        names = re.findall(r'(<a href="|"sex__names__name">)(.*?)(?:"|<|>)', source_code)
        for elem in names:
            if '/name/' in elem[1]:
                temp_names.append(str(elem[1]))
            if 'sex__names__name' in elem[0]:
                temp_names.append(str(elem[1]))
        for elem in temp_names:
            f.write(str(elem) + '\n')
