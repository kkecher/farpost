'''
Собирает список id объявлений из списка лемм в разделе «Сотовые телефоны»
Вход: файл со списком лемм
Выход: файл  с id-шниками объявлений

Нужно помнить, что farpost.ru отдает максимум 180 страниц вьюдира. Если объявлений >9000, то их нужно разбить на части (например, на объявления и гудсы).
Объявления — параметр ?type=bulletin
Гудсы — параметр ?type=good
'''

import urllib.request
import re

file_model = input('Enter file with models: ')
result = input('Enter result file: ')

with open(file_model, 'r') as f:
    list_model = f.read().splitlines()

open(result, 'w').close()

def collect_bulletins_id(model):
    '''
    Собирает список id объявлений
    Вход: URL вьюдира
    Выход: список с id-шниками объявлений
    '''
    i = 1
    url_model = 'https://www.farpost.ru/tech/communication/cellphones/+/' + str(model)
    bulletins_id_list = []
    
    source_page_for_page_total = urllib.request.urlopen(url_model) #получаем количество вьюбулов, чтобы посчитать количество страниц
    for line in source_page_for_page_total:
        viewbul_count_list = re.findall('itemsCount.*data-count="(.*?)"', line.decode('cp1251'))
        if viewbul_count_list != []:
            viewbul_count = viewbul_count_list[0]
            break
    try:
        viewbul_count = int(viewbul_count_list[0])
    except:
        print('АХТУНГ')
        bulletins_id_list.append(model + ' - АХТУНГ!!!')
        return(bulletins_id_list)
    page_total = (viewbul_count // 50) + 1 #получаем количество страниц через (челочисленное деление + 1)
    print()
    print('Found ' + str(page_total) + ' pages')
    print('Results will be written in file «' + str(result) + '»')
    print()

    while i <= page_total:
        print('Doing page ' + str(i))
        source_page_for_id = urllib.request.urlopen(url_model + '?page=' + str(i))
        for line in source_page_for_id:
            bulletins_id_list += re.findall('data-bulletin-id="(\d+)', line.decode('cp1251')) #получаем id для частных объявлений
            bulletins_id_list += re.findall('data-bulletin-id="(-\d+)', line.decode('cp1251')) #получаем id для гудсов
        i+=1
    return(bulletins_id_list)

for model in list_model:
    print()
    print('***************************************')
    print(model.upper())
    print('***************************************')
    model = model.replace(' ','+')
    bulletins_id_list = collect_bulletins_id(model)
    with open(result, 'a') as f:
        for bulletin_id in bulletins_id_list:
            f.write(bulletin_id + '\n')
