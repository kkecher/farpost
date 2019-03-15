'''
Собирает заголовки в спецтехнике (они НЕ выводятся во вьюдир, как в остальных разделах)
Вход: файл со списком URL'ов
Выход: файл с записями вида «URL — Заголовок»
'''

import urllib.request
import re

url_file = input('Enter file with URLs: ')
result_file = input('Enter result file: ')

with open(url_file, 'r') as f:
    url_list = f.read().splitlines()

subject_list= []
i = 0

for url in url_list:
    i+= 1
    len_url_list = len(url_list)
    source_page_for_lemma = urllib.request.urlopen(url)
    for line in source_page_for_lemma:
#Со временем скрипт начал использоваться не только для сбора заголовков, но и других полей
#        subject_temp_list = re.findall('(div class="label">Топливо</div>)', line.decode('cp1251'))
#        subject_temp_list = re.findall('(div class="label">Объём двигателя</div>)', line.decode('cp1251'))
#        subject_temp_list = re.findall('(div class="label">Мощность</div>)', line.decode('cp1251'))
        subject_temp_list = re.findall('data-field="subject" class="inplace">(.*?)<', line.decode('cp1251')) #тут как раз собираем заголовок
#        subject_temp_list = re.findall('data-field="spectechHeight">\n.*\n\t(.*?)<', line.decode('cp1251'))
        if subject_temp_list != []:
            break
    if subject_temp_list == []:
        subject = 'АХТУНГ!!!'
    else:
        subject = subject_temp_list[0]
        subject = subject.replace('&quot;','"')
        subject = subject.replace('&amp;','&')
        subject = subject.replace('&shy;','')
        subject = subject.replace('&gt;','>')
        subject = subject.replace('&#039;','\'')
    subject_list.append(subject)
    print(str(i) + ' of ' + str(len_url_list) + '. ' + subject)

with open(result_file, 'w') as f:
    i = 0
    for url in url_list:
        subject = subject_list[i]
        f.write(url + ' #—# ' + subject + '\n')
        i+=1
