#!/usr/bin/env python3

'''
Собирает количество вьюбулов по городам и разделам из API низкоуровневого поиска
Вход: файлы с id городов, id разделов, названиями городов, названиями разделов (ВАЖНО, чтобы порядок id и названий в файлах совпадал).
Выход: файл с количеством вьюбулов по городам и разделам, файл с ТОП5 городов по разделам

Если скрипт завершился с ошибкой и НЕ дошел до конца — БЕЗ ПАНИКИ. Смотрим в терминале, на каком городе случилась ошибка и удаляем в файлах «Города. id.txt» и «Города. Названия.txt» все строки до этого города.

Если нужно запустить скрипт с нуля, то руками очищаем файлы res_dir_city.txt и res_top5_dict.txt
'''

import urllib.request
import json
import natsort

#city_ids = input('Enter file with cities ids: ')
#city_names = input('Enter file with cities name: ')
#dir_ids = input('Enter file with dirs ids: ')
#dir_names = input('Enter file with dirs names: ')
#res_dir_city = input('Enter res_dir_city file: ')
#res_top5_dict = input('Enter file with dict for top5: ')
#res_top5 = input('Enter file for top5: ')

city_ids = 'Города. id.txt'
city_names = 'Города. Названия.txt'
dir_ids = 'Разделы. id.txt'
dir_names = 'Разделы. Названия.txt'
res_dir_city = 'res_dir_city.txt'
res_top5_dict = 'res_top5_dict.txt'
res_top5 = 'res_top5.txt'


#эти части используются при составлении урла для запроса по городу. Если по городу нет предложений, то во все разделы можем сразу записать 0
city_url_part_1 = 'http://search-actual.srv.loc/rest/v1.4/count?zone=default&filter=&query=cityId='
#city_url_part_2 = подставляем переменную city_id

#эти части используются при составлении урла для запроса по разделу. Если по разделу нет предложений, то записываем id раздела в отдельный список и исключаем этот id из списка для сбора каунтов вьюбулов
dir_url_part_1 = 'http://search-actual.srv.loc/rest/v1.4/count?zone=default&filter=&query=directoryId='
#dir_url_part_2 = подставляем переменную dir_id

#эти части используются при составлении урла для запроса город+раздел
url_part_1 = 'http://search-actual.srv.loc/rest/v1.4/count?zone=default&filter=&query=directoryId='
#url_part_2 = подставляем переменную dir_id
url_part_3 = '%20and%20cityId='
#url_part_4 = подставляем переменную city_id


#загружаем данные с файлов
with open (city_ids, 'r', encoding='utf-8') as f:
    city_id_list = f.read().splitlines()

with open (city_names, 'r', encoding='utf-8') as f:
    city_name_list = f.read().splitlines()

with open (dir_ids, 'r', encoding='utf-8') as f:
    dir_id_list = f.read().splitlines()

with open (dir_names, 'r', encoding='utf-8') as f:
    dir_name_list = f.read().splitlines()

with open(res_top5_dict, 'r') as f:
    dir_city_list = f.read().splitlines()
    try:
        dir_city_dict = json.loads(dir_city_list[0])
    except:
        dir_city_list = ['{}']
        dir_city_dict = json.loads(dir_city_list[0])


def get_count(search_url):
    '''
    Вход: URL search_url
    Выход: число предложений по указаному URL'у
    '''
    source_page_for_count = urllib.request.urlopen(search_url)
    count = int(source_page_for_count.read())
    return(count)


def dir_clean(dir_id_list, dir_name_list):
    '''
    Собирает каунты по разделам. id и названия пустых и заполненных разделов разносит в отдельные списки empty_dir и filled_dir. Потом filled_dir копируем в dir_id_list и dir_name_list. Потом для пустых разделов во всех городах запишем 0
    Note: изначально я просто удалял пустые элементы из dir_id_list и dir_name_list, но возникало непрозрачное поведение при итерации по списку, поэтому переделал от греха подальше.
    Вход: dir_id_list, dir_name_list
    Выход: empty_dir_id_list, empty_dir_name_list
    '''
    print ('Исключаем из списка пустые разделы: ')
    i = 0
    number_of_iter = len(dir_id_list)
    empty_dir_id_list = []
    empty_dir_name_list = []
    filled_dir_id_list = []
    filled_dir_name_list = []
    for dir_id in dir_id_list:
        print('Doing ' + str(i+1) + ' of ' + str(number_of_iter))
        search_url = dir_url_part_1 + str(dir_id)
        total_num = get_count(search_url)
        if total_num == 0:
            empty_dir_id_list.append(dir_id)
            empty_dir_name_list.append(dir_name_list[i])
        else:
            filled_dir_id_list.append(dir_id)
            filled_dir_name_list.append(dir_name_list[i])
        i += 1
    dir_id_list = filled_dir_id_list
    dir_name_list = filled_dir_name_list
    len_empty_dir_list = len(empty_dir_id_list)
    print()
    print('Исключено пустых разделов: ' + str(len_empty_dir_list))
    print()
    return(dir_id_list, dir_name_list, empty_dir_id_list, empty_dir_name_list, len_empty_dir_list)

def collect_dir_city_dict(dir_city_dict):
    '''
    Собирает в словарь разделов словарь с городами и каунтами по ним. Нужно, чтобы потом вывести ТОП5 городов по разделам.
    Вход: dir_iter, dir_name_list, city_name, dir_city_dict, total_num
    Выход: dir_city_dict
    '''
    dir_name = dir_name_list[dir_iter]
    if dir_name in dir_city_dict:
        dir_city_dict[dir_name][city_name] = total_num
    else:
        dir_city_dict[dir_name] = {}
        dir_city_dict[dir_name][city_name] = total_num
    return(dir_city_dict)

#очищаем dir_id_list и dir_name_list от пустых разделов, они записываются в отдельные списки и НЕ участвуют в парсинге по городам
dir_id_list, dir_name_list, empty_dir_id_list, empty_dir_name_list, len_empty_dir_list = dir_clean(dir_id_list, dir_name_list)

with open(res_dir_city, 'a', encoding='utf-8') as f:
    f.write('Город') #записываем заголовок файла
    dir_iter = 0 #итератор для записывания в файл id раздела рядом с его названием
    for dir_name in dir_name_list: #продолжаем записывать в заголовок файла разделы, в которых есть предложения хоть в каких-то городах
        f.write('\t' + str(dir_name) + ' (' + str(dir_id_list[dir_iter]) + ')')
        dir_iter += 1
    empty_dir_iter = 0 #итератор для записывания в файл id пустого раздела рядом с его названием
    for empty_dir_name in empty_dir_name_list: #продолжаем записывать в заголовок файла разделы, в которых нет предложений ни в каких городах
        f.write('\t' + str(empty_dir_name) + ' (' + str(empty_dir_id_list[empty_dir_iter]) + ')')
        empty_dir_iter += 1
    f.write('\n') #закончили записывать заголовок файла
    city_iter = 0
    step_iter = 1
    len_city_id_list = len(city_id_list) #считаем длину списка городов, чтобы посчитать общее количество итераций
    len_dir_id_list = len(dir_id_list) #считаем длину списка разделов, чтобы посчитать общее количество итераций
    total_iter = len_city_id_list * len_dir_id_list #считаем общее количество итераций
    len_city_id_list_str = str(len_city_id_list)
    len_dir_id_list_str = str(len_dir_id_list)
    for city_id in city_id_list:
        dir_iter = 0 #обнуляем индекс раздела
        city_name = city_name_list[city_iter]
        city_iter += 1
        f.write(str(city_name) + ' (' + str(city_id) + ')') #записываем название города и его id в первую ячейку
        print('Check city ' + city_name)

        #проверяем каунт по городу. Если ничего нет, то записываем во все разделы нули и переходим к следующему городу
        search_url = city_url_part_1 + str(city_id)
        total_num = get_count(search_url)
        if total_num == 0:
            print('This city is empty, my Lord!')
            print()
            len_empty_string = len_dir_id_list + len(empty_dir_id_list)
            empty_string = len_empty_string * '\t0'
            f.write(empty_string + '\n')
            step_iter += len_dir_id_list #прибавляем к итератору количество разделов, которые считать не пришлось
            continue

        #если в городе каунт не равен нулю, то проходим по всем разделам для этого города и собираем каунты
        for dir_id in dir_id_list:
            print('Doing ' + str(step_iter) + ' of ' + str(total_iter) + ' total steps: city is ' + city_name)
            search_url = url_part_1 + str(dir_id) + url_part_3 + str(city_id)
            total_num = get_count(search_url)
            f.write('\t' + str(total_num))
            dir_city_dict = collect_dir_city_dict(dir_city_dict)
            step_iter += 1
            dir_iter += 1
        print()
        f.write(len_empty_dir_list * '\t0') #записываем нули для разделов, где ничего нет во всех городах 
        f.write('\n') #прошлись по всем разделам для текущего города, переходим на следующую строку
        with open(res_top5_dict, 'w') as d: #записываем в res_top5_dict текущее состояние словаря разделов с каунтами по городам
            dir_city_json = json.dumps(dir_city_dict, ensure_ascii=False) #переводим словать в JSON для записи в файл
            d.write(dir_city_json)

#записываем в файл ТОП5 городов для каждого раздела
with open (res_top5, 'w') as f:
    for dir_name, city_dict in dir_city_dict.items():
        f.write(str(dir_name) + '\n' + 30*'-' + '\n')
        city_list_sorted = natsort.natsorted(city_dict.items(), key=lambda kv: kv[1], reverse=True) #получили список кортежей, отсортированный в обратном порядке
        i = 0
        for city_tuple in city_list_sorted:
            if i >= 5 or i > len(city_dict):
                break
            city_name = city_tuple[0]
            city_count = city_tuple[1]
            f.write(str(city_name) + ' (' + str(city_count) + ')\n')
            i += 1
        f.write('\n')

print()
print('I\'ve done your dirty job, old bastard!')
print()
print('Results is in files: ')
print('— Табличка с каунтами по разделам и городам (делитель - tab): ' + str(res_dir_city))
print('— Файлик с ТОП5 городов по разделам: ' + str(res_top5))
print('— Служебный файл на случай, если скрипт сбойнет: ' + str(res_top5_dict))
