#!/usr/bin/env python3

'''
КОД РАБОТАЕТ, НО У АДМИНОВ ФАРПОСТА ВЫЛЕЗАЮТ КАКИЕ-ТО ОШИБКИ ПРИ ЕГО СРАБАТЫВАНИИ
Собирает количество вьюбулов по городам и разделам из низкоуровневого поиска
Вход: файлы с id городов, id разделов, названиями городов, названиями разделов (ВАЖНО, чтобы порядок id и названий в файлах совпадал). В res_top5_dict нужно записать фигурные скобки «{}»
Выход: файл с количеством вьюбулов по городам и разделам, файл с ТОП5 городов по разделам
'''

import urllib.request
import json
import natsort
from selenium import webdriver

#city_ids = input('Enter file with cities ids: ')
#city_names = input('Enter file with cities name: ')
#dir_ids = input('Enter file with dirs ids: ')
#dir_names = input('Enter file with dirs names: ')
#res_dir_city = input('Enter res_dir_city file: ')
#res_top5_dict = input('Enter file with dict for top5: ')
#res_top5 = input('Enter file for top5: ')

city_ids = 'city_id'
city_names = 'city_name'
dir_ids = 'dir_id'
dir_names = 'dir_name'
res_dir_city = 'res_dir_city'
res_top5_dict = 'res_top5_dict'
res_top5 = 'res_top5'


#эти части используются при составлении урла для запроса по городу. Если по городу нет предложений, то во все разделы можем сразу записать 0
city_url_part_1 = 'http://search-ui.srv.loc/search?agentId=&attributes=&clientId=&command=StandardSearch&facetingAttributes=&filter=&itemsPerPage=50&pageNumber=1&query=cityId%20%3D%20'
#city_url_part_2 = подставляем переменную city_id
city_url_part_3 = '&sort=&zone=default'

#эти части используются при составлении урла для запроса по разделу. Если по разделу нет предложений, то записываем id раздела в отдельный список и исключаем этот id из списка для сбора каунтов вьюбулов
dir_url_part_1 = 'http://search-ui.srv.loc/search?agentId=&attributes=&clientId=&command=StandardSearch&facetingAttributes=&filter=&itemsPerPage=50&pageNumber=1&query=directoryId%20%3D%20'
#dir_url_part_2 = подставляем переменную dir_id
dir_url_part_3 = '&sort=&zone=default'

#эти части используются при составлении урла для запроса город+раздел
url_part_1 = 'http://search-ui.srv.loc/search?agentId=&attributes=&clientId=&command=StandardSearch&facetingAttributes=&filter=&itemsPerPage=50&pageNumber=1&query=directoryId%20%3D%20'
#url_part_2 = подставляем переменную dir_id
url_part_3 = '%20and%20cityId%20%3D%20'
#url_part_4 = подставляем переменную city_id
url_part_5 = '&sort=&zone=default'


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
    dir_city_dict = json.loads(dir_city_list[0])


#Выключает картинки, но мы не сможем включить stalin
opt = webdriver.ChromeOptions()
opt.add_extension("D:\OneDrive\Документы\Фарпост\Block-image_v1.1.crx")
#browser = webdriver.Chrome(executable_path='/home/arzhanov/Documents/chromedriver', chrome_options=opt) #активировать при работе в Linux, поменять путь к chromedriver при необходимости
browser = webdriver.Chrome(executable_path='D:\OneDrive\Документы\Фарпост\chromedriver.exe', options=opt) #активировать при работе в Windows

#Включаем картинки. Страницы загружаются дольше, но можем включить stalin и поменять ряд других параметров
#browser = webdriver.Chrome(executable_path='/home/arzhanov/Documents/chromedriver') #активировать при работе в Linux, поменять путь к chromedriver при необходимости
#browser = webdriver.Chrome(executable_path='D:\OneDrive\Документы\Фарпост\chromedriver.exe') #активировать при работе в Windows


def wait_for_page_load():
    '''
    Проверяет, загрузилась ли полностью страница
    Вход: ничего
    Выход: дает программе дальнейший ход
    '''
    while True:
        list_table_of_results = browser.find_elements_by_xpath("//*[@class='table search-results']")
        if list_table_of_results != []:
            break
    return()

def count_total():
    '''
    Считает общее число страниц
    Вход: ничего
    Выход: общее число страниц
    '''
    wait_for_page_load()
    total_num_text = browser.find_element_by_xpath("//*[@class='dl-horizontal search-summary-dl']/div/dd")
    total_num_text = total_num_text.text
    total_num_text = total_num_text.replace(' ', '')
    total_num = int(total_num_text)
    return(total_num)

def dir_clean(dir_id_list, dir_name_list):
    '''
    Собирает каунты по разделам. id и названия пустых разделов записывает в отдельный список и удаляет их из списков dir_id_list и dir_name_list. Потом для пустых разделов во всех городах запишем 0
    Вход: dir_id_list, dir_name_list
    Выход: empty_dir_id_list, empty_dir_name_list
    '''
    i = 0
    empty_dir_id_list = []
    empty_dir_name_list = []
    for dir_id in dir_id_list:
        search_url = dir_url_part_1 + str(dir_id) + dir_url_part_3
        browser.get(search_url)
        wait_for_page_load()
        total_num = count_total()
        if total_num == 0:
            empty_dir_id_list.append(dir_id)
            empty_dir_name_list.append(dir_name_list[i])
            del dir_id_list[i]
            del dir_name_list[i]
        i+=1
    len_empty_dir_list = len(empty_dir_id_list)
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
        dir_iter+=1
    dir_iter = 0 #итератор для записывания в файл id раздела рядом с его названием. Это не дубль, это нужно!
    for empty_dir_name in empty_dir_name_list: #продолжаем записывать в заголовок файла разделы, в которых нет предложений ни в каких городах
        f.write('\t' + str(empty_dir_name) + ' (' + str(dir_id_list[dir_iter]) + ')')
        dir_iter+=1
    f.write('\n') #закончили записывать заголовок файла
    city_iter = 0
    step_iter = 1
    len_city_id_list = len(city_id_list) #считаем длину списка городов, чтобы посчитать общее количество итераций
    len_dir_id_list = len(dir_id_list) #считаем длину списка разделов, чтобы посчитать общее количество итераций
    total_iter = len_city_id_list * len_dir_id_list #считаем общее количество итераций
    len_city_id_list_str = str(len(city_id_list))
    len_dir_id_list_str = str(len(dir_id_list))
    for city_id in city_id_list:
        dir_iter = 0 #обнуляем индекс раздела
        city_name = city_name_list[city_iter]
        f.write(str(city_name)) #записываем название города в первую ячейку

        #проверяем каунт по городу. Если ничего нет, то записываем во все разделы нули и переходим к следующему городу
        search_url = city_url_part_1 + str(city_id) + city_url_part_3
        browser.get(search_url)
        wait_for_page_load()
        total_num = count_total()
        if total_num == 0:
            len_empty_string = len(dir_id_list)
            empty_string = len_empty_string * '\t0'
            f.write(empty_string + '\n')
            continue

        #если в городе каунт не равен нулю, то проходим по всем разделам для этого города и собираем каунты
        for dir_id in dir_id_list:
            print('Doing ' + str(step_iter) + ' of ' + str(total_iter))
            dir_city_dict = collect_dir_city_dict(dir_city_dict)
            search_url = url_part_1 + str(dir_id) + url_part_3 + str(city_id) + url_part_5
            browser.get(search_url)
            wait_for_page_load()
            total_num = count_total()
            f.write('\t' + str(total_num))
            step_iter+=1
            dir_iter+=1
        f.write(len_empty_dir_list * '\t0') #записываем нули для разделов, где ничего нет во всех городах 
        f.write('\n') #прошлись по всем разделам для текущего города, переходим на следующую строку
        with open(res_top5_dict, 'w') as d: #записываем в res_top5_dict текущее состояние словаря разделов с каунтами по городам
            dir_city_json = json.dumps(dir_city_dict, ensure_ascii=False) #переводим словать в JSON для записи в файл
            d.write(dir_city_json)
        city_iter+=1

#записываем в файл ТОП5 городов для каждого раздела
with open (res_top5, 'w') as f:
    for dir_name, city_dict in dir_city_dict.items():
        f.write(str(dir_name) + '\n--------------------------\n')
        i = 0
        while i < 5 and i < len(city_dict):
            for city_name, city_count in natsort.natsorted(city_dict.items(), reverse=True):
                f.write(str(city_name) + ' (' + str(city_count) + ')\n')
                i+=1
        f.write('\n')
