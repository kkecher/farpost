#!/usr/bin/env python3

'''
Собирает заголовки объявлений и товаров с низкоуровневого поиска
Вход: id раздела
Выход: файл с заголовками объявлений и товаров

Максимум: 1000 страниц
ВЫДАЕТ НЕ ВСЕ РЕЗУЛЬТАТЫ И МЕНЬШЕ, ЧЕМ ЗАЯВЛЕНО В «ВСЕГО НАЙДЕНО»
'''

import urllib.request
from selenium import webdriver
import re
import math

#dir_id = input('Enter directory id: ')
#search_url = 'http://search-ui.srv.loc/search?agentId=&attributes=&clientId=&command=undefined&facetingAttributes=&filter=&pageNumber=1&query=directoryId%20%3D%20' + str(dir_id) + '&sort=&zone=default'
search_url = 'http://search-ui.srv.loc/search?agentId=&attributes=&clientId=&command=undefined&facetingAttributes=&filter=&itemsPerPage=50&pageNumber=1&query=directoryId%3D776%20and%20type%3Dgood%20and%20subject%20contains%28%27hybrid%27%29&sort=&zone=default'
result = input('Enter result file: ')

open(result, 'w').close()

#Выключает картинки, но мы не сможем включить stalin
opt = webdriver.ChromeOptions()
opt.add_extension("Block-image_v1.1.crx")
#browser = webdriver.Chrome(executable_path='/home/arzhanov/Documents/chromedriver', chrome_options=opt) #активировать при работе в Linux, поменять путь к chromedriver при необходимости
browser = webdriver.Chrome(executable_path='D:\OneDrive\Документы\Фарпост\chromedriver.exe', options=opt) #активировать при работе в Windows

#Включаем картинки. Страницы загружаются дольше, но можем включить stalin и поменять ряд других параметров
#browser = webdriver.Chrome(executable_path='/home/arzhanov/Documents/chromedriver') #активировать при работе в Linux, поменять путь к chromedriver при необходимости
#browser = webdriver.Chrome(executable_path='D:\OneDrive\Документы\Фарпост\chromedriver.exe') #активировать при работе в Windows

browser.get(search_url)

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

def total_count_pages():
    '''
    Считает общее число страниц
    Вход: ничего
    Выход: общее число страниц
    '''
    wait_for_page_load()
    total_count_text = browser.find_element_by_xpath("//*[@class='dl-horizontal search-summary-dl']/div/dd")
    total_count_text = total_count_text.text
    total_count_text = total_count_text.replace(' ', '')
    total_count = int(total_count_text)
    page_total = math.ceil(total_count / 50)
    return(page_total)

def get_subjects():
    '''
    Собирает заголовки на текущей странице
    Вход: ничего
    Выход: список с 50 заголовками
    '''
    list_subject = []
    for i in range(2, 52):
        try:
            subject_html_string = "//*[@class='table search-results']/tbody/tr[" + str(i) + "]/td[3]"
            subject = browser.find_element_by_xpath(subject_html_string)
            subject = subject.text
            list_subject.append(subject)
        except:
            return(list_subject)
    return(list_subject)

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
with open(result, 'a') as f:
    while True:
        print('Doing page ' + str(i) + ' of ' + str(page_total))
        list_subject = get_subjects()
        for subject in list_subject:
            subject = subject.replace('&quot;','"')
            subject = subject.replace('&amp;','&')
            subject = subject.replace('&shy;','')
            subject = subject.replace('&gt;','>')
            subject = subject.replace('&#039;','\'')
            f.write(subject + '\n')
        if i == page_total:
            break
        i += 1
        go_next_page()
        wait_for_page_load()
