#!/usr/bin/env python3

'''
Собирает список id объявлений
Вход: URL вьюдира
Выход: файл с id-шниками объявлений

Нужно помнить, что farpost.ru отдает максимум 180 страниц вьюдира. Если объявлений >9000, то их нужно разбить на части (например, на объявления и гудсы).
Объявления — параметр ?type=bulletin
Гудсы — параметр ?type=good
'''

import urllib.request
import re

dir_url = input('Enter viewdir URL: ')
result = input('Enter result file: ')

#if '/?' in dir_url: #farpost начал по-умолчанию отправлять в город, который определился по ip, то есть Владивосток. Этот костыль это лечит и возвращает «Всю Россию»
#    dir_url += '&city=0'
#else:
#    dir_url += '?city=0'

def collect_bulletins_id():
    '''
    Собирает список id объявлений
    Вход: URL вьюдира
    Выход: список с id-шниками объявлений
    '''
    i = 1
    bulletins_id_list = []
    source_page_for_page_total = urllib.request.urlopen(dir_url) #получаем количество вьюбулов, чтобы посчитать количество страниц
    for line in source_page_for_page_total:
        viewbul_count_list = re.findall('itemsCount.*data-count="(.*?)"', line.decode('cp1251'))
        if viewbul_count_list != []:
            viewbul_count = viewbul_count_list[0]
            break
    viewbul_count = int(viewbul_count_list[0])
    page_total = (viewbul_count // 50) + 1 #получаем количество страниц через (целочисленное деление + 1)
    print()
    print(f'Found {page_total} pages')
    if page_total > 180:
        page_total = 180
        print()
        print('DOING FIRST 180 PAGES')
    print('Results will be written in file «' + str(result) + '»')
    print()

    while i <= page_total:
        print(f'Doing page {i}')
        if '/?' in dir_url:
            source_page_for_id = urllib.request.urlopen(dir_url + '&page=' + str(i))
        else:
            source_page_for_id = urllib.request.urlopen(dir_url + '?page=' + str(i))
        for line in source_page_for_id:
            bulletins_id_list += re.findall('data-bulletin-id="(\d+)', line.decode('cp1251')) #получаем id частного объявления
            bulletins_id_list += re.findall('data-bulletin-id="(-\d+)', line.decode('cp1251')) #получаем id гудса
            if 'Возможно, вам также могут подойти следующие предложения' in line.decode('cp1251'):
                break
        i+=1
    return(bulletins_id_list)

bulletins_id_list = collect_bulletins_id()

with open(result, 'w') as f:
    for bulletin_id in bulletins_id_list:
        f.write(f'{bulletin_id} \n')
