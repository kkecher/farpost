'''
Собирает id городов из URL-ов городов
Вход: список с URL-ами городов на барахолке (например, https://www.farpost.ru/chelyabinsk/)
Выход: список id-шников городов
'''

import urllib.request
import re

city_list = input('Enter file with cities: ')
result = input('Enter result file: ')

with open(city_list, 'r') as f:
    city_list = f.read().splitlines()

open(result, 'w').close()

i = 1
for city in city_list:
    len_city_list = len(city_list)
    print('Doing ' + str(i) + ' of ' + str(len_city_list) + ': ' + city)
    source_page_for_page_total = urllib.request.urlopen(city)
    for line in source_page_for_page_total:
        city_id_list = re.findall('data-city-id="(.*?)"', line.decode('cp1251'))
        if city_id_list != []:
            city_id = city_id_list[0]
            break
    try:
        city_id = int(city_id_list[0])
    except:
        print('АХТУНГ!!!')
        city_id = 'АХТУНГ!!!'
    with open(result, 'a') as f:
        f.write(str(city_id) + '\n')
    i += 1
