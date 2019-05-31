#!/usr/bin/env python3

'''
Собирает ответы сервера и конечные URL'ы редиректов
Вход: файл со списком URL'ов
Выход: файл с исходным списком URL'ов, ответами сервера, конечными URL'ами редиректов
В МОЕМ СПИСКЕ ГОРОДОВ city_url НЕТ РЕГИОНОВ, ПОЭТОМУ УРЛЫ С РЕГИОНАМИ ПРЕВРАЩАЮТСЯ ВО ВСЮ РОССИЮ. С ЭТИМ НУЖНО ЧТО-ТО СДЕЛАТЬ, НО ТЕКУЩУЮ ЗАДАЧУ Я ПОЧТИ ЗАКОНЧИЛ, ПОЭТОМУ ЗАБИВАЮ.
'''

import urllib.request
import re

urls_file = input('Enter file with URL\'s: ')
results = input('Enter results file: ')
print()

#загружаем список городов farpost.ru из стороннего файла. Нужно, чтобы не дописывать city=0 в урлы, где есть город (иначе нас отправляет в город по IP). Да-да, даже с указанным городом в урле
with open('city_url', 'r') as city:
    city_list=city.read().splitlines()

def collect_response_from_file(urls_file):
    '''
    Собирает ответы сервера и конечные URL'ы редиректов
    Вход: файл со списком URL'ов
    Выход: файл с исходным списком URL'ов, ответами сервера, конечными URL'ами редиректов
    '''
    responses_string = 'URL\tCode\tLast URL\n' #записываем в строку заголовок будущего файла
    i = 1
    cyr_world = ''
    is_cyr = 0
    new_url = ''

    #загружаем файл с урлами
    with open(urls_file, 'r', encoding='utf-8') as f:
        url_list = f.read().splitlines()

    print('Found ' + str(len(url_list)) + ' URLs')
    print('Результаты будут выведены в файл «' + str(results) + '»')
    print()

    #кодируем кириллицу в URL-формат, иначе выпадает ошибка
    for url in url_list:
        for letter in url:
            if ord(letter) in range(1040,1104):
                cyr_world+=letter
                is_cyr = 1
            elif is_cyr == 1:
                cyr_world = urllib.parse.quote(cyr_world)
                new_url+=cyr_world+letter
                is_cyr=0
                cyr_world=''
            else:
                new_url+=letter
        if is_cyr == 1:
            cyr_world = urllib.parse.quote(cyr_world)
            new_url+=cyr_world
            is_cyr=0
            cyr_world=''
        url=new_url
        new_url = ''

        #если в урле нет города, то в конец урла подставляем city=0, чтобы нас не перекидывало в город по IP
        city_url_list = re.findall('(?:farpost|drom).ru(\/.*?\/)', url)
        if len(city_url_list) == 0: #если предыдущая регулярка вернула [], то вставляем в переменную city_url любое значение, не равное городу (я вставил «no_city»)
            city_url = 'no_city'
        else:
            city_url = city_url_list[0]
        if city_url not in city_list:
            if '/?' in url: #Фарпост начал по-умолчанию отправлять в город, который определился по ip, то есть Владивосток. Этот костыль это лечит и возвращает «Всю Россию»
                url += '&city=0'
            else:
                url += '?city=0'

        #получаем ответ сервера и конечный урл редиректов
        print('Doing URL ' + str(i) + ' of ' + str(len(url_list)))
        try: #try-except нужны, если страница отдает 404 — в этом случае вылетает ошибка
            source_page_for_response = urllib.request.urlopen(url)
            response_code = source_page_for_response.getcode()
            last_redirect_url = source_page_for_response.geturl()
            url = url.replace('?city=0', '')
            url = url.replace('&city=0', '')
            last_redirect_url = last_redirect_url.replace('?city=0', '')
            last_redirect_url = last_redirect_url.replace('&city=0', '')
            if url!=last_redirect_url:
                response_code='30x'
            responses_string += str(url) + '\t' + str(response_code) + '\t' + str(last_redirect_url) + '\n'
            i+=1
        except:
            responses_string += str(url) + '\t' + '404?' + '\t' + 'АХТУНГ' + '\n'
            i+=1
    return(responses_string)

responses_string = collect_response_from_file(urls_file)

with open(results, 'w') as f:
    for response in responses_string:
        f.write(response)
