#!/usr/bin/env python3

'''
НЕ ДОДЕЛАНО! НУЖНО ПРИКРУТИТЬ АВТОРИЗАЦИЮ НА ФАРПОСТЕ
Одобряет фразы в админке низкочастотников https://www.farpost.ru/seo/search_phrases/untried
Вход: ничего
Выход: ничего (одобренные фразы)
'''

import urllib.request
import base64
import re

adminka_url = 'https://www.farpost.ru/seo/search_phrases/untried'

i = 1
approve_id_list = []
approve_id_list_raw = []

#получаем количество ключевиков для расчета количества страниц
#source_page_for_page_total = urllib.request.urlopen(adminka_url) 
#for line in source_page_for_page_total:
#    keywords_count_list = re.findall('pagestat"> \((.*?) запросов"', line.decode('cp1251'))
#    if keywords_count_list != []:
#        keywords_count = keywords_count_list[0]
#        break
#keywords_count = keywords_count.replace(' ', '') 
#keywords_count = int(keywords_count_list[0])
#page_total = (keywords_count // 100) + 1 #получаем число страниц через (целочисленное деление + 1)
#print('Found ' + str(page_total) + ' pages')

#получаем список id ключевиков для одобрения
#while i <= page_total:
#    print('Doing page ' + str(i) + ' of ' + str(page_total))
#    source_page = urllib.request.urlopen(adminka_url + '?page=' + str(i))
#    for line in source_page:
#        approve_id_list_raw += re.findall('<input type="radio" name="status_id(.*?)', line)
#    for approve_id in approve_id_list_raw:
#        approve_id_list.append(approve_id)
#    i+=1
#    approve_id_list_raw = []

#Авторизуемся на farpost.ru
password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
top_level_url = 'https://www.farpost.ru/sign?return=%2F'
password_mgr.add_password(None, top_level_url, 'IvanArzhanov', 'm4$CEtaxy.V^v*-w\C9K')

handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

opener = urllib.request.build_opener(handler)

#opener.open('https://www.farpost.ru/seo/search_phrases/untried')
opener.open('https://www.farpost.ru/sign?return=%2F')

urllib.request.install_opener(opener)

#result = urllib.request.urlopen('https://www.farpost.ru/seo/search_phrases/untried?page=1')
result = urllib.request.urlopen('https://www.farpost.ru/sign?return=%2F')
#result = urllib.request.urlopen('https://newadmin.drom.ru/newadmin/seo/tools/watcher/groups.php')
print(result.headers['www-authenticate'])
#for url in result:
#    print(url.decode('cp1251'))
