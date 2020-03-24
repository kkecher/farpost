#!/usr/bin/env python3

'''
Собирает для указанных регионов вакансии с trudvsem.ru по API
Вход: список регионов в таком формате: 
ДВФО
Амурская область	Благовещенск	2800000000000
Республика Бурятия	Улан-Удэ	0300000000000

СибФО
Республика Алтай	Горно-Алтайск	0400000000000
Алтайский край	Барнаул	2200000000000

Выход: файл со списком вакансий
'''

import requests
import json
import math

#Загружаем список регионов
with open('Выгрузка вакансий. Регионы.txt', 'r', encoding='utf8') as f:
    region_dict = {}
    for line in f:
        line = line.strip()
        if '\t' not in line and line != '':
            region_dict[line] = []
            key = line
        elif '\t' in line:
            region_tuple = tuple(line.split('\t'))
            region_dict[key].append(region_tuple)

def get_vacancy(region_name, region_code):
    '''
    Собираем вакансии для указанного региона
    Вход: имя региона, код региона
    Выход: файл со списком вакансий для региона
    '''
    print()
    print(f'Doing {region_name}')
    with open('res_vac', 'a') as f:
        page = 1
        url_part_1 = 'http://opendata.trudvsem.ru/api/v1/vacancies/region/'
        url_part_2 = region_code
        url_part_3 = '/?offset='
        #url_part_4 = page
        while True:
            try:
                url = url_part_1 + url_part_2 + url_part_3 + str(page)
                response = requests.get(url)
                api_json = json.loads(response.text)
                status = api_json['status']
                count = api_json['meta']['total'] #получаем общее число вакансий
                pages = int(math.ceil(count / 100))
                print(f'Doing {page} of {pages}')
                if page == 1:
                    f.write('\n')
                    f.write(f'{50*"-"}\n')
                    f.write(f'{region_name}: count = {count}\n')
                    f.write(f'{50*"-"}\n')
                f.write(f'{50*"-"}\n')
                f.write(f'URL = {url}\tstatus: {status}\n')
                f.write(f'{50*"-"}\n')
                f.write(f"{api_json['results']['vacancies']}\n") #записываем в файл весь список вакансий
                page += 1
                if page > pages:
                    break
            except:
                print(f'Doing {page} of {pages}')
                print(f'{url}: АХТУНГ!!!')
                if page == 1:
                    f.write(f'{50*"-"}\n')
                    f.write(f'{region_name}: count = {count}\n')
                    f.write(f'{50*"-"}\n')
                f.write(f'{50*"-"}\n')
                f.write(f'URL = {url}\n')
                f.write(f'{50*"-"}\n')
                f.write(f"АХТУНГ!!!\n") #записываем в файл весь список вакансий
                page += 1
                if page > pages:
                    break

for region_federal_district in region_dict:
    region_oblast_list = region_dict[region_federal_district]
    for region_oblast in region_oblast_list:
        region_name = region_oblast[0]
        region_code = region_oblast[2]
        get_vacancy(region_name, region_code)
