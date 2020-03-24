'''
Собирает число объявлений/товаров в наличии с низкоуровневого поиска по id городов
Вход: файл со список id городов
Выход: файл с числом предложений в наличии
'''

import urllib.request
from selenium import webdriver
import re
import math

city_id = input('Enter city file: ')
result = input('Enter result file: ')
count_total = 0

with open(city_id, 'r') as f:
    city_id_list = f.read().splitlines()

open(result, 'w').close()

#Turn off images, but we can't turn on stalin in this mode
opt = webdriver.ChromeOptions()
opt.add_extension("Block-image_v1.1.crx")
browser = webdriver.Chrome(executable_path='/home/arzhanov/Documents/chromedriver', chrome_options=opt)


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

def total_count():
    '''
    Считает число предложений в наличии
    Вход: ничего
    Выход: число предложений в наличии
    '''
    wait_for_page_load()
    total_count_text = browser.find_element_by_xpath("//*[@class='dl-horizontal search-summary-dl']/div/dd")
    total_count_text = total_count_text.text
    total_count_text = total_count_text.replace(' ', '')
    total_count = int(total_count_text)
    return(total_count)

i = 1
for city_id in city_id_list:
    print('Doing ' + str(i) + ' of ' + str(len(city_id_list)))
    search_url = 'http://search-ui.srv.loc/search?agentId=&attributes=&clientId=&command=StagedSearch&facetingAttributes=&filter=&pageNumber=1&query=cityId%20%3D%20' + str(city_id) + '%20and%20goodPresentState%20%3D%20present&sort=&zone=default'
    browser.get(search_url)
    try:
        count_total = total_count()
    except:
        count_total = 'Ахтунг!!!'
    i += 1
    with open(result, 'a') as f:
        f.write(str(count_total) + '\n')
