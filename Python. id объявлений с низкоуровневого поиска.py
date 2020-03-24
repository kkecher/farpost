#!/usr/bin/env python3

'''
Собирает id объявлений и товаров с низкоуровневого поиска
Вход: id раздела
Выход: файл с id объявлений и товаров

Максимум: 1000 страниц
ВЫДАЕТ НЕ ВСЕ РЕЗУЛЬТАТЫ И МЕНЬШЕ, ЧЕМ ЗАЯВЛЕНО В «ВСЕГО НАЙДЕНО»
'''

import urllib.request
from selenium import webdriver
import re
import math
import time

search_url = input('Enter search URL: ')
#dir_id = input('Enter directory id: ')

#выводит частные объявления и товары
#search_url = f'http://search-ui.srv.loc/search?agentId=&attributes=&clientId=&command=undefined&facetingAttributes=&filter=&pageNumber=1&query=directoryId%20%3D%20{dir_id}&sort=&zone=default'

#выводит только товары
#search_url = f'http://search-ui.srv.loc/search?agentId=&attributes=&clientId=&command=undefined&facetingAttributes=&filter=&pageNumber=1&query=directoryId%20%3D%20{dir_id}%20and%20type%3Dgood&sort=&zone=default'

#выводит только объявления
#search_url = f'http://search-ui.srv.loc/search?agentId=&attributes=&clientId=&command=undefined&facetingAttributes=&filter=&pageNumber=1&query=directoryId%20%3D%20{dir_id}%20and%20type%3Dbulletin&sort=&zone=default'

result = input('Enter result file: ')

open(result, 'w').close()

#Выключаем картинки, но в этом режиме НЕ сможем включить stalin
opt = webdriver.ChromeOptions()
opt.add_extension("Block-image_v1.1.crx")
#browser = webdriver.Chrome(executable_path='/home/arzhanov/Documents/chromedriver', chrome_options=opt) #активировать при работе в Linux, при необходимости поменять путь к файлу chromedriver
browser = webdriver.Chrome(executable_path='D:\OneDrive\Документы\Фарпост\chromedriver.exe', chrome_options=opt) #активировать при работе в Windows

#Включает картинки, страницы дольше загружаются, но иногда нужно для включения stalin и прочего
#browser = webdriver.Chrome(executable_path='/home/arzhanov/Documents/chromedriver') #активировать при работе в Linux, при необходимости поменять путь к файлу chromedriver
#browser = webdriver.Chrome(executable_path='D:\OneDrive\Документы\Фарпост\chromedriver.exe') #активировать при работе в Windows

browser.get(search_url)

def wait_for_page_load():
    '''
    Проверяет, загрузилась ли полностью страница
    Вход: ничего
    Выход: дает программе дальнейший ход
    '''
    time.sleep(1)
    while True:
        list_table_of_results = browser.find_elements_by_xpath("//*[@class='table search-results']")
        if list_table_of_results != []:
            break
    return()

def total_count_pages():
    '''
    Считает количество страниц с результатами
    Вход: ничего
    Выход: количество страниц с результатами
    '''
    wait_for_page_load()
    total_count_text = browser.find_element_by_xpath("//*[@class='dl-horizontal search-summary-dl']/div/dd")
    total_count_text = total_count_text.text
    total_count_text = total_count_text.replace(' ', '')
    total_count = int(total_count_text)
    page_total = math.ceil(total_count / 50)
    return(page_total)

def get_ids():
    '''
    Собирает заголовки на текущей странице
    Вход: ничего
    Выход: список из 50 заголовков
    '''
    list_id = []
    for i in range(2, 52):
        try:
            id_html_string = "//*[@class='table search-results']/tbody/tr[" + str(i) + "]/td[1]"
            id_ = browser.find_element_by_xpath(id_html_string)
            id_ = id_.text
            list_id.append(id_)
        except:
            return(list_id)
    return(list_id)

def go_next_page():
    '''
    Переходит на следующую страницу
    Вход: ничего
    Выход: переход на следующую страницу
    '''
    next_page_link_html_string = browser.find_element_by_link_text("»")
    next_page_link_html_string.click()
    return()

wait_for_page_load()
page_total = total_count_pages()
i = 1
while True:
    print(f'Doing page  {i} of  {page_total}')
    list_id = get_ids()
    with open(result, 'a') as f:
        for id_ in list_id:
            id_ = id_.replace('&quot;','"')
            id_ = id_.replace('&amp;','&')
            id_ = id_.replace('&shy;','')
            id_ = id_.replace('&gt;','>')
            id_ = id_.replace('&#039;','\'')
            id_ = re.sub(r'06$', '', id_)
            id_ = '-' + id_
            f.write(f'{id_}\n')
    if i == page_total:
        break
    i += 1
    go_next_page()
    wait_for_page_load()
