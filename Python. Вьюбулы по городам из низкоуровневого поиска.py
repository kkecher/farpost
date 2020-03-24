'''
Собирает количество вьюбулов по городам из низкоуровневого поиска
Вход: файл с id городов
Выход: файл с количеством вьюбулов и id городов
'''

import urllib.request
from selenium import webdriver

city_ids = input('Enter file with cities ids: ')
#start_search_url = 'http://search-ui.srv.loc/search?agentId=&attributes=&clientId=&command=StandardSearch&facetingAttributes=&filter=&itemsPerPage=50&pageNumber=1&query=cityId%3D'
start_search_url = 'http://search-ui.srv.loc/search?agentId=&attributes=&clientId=&command=StandardSearch&facetingAttributes=&filter=&itemsPerPage=50&pageNumber=1&query=directoryId%20in%20%281121%2C%201122%2C%201123%2C%201124%2C%201125%2C%201126%2C%201127%2C%201128%2C%201129%2C%201130%2C%201131%2C%201132%2C%201133%2C%201134%2C%201135%2C%201136%2C%201137%2C%201138%2C%201139%2C%201140%2C%201141%2C%201142%2C%201148%2C%20212%2C%20214%2C%20215%2C%20216%2C%20218%2C%20219%2C%20220%2C%20221%2C%20222%2C%20223%2C%20225%2C%20226%2C%20227%2C%20520%2C%20686%2C%20687%2C%20805%2C%20835%2C%20848%2C%20849%2C%20850%2C%20851%2C%20541%2C%20213%29%20and%20cityId%3D'
end_search_url = '&sort=&zone=default'
result = input('Enter result file: ')

with open (city_ids, 'r') as f:
    city_id_list = f.read().splitlines()

open(result, 'w').close()

#Выключает картинки, но мы не сможем включить stalin
opt = webdriver.ChromeOptions()
opt.add_extension("Block-image_v1.1.crx")
#browser = webdriver.Chrome(executable_path='/home/arzhanov/Documents/chromedriver', chrome_options=opt) #активировать при работе в Linux, поменять путь к chromedriver при необходимости
browser = webdriver.Chrome(executable_path='D:\OneDrive\Документы\Фарпост\chromedriver.exe', options=opt) #активировать при работе в Windows

#Включаем картинки. Страницы загружаются дольше, но можем включить stalin и поменять ряд других параметров
#browser = webdriver.Chrome(executable_path='/home/arzhanov/Documents/chromedriver') #активировать при работе в Linux, поменять путь к chromedriver при необходимости
#browser = webdriver.Chrome(executable_path='D:\OneDrive\Документы\Фарпост\chromedriver.exe') #активировать при работе в Windows


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

def count_total():
    '''
    Считает общее число страниц
    Вход: ничего
    Выход: общее число страниц
    '''
    wait_for_page_load()
    total_num_text = browser.find_element_by_xpath("//*[@class='dl-horizontal search-summary-dl']/div/dd")
    total_num_text = total_num_text.text
    total_num_text = total_num_text.replace(' ', '')
    total_num = int(total_num_text)
    return(total_num)

with open(result, 'a') as f:
    i = 1
    len_city_id_list = len(city_id_list)
    len_city_id_list = str(len_city_id_list)
    for city_id in city_id_list:
        print('Doing ' + str(i) + ' of ' + len_city_id_list)
        search_url = start_search_url + str(city_id) + end_search_url
        browser.get(search_url)
        wait_for_page_load()
        total_num = count_total()
        f.write(str(city_id) + '\t' + str(total_num) + '\n')
        i += 1
