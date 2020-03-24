#!/usr/bin/env python3

'''
Собирает леммы всех уровней по разделам
Вход: файл со списком разделов, полученный в Python. Собираем URL'ы из API Хьюстона.py
Выход: файл со списком лемм по разделам
'''

import requests
import re

#dirs_file = input('Enter dirs file: ')
#result = input('Enter result file: ')
dirs_file = 'temp_dirs'
result = 'res2'

with open(dirs_file, 'r', encoding='utf8') as f:
    dirs_list = f.read().splitlines()

def get_lemma(url):
    '''
    Рекурсивно собирает список лемм всех уровней по урлу
    Вход: url раздела или леммы
    Выход: словарь со списком лемм со всех уровней
    '''
    response = requests.get(url)
    lemmas_dirty = re.findall(r'div name="query.*?"clear"', response.text)
    lemmas = re.findall(r'"(https[^"]+\/\+\/.*?)"', lemmas_dirty[0])
    print(lemmas)
    input('enter')
    if len(lemmas) == 1:
        print('Next lemma')
        res_dict.setdefault(dir_url, []).append(lemmas)
    else:
        print('We need to go deeper')
        for lemma in lemmas:
            get_lemma(lemma)
    return()

res_dict= {}
i = 1
for dir_url in dirs_list:
    print(f'Doing {i} of {len(dirs_list)}')
    get_lemma(dir_url)
    i += 1

with open(result, 'w') as f:
    for dir_url, lemmas in res_dict.items():
        f.write(f'{dir_url}\n{"-"*30}\n')
        for lemma in lemmas:
            f.write(lemma + '\n')
            f.write('\n')
