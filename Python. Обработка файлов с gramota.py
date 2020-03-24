#!/usr/bin/env python3

'''
Вычленяет имена и синонимы из данных, собранных с gramota.ru
Вход: файл с данными из gramota.ru
Выход: файл со списком имен и синоинмво
'''

import re
import timeit

start_time = timeit.default_timer()

file_name = input('Enter file name: ')

names = {}
name_regex = '([а-яa-z]+)\*?,'
synonyms_regex = '[рР]азг\..*?([А-ЯA-Z][а-яa-z]+)|[Пп]роизводные.*?([А-ЯA-Z].*)|[Сс]тар.*форма.*?([А-ЯA-Z][а-яa-z]+)'
name_regex = re.compile(name_regex, flags=re.IGNORECASE)
synonyms_regex = re.compile(synonyms_regex)

with open(file_name, 'r', encoding='cp1251') as f:
    for line in f:
        name_list = name_regex.match(line)
        synonyms_list = synonyms_regex.findall(line)
        if name_list:
            name = name_list.group(1)
            names[name] = names.get(name, [])
        if synonyms_list:
            for synonyms_tuple in synonyms_list:
                for synonym in synonyms_tuple:
                    if synonym != '' and synonym not in names[name]:
                        names[name].append(synonym)
        #print(f'line: {line}')
        #print(f'name: {name}')
        #print(f'synonym_list {synonyms_list}')
        #print(f'dict: {names}')
        #input('enter')
        #print()
        #print()

with open('res_gramota_total_2', 'a') as f:
    for name, synonyms in names.items():
        f.write(name)
        for synonym in synonyms:
            synonym = synonym.replace(';', ',')
            synonym = synonym.replace('.', ',')
            synonym = synonym.replace('<OL>', '')
            synonym = synonym.replace('  ', ' ')
            synonym = synonym.replace(',,', ',')
            synonym = synonym.replace(', ,', ',')
            f.write(f', {synonym}')
        f.write('\n')

stop_time = timeit.default_timer()
program_time = stop_time-start_time
program_time_hour = int(program_time // 3600)
program_time_min = int((program_time - program_time_hour*3600) // 60)
program_time_sec = int(program_time - program_time_min*60 - program_time_hour*3600)

print()
print('I have finished your dirty wish.')
print(f'It took {program_time_hour}:{program_time_min}:{program_time_sec} of my life, silly bastard.')
