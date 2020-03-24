'''
Оставляет уникальные синонимы и сортирует их по алфавиту
Вход: справочник лемм
Выход: справочник лемм с отсортированными уникальными синонимами

В НЕКОТОРЫХ СПРАВОЧНИКАХ ПЕРВЫЕ СИНОНИМЫ ИСПОЛЬЗУЮТСЯ ДЛЯ SEO. Ты НЕ хочешь использовать этот скрипт для таких справочников!
'''

import natsort

lemmax_file = input('В каком файле сохранен справочник? ')
result_file = input('Куда сохранить результаты? ')

try:
    with open(lemmax_file, 'r', encoding='utf8') as f:
        lemmax_list = f.read().splitlines()
except:
    with open('res2', 'r', encoding='cp1251') as f:
        lemmax_list = f.read().splitlines()

lemmax_dict = {}
for line in lemmax_list:
    line = line.replace(', ', ',')
    line = line.replace('%', '')
    line_list = line.split(',')
    name = line_list[0]
    synonyms_list = line_list[1:]
    lemmax_dict[name] = synonyms_list

with open(result_file, 'w') as f:
    for name, synonyms_list in lemmax_dict.items():
        f.write(name)
        synonyms_set = set(synonyms_list)
        synonyms_sorted_set = natsort.natsorted(synonyms_set)
        for synonym in synonyms_sorted_set:
            f.write(f', {synonym}')
        f.write('\n')
