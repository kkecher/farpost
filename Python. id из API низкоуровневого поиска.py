#!/usr/bin/env python3

'''
Собирает id объявлений из API низкоуровневого поиска. API отдает максимум 50000 записей. Решил, что буду собирать сразу отдельно объявления и товары, чтобы не усложнять логику. Если даже с таким делением предложений больше 50000, то идем по всем городам.
Вход: URL низкоуровневого поиска (обычного, НЕ API)
Выход: файл со списком id
Note: указываем максимум 100 вводов на страницу, иначе прибежит Турчанов и даст пизды (очень много памяти сервера требуется, чтобы выгружать по 5000 вводов, и админы начинают нервничать)
'''

import urllib.request
import json
import re
import timeit

search_url = input('Введите URL низкоуровневого поиска: ')
print()
results = input('Введите файл с результатами: ')
print()

start_time = timeit.default_timer()

ids_list = [] #список с id

#выделяем из search_url URL для API низкоуровневого поиска
query_list = re.search(r'^.*&(query=.*)&sort=', search_url, flags=re.IGNORECASE)
URL_query = query_list.group(1)

#загружаем id городов с внешнего файла
city_id_file = 'd:\OneDrive\Документы\Фарпост\Archive\Города. id.txt'
with open(city_id_file, 'r') as f:
    city_id_list = f.read().splitlines()

def get_url_count(type_param='', city_param=''):
    '''
    Получаем число предложений для введенного URL'а. Если их >50000, то будем собирать каунты по городам.
    Вход: URL_query=часть URL'а с параметрами поиска; type_param=bulletin или good; city_param=город, если идем по городам или указали город в поиске
    Выход: число предложений для указанного поиска
    Note: нет, выделить id раздела и вставлять его сюда нельзя. Так как может быть нужно обрабатывать команды, которые содержат не только directoryId.
    '''
    URL_part_1 = 'http://search-actual.srv.loc/rest/v1.4/count'
    URL_part_2 = '/?' + URL_query
    URL_part_3 = '%20and%20type=' + str(type_param)
    URL_part_4 = '%20and%20cityId=' + str(city_param)
    URL_part_5 = '&sort=&zone=default'
    if type_param == '':
        URL_part_3 = ''
    if city_param == '':
        URL_part_4 = ''
    count_api_url = URL_part_1 + URL_part_2 + URL_part_3 + URL_part_4 + URL_part_5
    source_page_for_count = urllib.request.urlopen(count_api_url)
    count = int(source_page_for_count.read())
    return(count)

def get_dir_ids(count, type_param='', city_param=''):
    '''
    Собирает id из API низкоуровневого поиска с учетом типа
    Вход: URL_query=часть URL'а с параметрами поиска; type_param=bulletin или good; city_param=город, если идем по городам или указали город в поиске; count=число предложений для указанного набора параметров поиска
    Выход: список id
    Note: я специально НЕ написал дефолтное значение для каунт, чтобы не забыть его пересчитать для очередного if
    '''
    itemsPerPage = 100 #изначально сделал 10000, но периодически вылетала ошибка. Потом сделал 5000, но админы сказали свое фи. Безопасное число = 100.
    URL_part_1 = 'http://search-ui.srv.loc/api/search?agentId=&attributes=&clientId=&command=undefined&facetingAttributes=&filter=&itemsPerPage='
    URL_part_2 = str(itemsPerPage)
    URL_part_3 = '&pageNumber='
    #URL_part_4 = str(page_iter) #НЕ используется никогда; тут просто показал, что в этой части должен быть номер страницы
    URL_part_5 = '&' + URL_query
    URL_part_6 = '%20and%20type=' + str(type_param)
    URL_part_7 = '%20and%20cityId=' + str(city_param)
    URL_part_8 = '&sort=&zone=default'
    if type_param == '':
        URL_part_6 = ''
    if city_param == '':
        URL_part_7 = ''
    ids_list = []
    total_page_count = count // itemsPerPage + 1
    if total_page_count > 50000 / itemsPerPage: #если количество предложений на всех страницах > 50000, то оставляем только первые страницы с 50000 предложений, так как админка больше не отдает
        total_page_count = 50000 / itemsPerPage
        print('total_page_count') #debug
    for page_iter in range(total_page_count):
        page_iter+=1
        print(f'Doing page {page_iter} of {total_page_count}')
        id_api_url = URL_part_1 + URL_part_2 + URL_part_3 + str(page_iter) + URL_part_5 + URL_part_6 + URL_part_7 + URL_part_8
        try:
            temp_ids_byte = urllib.request.urlopen(id_api_url)
            temp_ids_str = temp_ids_byte.read().decode('utf-8')
            temp_ids_dict = json.loads(temp_ids_str)
            temp_ids_list = temp_ids_dict['documents']
            for id_dict in temp_ids_list:
                id_ = id_dict['id']
                id_ = str(id_)
                if id_[-2:] == '15':
                    id_ = id_[:-2]
                elif id_[-2:] == '06':
                    id_ = '-' + id_[:-2]
                else:
                    id_ = id_ + ' — Who the hell are you??!!!'
                ids_list.append(id_)
        except: #если предложений >50000, то админка выдаст ошибку. В этом случае наши полномочия все, переходим на следующий город.
            break
    with open(results, 'a') as f:
        for id_ in ids_list:
            f.write(f'{id_}\n')
    return(ids_list)

#проверяем, если ли в исходном урле параметр по типу предложения. Если есть, то будем собирать id только для этого типа
if '%20type' in search_url or '&type' in search_url:
    is_contain_type = True
else:
    is_contain_type = False

#проверяем, есть ли в исходном урле параметр по городу. Если есть, то будем собирать id только для этого города
if '%20cityId' in search_url or '&cityId' in search_url:
    is_contain_city = True
else:
    is_contain_city = False

#получаем каунт для исходного урла
if is_contain_type: #если в урле указан type=bulletin or type=good, то собираем предложения только для этого типа
    print('Так-с. Ты сказал собрать id только одного типа. Балуешь ты меня, засранец:)')
    print()
    count = get_url_count()
    if count > 50000:
        print(f'Пидор ты, а не засранец! Тут больше 50000 предложений ({count}). Я пройдусь по городам, но не факт, что соберу ВСЕ id. Ты доволен?!')
        print()
        city_iter = 1
        for city_id in city_id_list:
            count = get_url_count(city_param=city_id)
            print()
            print(f'Doing city {city_iter} of {len(city_id_list)}')
            ids_list += get_dir_ids(city_param=city_id, count=count)
            city_iter+=1
    else:
        print(f'И тут всего лишь {count} id. Ладно, попрошу тебя оставить моим рабом, когда будет революция^_^')
        print()
        ids_list += get_dir_ids(count=count)
elif is_contain_city: #если в урле указан город, то собираем предложения только для этого города
    #считаем количество предложений и собираем id для type=bulletin
    print(f'Ой, хозяин сказал Добби собрать только конкретный город! Какой добрый хозяин. Я запомню твою доброту, и убью быстро')
    print()
    count = get_url_count(type_param='bulletin')
    if count>50000:
        print(f'AHHHGR! Тут больше 50000 предложений ({count}). Я буду вытягивать из тебя по одному сухожилию! Ъъъъууууъъъ, cъуко. Я смогу собрать только 50000 id объявлений для этого города:(')
        print()
    ids_list += get_dir_ids(type_param='bulletin', count=count)

    #считаем количество предложений и собираем id для type=good
    count = get_url_count(type_param='good')
    if count>50000:
        print(f'Оу, тут больше 50000 предложений ({count}). Я смогу собрать только 50000 id товаров для этого города:(')
        print()
    ids_list += get_dir_ids(type_param='good', count=count)
else:
    print('Сначала соберем id объявлений.')
    count = get_url_count('bulletin')
    if count > 50000:
        print(f'Оу, тут больше 50000 предложений ({count}). Я пройдусь по городам, но не факт, что соберу ВСЕ id.')
        print()
        for city_id in city_id_list:
            ids_list += get_dir_ids(type_param='bulletin', count=count)
    else:
        print(f'Хорошие новости! Тут всего {count} предложений, поэтому я быстро сделаю твою грязную работу и пойду к Бендеру.')
        print()
        ids_list = get_dir_ids(type_param='bulletin', count=count)
    print()
    print('А теперь соберем id товаров')
    count = get_url_count(type_param='good')
    if count > 50000:
        print(f'Так-так-такс. А кто это сделал?? Тут больше 50000 предложений ({count}). Я начинаю понимать Бендера:( Ok, я пройдусь по городам, но не факт, что соберу ВСЕ id. Ты доволен, кожаный ублюдок?')
        print()
        city_iter = 1
        for city_id in city_id_list:
            count = get_url_count(city_param=city_id)
            print()
            print(f'Doing city {city_iter} of {len(city_id_list)}')
            ids_list += get_dir_ids(type_param='good', count=count)
            city_iter+=1
    else:
        print(f'Ах. Я люблю тебя, кожаный мешок с мясом! Тут всего {count} id. Я их махом соберу.')
        ids_list += get_dir_ids(type_param='good', count=count)

print()
stop_time = timeit.default_timer()
program_time = stop_time-start_time
program_time_hour = int(program_time // 3600)
program_time_min = int((program_time - program_time_hour*3600) // 60)
program_time_sec = int(round(program_time - program_time_min*60 - program_time_hour*3600))
print('I have finished your dirty wish.')
print(f'It took {program_time_hour}:{program_time_min}:{program_time_sec} of my life, silly bastard!') 
print()
