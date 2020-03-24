#!/usr/bin/env python3

'''
Собирает ответы сервера и конечные URL'ы редиректов
Вход: файл со списком URL'ов
Выход: файл с исходным списком URL'ов, ответами сервера, конечными URL'ами редиректов
'''

import urllib.parse
import requests
import re

urls_file = input('Enter file with URL\'s: ')
results = input('Enter results file: ')
print()

def collect_response_from_file(urls_file):
    '''
    Собирает ответы сервера и конечные URL'ы редиректов
    Вход: файл со списком URL'ов
    Выход: файл с исходным списком URL'ов, ответами сервера, конечными URL'ами редиректов
    '''
    responses_string = 'URL\tCode\tLast URL\n' #записываем в строку заголовок будущего файла
    i = 1

    #Загружаем файл с урлами
    try:
        with open(urls_file, 'r', encoding = 'utf8') as f:
            url_list = f.read().splitlines()
    except:
        with open(urls_file, 'r', encoding = 'cp1251') as f:
            url_list = f.read().splitlines()

    print('Found ' + str(len(url_list)) + ' URLs')
    print('Результаты будут выведены в файл «' + str(results) + '»')
    print()

#    #Кодируем кириллицу в URL-формат, иначе выпадает ошибка. По буквам, потому что иначе спецсимволы превращаются в тыкву.
#UPD 06.11.2019: есть гипотеза, что достаточно указать кодировку при открытии файла, и трансформации больше никакие не нужны. Проверить при следующем использовании.
    for url in url_list:
#        url = url.replace('ё', 'е')
#        is_cyr = 0
#        new_url = ''
#        cyr_world = ''
#        for letter in url:
#            if ord(letter) in range(1040,1104):
#                cyr_world += letter
#                is_cyr = 1
#            elif is_cyr == 1:
#                cyr_world = requests.compat.quote_plus(cyr_world.encode('utf8'))
#                new_url += cyr_world+letter
#                is_cyr = 0
#                cyr_world = ''
#            else:
#                new_url += letter
#        if is_cyr == 1:
#            cyr_world = urllib.parse.quote(cyr_world)
#            new_url += cyr_world
#            cyr_world = ''
#        url = new_url


        #Получаем ответ сервера и конечный урл редиректов
        print('Doing URL ' + str(i) + ' of ' + str(len(url_list)))
        try: #try/except нужны, если страница отдает 404 — в этом случае вылетает ошибка
            response = requests.get(url)
            response_code = response.status_code
            last_redirect_url = response.url
            if url != last_redirect_url:
                response_code = '30x'
            responses_string += str(url) + '\t' + str(response_code) + '\t' + str(last_redirect_url) + '\n'
            i += 1
        except Exception:
            responses_string += str(url) + '\t' + '404?' + '\t' + 'АХТУНГ' + '\n'
            i += 1
    return(responses_string)

responses_string = collect_response_from_file(urls_file)

with open(results, 'w') as f:
    for response in responses_string:
        f.write(response)
