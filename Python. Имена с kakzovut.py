#!/usr/bin/env python3

'''
Собирает имена и их синонимы из kakzovut.ru
Вход: список URL'ов
Выход: список имен с синонимами
'''

import requests
import re

#url_list = input('Enter file with URLs: ')
#result = input('Enter result file: ')

url_list = 'kakzovut_url'
result = 'res_kakzovut'

with open(url_list, 'r', encoding='utf8') as f:
    url_list = f.read().splitlines()

def get_name(source_code):
    name = re.findall(r'<h1>Значение имени (.*?)<', source_code)
    if name == []:
        name = ''
    else:
        name = name[0]
    return(name)


def get_short_form(source_code):
    short_form = re.findall(r'Краткая форма имени.*?<\/b>(.*?)<br>', source_code)
    if short_form == []:
        short_form = ''
    else:
        short_form = short_form[0]
    return(short_form)

def get_synonyms(source_code):
    synonyms = re.findall(r'Синонимы имени.*?<\/b>(.*?)<br>', source_code)
    if synonyms == []:
        synonyms = ''
    else:
        synonyms = synonyms[0]
    return(synonyms)

i = 1
for url in url_list:
    print (f'Doing {i} of {len(url_list)} urls')
    try:
        source_code = requests.get(url)
        source_code = source_code.text
        name = get_name(source_code)
        short_form = get_short_form(source_code)
        synonyms = get_synonyms(source_code)
    except KeyboardInterrupt:
        raise
    except:
        name = 'АХТУНГ'
        short_forms = 'АХТУНГ'
        synonyms = 'АХТУНГ'
    i += 1
    with open(result, 'a') as f:
        try:
            f.write(f'{name} - {url}\n')
        except KeyboardInterrupt:
            raise
        except:
            name = 'АХТУНГ'
            f.write(f'{name} - {url}\n')
        f.write('-'*35 + '\n')
        f.write('Краткая форма: ')
        try:
            f.write(f'{short_form}')
        except KeyboardInterrupt:
            raise
        except:
            short_forms = 'АХТУНГ'
            f.write(f'{short_form}')
        f.write('\n')
        f.write('Синонимы: ')
        try:
            f.write(f'{synonyms}')
        except KeyboardInterrupt:
            raise
        except:
            synonyms = 'АХТУНГ'
            f.write(f'{synonyms}')
        f.write('\n'*2)

