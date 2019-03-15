'''
Собирает список id продавцов
Вход: URL вьюдира или файл с URL-ами
Выход: файл с записями вида «URL объявления : Продавец»

Для ускорения процесса рекомендуется файл с URL-ами разделить на несколько и запускать процессы параллельно
'''

import urllib.request
import re

mode = input('Enter viewdir URL or file with bulletin ids: ')
result_file = input('Enter result file: ')

def collect_bulletins_url(): #срабатывает, если в mode был введен URL
    '''
    Собирает список id объявлений
    Вход: URL вьюдира
    Выход: список с URL-ами объявлений
    '''
    i = 1
    bulletins_id_list = []
    bulletins_url_list = []

    source_page_for_page_total = urllib.request.urlopen(dir_url) #получаем число вьюбулов, чтобы посчитать число страниц
    for line in source_page_for_page_total:
        viewbul_count_list = re.findall('itemsCount.*data-count="(.*?)"', line.decode('cp1251'))
        if viewbul_count_list != []:
            viewbul_count = viewbul_count_list[0]
            break
    viewbul_count = int(viewbul_count_list[0])
    page_total = (viewbul_count // 50) + 1 #получаем число страниц через (целочисленное деление + 1)
    print()
    print('Found ' + str(page_total) + ' pages')
    print('Results will be written in file «' + result_file + '»')
    print()

    while i <= page_total:
        print('Doing page ' + str(i))
        if '/?' in dir_url:
            source_page_for_id = urllib.request.urlopen(dir_url + '&page=' + str(i))
        else:
            source_page_for_id = urllib.request.urlopen(dir_url + '?page=' + str(i))
        for line in source_page_for_id:
            bulletins_id_list += re.findall('data-bulletin-id="(\d+)', line.decode('cp1251')) #получаем id частного объявления
            bulletins_id_list += re.findall('data-bulletin-id="(-\d+)', line.decode('cp1251')) #получаем id гудса
        i+=1
    for id_viewbull in bulletins_id_list:
        if '-' in id_viewbull:
            url = 'https://farpost.ru/g' + id_viewbull[1:] + '.html'
        else:
            url = 'https://farpost.ru/' + id_viewbull
        bulletins_url_list.append(url)
    return(bulletins_url_list)

def collect_sellers_id():
    '''
    Собирает список продавцов
    Вход: Список bulletins_url_list, полученный из стороннего файла или из функции collect_bulletins_url
    Выход: словарь вида {<URL>:<id продавца>}
    '''
    print()
    i = 1
    dict_results = {}
    for url in bulletins_url_list:
        try:
            url = url.rstrip() #убираем символы новой строки, чтобы в итоговом файле URL и id продавца были на одной строке
            print('Doing URL ' + str(i) + ' of ' + str(len(bulletins_url_list)))
            source_page = urllib.request.urlopen(url)
            for line in source_page:
                temp_id_list = re.findall('href=\'/user/(.*?)/', line.decode('cp1251')) #временный список для хранения id продавца, найденного в текущем URL
                if temp_id_list != []:
                    dict_results[url] = temp_id_list[0]
                    break
            if temp_id_list == []:
                source_page = urllib.request.urlopen(url) #не знаю почему, но к этому шагу значение source_page, полученное раннее, исчезает. Приходится получать еще раз
                for line in source_page:
                    temp_id_list = re.findall('/user/(.*?)/', line.decode('cp1251'))
                    if temp_id_list != []:
                        dict_results[url] = temp_id_list[0]
                        break
        except:
            dict_results[url] = 'АХТУНГ!!!'
        i += 1
    return(dict_results)

if 'http' in mode: #срабатывает, если в mode был введен URL
    dir_url = mode
    bulletins_url_list = collect_bulletins_url()
    dict_results = collect_sellers_id()
else: #срабатывает, если в mode было введено название файла
    with open(mode, 'r') as f:
        bulletins_url_list = f.read().splitlines()
    dict_results = collect_sellers_id()

with open(result_file, 'w') as f:
    for key, value in dict_results.items():
        f.write(key + ' : ' + value + '\n')
