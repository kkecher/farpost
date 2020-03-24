#!/usr/bin/env python3

'''
Собирает имена и их синонимы из Википедии
Вход: список имен
Выход: список имен с синонимами

ВАЖНО!!!
— Нужно руками проверить данные для названий, состоящих НЕ из одного слова, так как могут быть переходы на ложные страницы
— Иногда собираются некорректные данные из некоторых чисел — нужно валидировать данные после сбора.
'''

import requests
import re

name_list = input('Enter file with names: ')
result = input('Enter result file: ')

with open(name_list, 'r', encoding='utf8') as f:
    name_list = f.read().splitlines()

def get_other_form(source_code):
    is_other_form = 0
    other_form = re.findall('Другие формы.*\n.*plainlist.*\n.*title="?(.*?)"?>', source_code)
    if other_form == []:
        other_form = ''
    else:
        other_form = other_form[0]
    return(other_form)

def get_synonyms(source_code):
    synonyms = re.findall('Производ. формы.*\n.*plainlist">.*\n(.*?)<', source_code)
    if synonyms == []:
        synonyms = ''
    else:
        synonyms = synonyms[0]
    return(synonyms)

i = 1
for name in name_list:
    print (f'Doing {i} of {len(name_list)} names')
    try:
        url = 'https://ru.wikipedia.org/wiki/' + name
        print(url)
        source_code = requests.get(url)
        source_code = source_code.text
        other_form = get_other_form(source_code)
        synonyms = get_synonyms(source_code)
    except KeyboardInterrupt:
        raise
    except:
        other_forms = 'АХТУНГ'
        synonyms = 'АХТУНГ'
    i += 1
    with open(result, 'a') as f:
        f.write(f'{name}\n')
        f.write('-'*35 + '\n')
        f.write('Другие формы: ')
        try:
            f.write(f'{other_form}')
        except KeyboardInterrupt:
            raise
        except:
            other_forms = 'АХТУНГ'
            f.write(f'{other_form}')
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
