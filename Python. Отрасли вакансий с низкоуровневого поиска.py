'''
Собирает обрасли вакансий с низкоуровневого поиска.
Вход: ничего
Выход: файл с отраслями вакансий

Максимум: 1000 страниц
ВЫДАЕТ НЕ ВСЕ РЕЗУЛЬТАТЫ И МЕНЬШЕ, ЧЕМ ЗАЯВЛЕНО В «ВСЕГО НАЙДЕНО»
'''

import urllib.request
from selenium import webdriver
import re
import math
import time

search_url = 'http://search-ui.srv.loc/search?agentId=&attributes=&clientId=&command=null&facetingAttributes=&filter=&itemsPerPage=50&pageNumber=1&query=directoryId%20%3D%2049&sort=&zone=default'

result = input('Enter result file: ')

open(result, 'w').close()

#загруать страницы в браузере Selenium с картинками. Грузятся дольше, но нужно, чтобы поменять subject на job.professionalArea
#browser = webdriver.Chrome(executable_path='/home/arzhanov/Documents/chromedriver') #активировать при работе в Linux
browser = webdriver.Chrome(executable_path='D:\OneDrive\Документы\Фарпост\chromedriver.exe') #активировать при работе в Windows

browser.get(search_url)
input ('CHANGE SUBJECT TO «job.professionalArea» AND PRESS «ENTER»: ')

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

def get_industry():
    '''
    Собирает отрасли на странице
    Вход: ничего
    Выход: список с 50 отраслями
    '''
    dict_industry = {}
    for i in range(2, 52):
        try:
            id_html_string = "//*[@class='table search-results']/tbody/tr[" + str(i) + "]/td[1]"
            id_ = browser.find_element_by_xpath(id_html_string)
            id_ = id_.text
            id_ = 'http://farpost.ru/' + id_[:-2]
            industry_html_string = "//*[@class='table search-results']/tbody/tr[" + str(i) + "]/td[3]"
            industry_ = browser.find_element_by_xpath(industry_html_string)
            industry_ = industry_.text[:]
            dict_industry[id_] = industry_
        except:
            return(dict_industry)
    return(dict_industry)

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
    print('Doing page ' + str(i) + ' of ' + str(page_total))
    dict_industry = get_industry()
    with open(result, 'a') as f:
        for id_, industry_ in dict_industry.items():
            industry_ = industry_.replace('&quot;','"')
            industry_ = industry_.replace('&amp;','&')
            industry_ = industry_.replace('&shy;','')
            industry_ = industry_.replace('&gt;','>')
            industry_ = industry_.replace('&#039;','\'')
            f.write(id_ + ' — ' + industry_ + '\n')
    if i == page_total:
        break
    i += 1
    go_next_page()
    wait_for_page_load()
