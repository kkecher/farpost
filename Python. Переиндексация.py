#!/usr/bin/env python3

'''
Переиндексирует объявления и URL-ы
Вход: URL вьюдира или файл «id_file» с id-шниками (перед id гудса должен быть дефис)
Выход: ничего (переиндексированные объявления)

Нужно помнить, что farpost.ru отдает максимум 180 страниц вьюдира. Если объявлений >9000, то их нужно разбить на части (например, на объявления и гудсы)
Объявления — параметр ?type=bulletin
Гудсы — параметр ?type=good
'''

import urllib.request
import re
import timeit
from selenium import webdriver

mode = input('Enter viewdir URL or file with bulletin ids: ')

if 'http' in mode:
        if '/?' in mode: #Фарпост начал по-умолчанию отправлять в город, который определился по ip, то есть Владивосток. Этот костыль это лечит и возвращает «Всю Россию»
            mode += '&city=0'
        else:
            mode += '?city=0'

def collect_bulletins_id():
    '''
    Собирает id объявлений из вьюдира для переиндексации
    Вход: URL вьюдира
    Выход: список с URL-ами переиндексации
    '''
    dir_url = mode
    i = 1
    id_list = []
    url_list = []

    source_page_for_page_total = urllib.request.urlopen(dir_url) #получаем количество вьюбулов для расчета количества страниц
    for line in source_page_for_page_total:
        viewbul_count_list = re.findall('itemsCount.*data-count="(.*?)"', line.decode('cp1251'))
        if viewbul_count_list != []:
            viewbul_count = viewbul_count_list[0]
            break
    viewbul_count = int(viewbul_count_list[0])
    page_total = (viewbul_count // 50) + 1 #получаем количество страниц через (целочисленное деление + 1)
    print('1 of 2. Collecting bulletins id…')
    print(f'Found {page_total} pages')
    if page_total > 180:
        page_total = 180
        print()
        print('DOING FIRST 180 PAGES')
        print()
    
    while i <= page_total:
        print(f'Doing page {i} of {page_total}')
        if '/?' in dir_url:
            source_page_for_id = urllib.request.urlopen(dir_url + '&page=' + str(i))
        else:
            source_page_for_id = urllib.request.urlopen(dir_url + '?page=' + str(i))
        for line in source_page_for_id:
            id_list += re.findall('data-bulletin-id="(-?\d+)', line.decode('cp1251'))
        i+=1
    for bulletin_id in id_list:
        if '-' in bulletin_id:
            url_list.append('https://www.farpost.ru/admin/update-index-attributes/good/' + bulletin_id[1:])
        else:
            url_list.append('https://www.farpost.ru/admin/update-index-attributes/bulletin/' + str(bulletin_id))
    return(url_list)

def collect_bulletins_id_from_file():
    '''
    Собирает id объявлений из файла id_file
    Вход: файл «id_file» (перед id гудсов должен стоять дефис)
    Выход: список в URL-ами переиндексации
    '''
    id_file = mode
    url_list = []
    with open (id_file) as f:
        id_list = f.readlines()
    for bulletin_id in id_list:
        bulletin_id = bulletin_id.rstrip() #удаляем символы новой строки
        if '-' in bulletin_id:
            url_list.append('https://www.farpost.ru/admin/update-index-attributes/good/' + bulletin_id[1:])
        else:
            url_list.append('https://www.farpost.ru/admin/update-index-attributes/bulletin/' + str(bulletin_id))
    return(url_list)

def reindex():
    '''
    Переиндексирует объявления и гудсы
    Вход: список url_list c  URL-ами переиндексации (получен в функции «collect_bulletins_id» или в «collect_bulletins_id_from_file»)
    Выход: ничего (переиндексированные объявления)

    НУЖНО ПОДТВЕРДИТЬ СЕРТИФИКАТ В БРАУЗЕРЕ ПРИ ЗАПУСКЕ
    '''
#    is_hitler = int(input('Turn on Hitler? 1 = YES, 0 = NO '))
#    is_hitler = 1
    is_hitler = 0
    if 'http' in mode:
        url_list = collect_bulletins_id()
        print()
        print('2 of 2. Reindex bulletins…')
    else:
        url_list = collect_bulletins_id_from_file()
        print('Reindex bulletins…')
    i = 1
    
    print(f'Found {len(url_list)} URLs')
    print('DON\'T FORGET TO ACCEPT CERTIFICATE IN CHROME WINDOW!')
    print()
    if is_hitler: #если Hitler включен, запускаем браузер Selenium с картинками
        #browser = webdriver.Chrome(executable_path='/home/arzhanov/Documents/chromedriver') #активировать при работе в Linux
        browser = webdriver.Chrome(executable_path='D:\OneDrive\Документы\Фарпост\chromedriver.exe') #активировать при работе в Windows
        browser.get("https://www.farpost.ru/sign?")
        username = browser.find_element_by_id("sign")
        password = browser.find_element_by_id("password")
        username.send_keys("IvanArzhanov")
        password.send_keys("m4$CEtaxy.V^v*-w\C9K")
        browser.find_element_by_id("signbutton").click()
        input('Turn on HITLER and click «Enter» to continue…') #программа ждет, когда мы включим Hilter и нажмем Enter
    else: #загружаем браузер Selenium без картинок
        opt = webdriver.ChromeOptions()
        opt.add_extension("Block-image_v1.1.crx")
        #browser = webdriver.Chrome(executable_path='/home/arzhanov/Documents/chromedriver', options=opt) #активировать при работе в Linux
        browser = webdriver.Chrome(executable_path='D:\OneDrive\Документы\Фарпост\chromedriver.exe', options=opt) #активировать при работе в Windows
        browser.get("https://www.farpost.ru/sign?")
        username = browser.find_element_by_id("sign")
        password = browser.find_element_by_id("password")
        username.send_keys("IvanArzhanov")
        password.send_keys("m4$CEtaxy.V^v*-w\C9K")
        browser.find_element_by_id("signbutton").click()
    for url in url_list:
        print(f'Doing URL {i} of {len(url_list)}')
        browser.get(url)
        i += 1

start_time = timeit.default_timer()
reindex()
stop_time = timeit.default_timer()
program_time = stop_time-start_time
print()
program_time_hour = int(program_time // 3600)
program_time_min = int((program_time - program_time_hour*3600) // 60)
program_time_sec = int(round(program_time - program_time_min*60,0))
print(f'It took {program_time_hour}:{program_time_min}:{program_time_sec} of my life, silly bastard!') 
print()
print(mode)
