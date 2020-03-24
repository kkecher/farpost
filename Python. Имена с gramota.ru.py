#!/usr/bin/env python3

'''
Собирает имена и их синонимы с gramota.ru. Сайт не отдает список имен, но позволяет искать со *, поэтому будем подставлять буквы и забирать результаты, пока не получим пустую страницу
Вход: ничего
Выход: список имен с синонимами
'''

import requests
import re

url = 'http://gramota.ru/slovari/dic/?pe=x&word=юри*'
#result = input('Enter result file: ')

results= 'res_gramota2'
alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

def build_url(url, has_results):
    if url == 'http://gramota.ru/slovari/dic/?pe=x&word=яя*':
        return(url)
    url = url[:-1] #убираем * в конце
    if has_results:
        url += alphabet[0]
    else:
        while True:
            last_letter = url[-1]
            last_letter_index = alphabet.find(last_letter)
            if last_letter_index == (len(alphabet)-1):
                url = url[:-1]
                continue
            else:
                last_letter_index += 1
                last_letter = alphabet[last_letter_index]
                url = url[:-1] + last_letter
                break
    url += '*'
    return(url)

def search(url):
    with open(results, 'a') as f:
        names = ''
        has_results = 1
        while True:
            url = build_url(url, has_results)
            print(url)
            if url == 'http://gramota.ru/slovari/dic/?pe=x&word=яя*':
                return(names)
            else:
                source_code = requests.get(url)
                source_code = source_code.text
                names_list = re.findall(r'href="http://www.gramota.ru/slovari/info/petr/">Словарь русских имён</a>.*?\n.*?<b>(.*?)<\/div>', source_code)
                if names_list:
                    has_results = 1
                    names_string = names_list[0]
                    names_string = re.sub(r'<span class="accent">', '', names_string, flags=re.IGNORECASE)
                    names_string = re.sub(r'<b>', '', names_string, flags=re.IGNORECASE)
                    names_string = re.sub(r'<\/b>', '', names_string, flags=re.IGNORECASE)
                    names_string = re.sub(r'<i>', '', names_string, flags=re.IGNORECASE)
                    names_string = re.sub(r'<\/i>', '', names_string, flags=re.IGNORECASE)
                    names_string = re.sub(r'<\/span>', '', names_string, flags=re.IGNORECASE)
                    names_string = re.sub(r'<br>', '\n', names_string, flags=re.IGNORECASE)
                    names_string = re.sub(r'<sup>\d+<\/sup>', '\n', names_string, flags=re.IGNORECASE)
                    names_string = re.sub(r'&mdash;', ' - ', names_string, flags=re.IGNORECASE)
                    names += names_string + '\n'
                    f.write(names)
                else:
                    has_results = 0

names = search(url)
