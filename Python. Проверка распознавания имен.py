#!/usr/bin/env python3

'''
Проверяет точное совпадение набора фраз с синонимом. В отличие от леммакса, не нормализует фразы.
Вход: справочник имен с синонимами. Список фраз для проверки.
Выход: список имен с относящимися к нему вводами.
'''

import re

#name_file = input('Введите файл со справочником имен: ')
name_file = 'Имена. Справочник.txt'
check_file = input('Введите файл со фразами, которые нужно проверить: ')
#res_file = input('В какой файл пишем результат? ')
res_file = 'res'

#создаем словарь с именами, где key - лемма, value - синонимы
def name_normalize(line):
    '''
    Нормализует строку и именем и синонимами
    Вход: ненормализованная строка с именем и синонимами
    Выход: нормализованная строка с именем и синонимами
    '''
    line = line.strip()
    line = re.sub(',$', '', line, flags=re.IGNORECASE)
    line = line.replace(',', ', ')
    line = line.replace('  ', ' ')
    line = line.replace(', ,', ',')
    line = line.strip()
    return(line)

try:
    with open(name_file, 'r', encoding = 'utf8') as f:
        name_dict = {}
        for line in f:
            cleaned_line = name_normalize(line) 
            line_list = cleaned_line.split(', ')
            name = line_list[0]
            has_wrong_symbols = re.findall(r'[^а-я,-]', name, flags=re.IGNORECASE)
            if has_wrong_symbols:
                raise Exception(f'Некорректные символы в имени: {name}')
            synonyms = [synonym.lower() for synonym in line_list]
            name_dict[name] = synonyms
except:
    with open(name_file, 'r', encoding = 'cp1251') as f:
        name_dict = {}
        for line in f:
            cleaned_line = name_normalize(line) 
            line_list = cleaned_line.split(', ')
            name = line_list[0]
            has_wrong_symbols = re.findall(r'[^а-я,-]', name, flags=re.IGNORECASE)
            if has_wrong_symbols:
                raise Exception(f'Некорректные символы в имени: {name}')
            synonyms = [synonym.lower() for synonym in line_list]
            name_dict[name] = synonyms

try:
    with open(check_file, 'r', encoding = 'utf8') as f:
        check_list = f.read().splitlines()
except:
    with open(check_file, 'r', encoding = 'cp1251') as f:
        check_list = f.read().splitlines()

def check_line_normalize(line):
    '''
    Нормализует проверяемую строку
    Вход: ненормализованная строка
    Выход: нормализованная строка
    '''
    line = line.lower()
    line = re.sub('ё', 'е', line)
    line = re.sub(r'[^а-яa-z]', '', line)
    return(line)

#проверяем соответствие фразы и синонимов. Если соответствие есть, то к имени приписываем проверяемую фразы и дописываем в словарь check_dict
check_dict = {}
no_match_list = []
match_multiple_names_list = []
i = 1
for line in check_list:
    print(f'Обрабатываю {i} строку из {len(check_list)}')
    cleaned_line = check_line_normalize(line)
    #print(cleaned_line)
    is_match = 0
    for name, synonyms in name_dict.items():
        if cleaned_line in synonyms:
            check_dict.setdefault(name, []).append(line)
            is_match += 1
    if is_match == 0:
        no_match_list.append(line)
    if is_match > 1:
        match_multiple_names_list.append(line)
    i += 1

with open(res_file, 'w') as f:
    for name, phrases in check_dict.items():
        f.write(name)
        f.write('\n')
        f.write('-'*35)
        f.write('\n')
        for phrase in phrases:
            f.write(phrase)
            f.write('\n')
        f.write('\n'*2)
    f.write('Нет соответствий')
    f.write('\n')
    f.write('-'*35)
    f.write('\n')
    for phrase in no_match_list:
        f.write(phrase)
        f.write('\n')
    f.write('\n'*2)
    f.write('Соответствует нескольким именам')
    f.write('\n')
    f.write('-'*35)
    f.write('\n')
    for phrase in match_multiple_names_list:
        f.write(phrase)
        f.write('\n')
