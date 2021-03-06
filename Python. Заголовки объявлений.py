#!/usr/bin/env python3

'''
Собирает заголовки объявлений из вьюдира
Вход: URL вьюдира или файл с URL'ами
Выход: файл со списком заголовков

Нужно помнить, что farpost.ru отдает максимум 180 страниц вьюдира. Если объявлений >9000, то их нужно разбить на части (например, на объявления и гудсы)
Объявления — параметр ?type=bulletin
Гудсы — параметр ?type=good
'''

import urllib.request
import re

mode = input('Enter viewdir URL or file: ')
results = input('Enter results file: ')
print()

def collect_titles():
    '''
    Собирает заголовки объявлений из вьюдира
    Вход: URL вьюдира
    Выход: список из заголовков
    '''
    dir_url = mode
#    if '/?' in dir_url: #Фарпост начал по-умолчанию отправлять в город, который определился по ip, то есть Владивосток. Этот костыль это лечит и возвращает «Всю Россию»
#        dir_url += '&city=0'
#    else:
#        dir_url += '?city=0'
    i = 1
    titles_list_raw = []
    titles_list = []

    source_page_for_page_total = urllib.request.urlopen(dir_url) #получаем количество вьюбулов для расчета количества страниц
    for line in source_page_for_page_total:
        viewbul_count_list = re.findall('itemsCount.*data-count="(.*?)"', line.decode('cp1251'))
        if viewbul_count_list != []:
            viewbul_count = viewbul_count_list[0]
            break
    viewbul_count = int(viewbul_count_list[0])
    page_total = (viewbul_count // 50) + 1 #получаем число страниц через (целочисленное деление + 1)
    print(f'Found {page_total} pages')
    if page_total > 180:
        page_total = 180
        print()
        print('DOING FIRST 180 PAGES')
    print(f'Results will be written in file «{results}»')
    print()

    while i <= page_total:
        print(f'Doing page {i} of {page_total}')
        if '/?' in dir_url:
            source_page_for_titles = urllib.request.urlopen(dir_url + '&page=' + str(i))
        else:
            source_page_for_titles = urllib.request.urlopen(dir_url + '?page=' + str(i))
        for line in source_page_for_titles:
            titles_list_raw += re.findall('data-stat="\d+">(.*?)</a>', line.decode('cp1251'))
            if 'Возможно, вам также могут подойти следующие предложения' in line.decode('cp1251'):
                break
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

def collect_titles_from_file():
    '''
    Собирает заголовки объявлений из URL-ов в файле
    Вход: текстовый файл 
    Выход: список из заголовков
    '''
    titles_file = mode
    titles_list_raw = []
    titles_list = []
    i = 1
    with open(titles_file, 'r') as f:
        url_list = f.readlines()
    print(f'Found {len(url_list)} URLs')
    print(f'Результаты будут выведены в файл «{results}»')
    print()
    for dir_url in url_list:
        print(f'Doing URL {i} of {len(url_list)}')
        source_page_for_titles = urllib.request.urlopen(dir_url)
        for line in source_page_for_titles:
            title = re.findall('data-field="subject" class="inplace.*">(.*?)<nobr>', line.decode('cp1251'))

            if title != []:
                break
        if title == []:
            titles_list_raw += [dir_url]
        else:
            titles_list_raw += title
        i+=1
    for title in titles_list_raw:
        title = title.replace('&quot;','"')
        title = title.replace('&amp;','&')
        title = title.replace('&shy;','')
        title = title.replace('&gt;','>')
        title = title.replace('&#039;','\'')
        titles_list.append(title)
    return(titles_list)

if 'http' in mode:
    titles_list = collect_titles()
else:
    titles_list = collect_titles_from_file()

with open(results, 'w') as f:
    for title in titles_list:
        f.write(f'{title}\n')
