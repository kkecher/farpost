'''
Собирает тело объявления (описание) в товарах
Вход: файл со списком URL-ов
Выход: файл с описаниями товаров
'''

import urllib.request
import re

url_file = input('Enter file with URLs: ')
result_file = input('Enter result file: ')
with open(url_file, 'r') as f:
    url_list = f.read().splitlines()

body_list= []
i = 0

for url in url_list:
    source_string = ''
    i+= 1
    len_url_list = len(url_list)
    print(str(i) + ' of ' + str(len_url_list))
    source_page_for_lemma = urllib.request.urlopen(url)
    for line in source_page_for_lemma:
        source_string += line.decode('cp1251')
    source_string = re.sub(r'\n|\t|\s', ' ', source_string)
    body_list_temp = re.findall('data-field="text">(.*?)<\/p>', source_string)
    if body_list_temp == []:
        body = 'Ахтунг!!!'
    else:
        body = body_list_temp[0]
    body = body.replace('&quot;','"')
    body = body.replace('&amp;','&')
    body = body.replace('&shy;','')
    body = body.replace('&gt;','>')
    body = body.replace('&#039;','\'')
    body = re.sub(r'<.*?>', ' ', body)
    body = body.replace('  ', ' ')
    if body == '':
        body = 'Ахтунг!!!'
    body_list.append(body)

with open(result_file, 'w') as f:
    i = 0
    for url in url_list:
        body = body_list[i]
        f.write(url + ' #—# ' + body + '\n')
        i+=1
