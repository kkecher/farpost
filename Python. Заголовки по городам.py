#!/usr/bin/env python3

'''
Собирает заголовки объявлений из вьюдира по городам. За счет прохождения по отдельным городам дает гораздо больше заголовков, чем при простом обходе по всей России
Вход: URL вьюдира
Выход: файл со списком заголовков

Нужно помнить, что farpost.ru отдает максимум 180 страниц вьюдира. Если объявлений >9000, то их нужно разбить на части (например, на объявления и гудсы)
Объявления — параметр ?type=bulletin
Гудсы — параметр ?type=good
'''

import urllib.request
import re

dir_url = input('Enter viewdir URL or file: ')
results = input('Enter results file: ')

#загружаем урлы городов с внешнего файла
city_file = 'd:\OneDrive\Документы\Фарпост\Archive\Города. URL\'ы.txt'
with open(city_file, 'r') as f:
    city_list = f.readlines()

open(results, 'w').close()


def collect_titles(city_url):
    '''
    Собирает заголовки объявлений из вьюдира
    Вход: URL вьюдира
    Выход: список из заголовков
    '''
    i = 1
    titles_list_raw = []
    titles_list = []
    #получаем количество вьюбулов для расчета количества страниц
    source_page_for_page_total = urllib.request.urlopen(city_url)
    for line in source_page_for_page_total:
        viewbul_count_list = re.findall('itemsCount.*data-count="(.*?)"', line.decode('cp1251'))
        if viewbul_count_list != []:
            viewbul_count = viewbul_count_list[0]
            break
    if viewbul_count_list == []:
        titles_list = []
        return(titles_list)
    viewbul_count = int(viewbul_count_list[0])
    page_total = (viewbul_count // 50) + 1 #считаем количество страниц через (целочисленное деление + 1)
    if page_total > 1:
        print('Found ' + str(page_total) + ' pages')
    if page_total > 180:
        page_total = 180
        print()
        print('DOING FIRST 180 PAGES')
        print()

    while i <= page_total:
        print('Doing page ' + str(i) + ' out of ' + str(page_total))
        if '/?' in city_url:
            source_page_for_titles = urllib.request.urlopen(city_url + '&page=' + str(i))
        else:
            source_page_for_titles = urllib.request.urlopen(city_url + '?page=' + str(i))
        for line in source_page_for_titles:
            titles_list_raw += re.findall('.html.*?>(.*?)</a>', line.decode('cp1251'))
        for title in titles_list_raw:
            if 'img' not in title:
                title = title.replace('&quot;','"')
                title = title.replace('&amp;','&')
                title = title.replace('&shy;','')
                title = title.replace('&gt;','>')
                title = title.replace('&#039;','\'')
                titles_list.append(title)
        i+=1
        titles_list_raw = []
    return(titles_list)

city_list = city_list[:] #если случилась неожиданность и программа вылетела с ошибкой, то мы можем стартовать с города, где остановились. Здесь определяем номер строки, с которой нужно продолжить
print()
print('OK, MY FRIEND. WE HAVE LONG-LONG ROAD BETWEEN ' + str(len(city_list)) + ' CITIES')
print()
city_num = 1
with open(results, 'a') as f:
    for city in city_list:
        print()
        city = city[22:-1] #удаляем фразу 'https://farpost.ru' из начала строки и '\n' с конца строки
        print('City ' + str(city_num) + ' of ' + str(len(city_list)) + '. Ladies and gentlemen, our horse in ' + city + ' now. Have a good day.')
        city_url = dir_url[:22] + city + dir_url[23:]
        titles_list = collect_titles(city_url)
        if titles_list == []:
            next
        for title in titles_list:
            f.write(title + '\n')
        city_num += 1
