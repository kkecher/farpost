#!/usr/bin/env python3

'''
Группирует фразы, полученные в «Python. Собираем URL'ы из API Хьюстона.py».
Вход: файл, полученный в «Python. Собираем URL'ы из API Хьюстона.py» и «Python. Получаем ответ сервера и собираем конечные URL'ы редиректов.py». Порядок столбцов: Фраза > URL
Выход: фразы, сгруппированные по разделам, леммам и применимости

ОТЛИЧИЯ ОТ ПЕРВОЙ ВЕРСИИ
Собирает локальную частоту и постепенно пополняет файл с результатами.

ПРИМЕЧАНИЕ 1:
Пока что группирует только по разделам, леммам и применимости! При необходимости добавлю еще фильтры

ПРИМЕЧАНИЕ 2:
Тут используется файл соответствий id раздела - URL раздела, полученый по «Python. Чтение структуры разделов из JSON.py»
'''

import re
import pandas as pd
import statistics
import natsort
from my_library import get_farpost_search_freq, convert_url_to_cyr

#houston_file = input('Enter file with keywords: ')
#results = input('Enter results file: ')
houston_file = 'Теги. Соответствия из Хьюстона без частотностей (разделы).txt'
results = 'Теги. Группировка для разделов.txt'

dir_id_name_url_file = 'Теги. Разделы.txt'
print()

#Создаем словарь разделов для подбора имени раздела по урлу
with open(dir_id_name_url_file, 'r', encoding='cp1251') as f:
    dir_dict = {}
    for line in f:
        line = line.strip()
        dir_id_name_url_list = line.split('\t')
        dir_url = dir_id_name_url_list.pop(2)
        dir_id_name_list = dir_id_name_url_list
        dir_dict[dir_url] = dir_id_name_list

#Разбиваем фразы из Хьюстона на word, dir_url, lemma_url, autoparts_compatibility_url
with open(houston_file, 'r', encoding='utf8') as f:
    houston_list = []
    for line in f:
        line = line.strip()
        word = line.split('\t')[0]
        url = line.split('\t')[1]
        dir_url = re.findall(r'(^.*?)(?:/dir?|/\?|/\+|/body/|/engine/|/model/)', url)
        lemma_url = re.findall(r'/\+/(.*?)/', url)
        if lemma_url == []:
            lemma_url = ['']
        else:
            lemma_url[0] = convert_url_to_cyr(lemma_url[0])
            if word.lower() == lemma_url[0].lower():
                lemma_url = [''] #если лемма полностью совпадает с ключевиком, то такой ключевик нам не нужен — лемма полностью отвечает на запрос 
        autoparts_compatibility_url = re.findall(r'(/(?:model|engine|body)/.*/)(?:\?|$)', url)
        if autoparts_compatibility_url == []:
            autoparts_compatibility_url = ['']
        else:
            autoparts_compatibility_url[0] = convert_url_to_cyr(autoparts_compatibility_url[0])
        word_url_params_list = [line] + dir_url + lemma_url + autoparts_compatibility_url
        houston_list.append(word_url_params_list)

#Группируем по разделам и леммам
df = pd.DataFrame(houston_list, columns=['word', 'dir', 'lemma', 'autoparts_compatibility'])
grouped = df.groupby(['dir', 'lemma', 'autoparts_compatibility'])['word'].apply(list)

prev_dir_url = ''
prev_lemma_url = ''
prev_autoparts_compatibility_url = ''
dir_count_list = []
lemma_count_list = []
autoparts_compatibility_count_list = []
min_count = 5 #минимальное количество фраз, при наличии которых в файл будет записан раздел / лемма / применимость
i = 0
for col in grouped.keys():
    dir_url = col[0]
    lemma_url = col[1]
    autoparts_compatibility_url = col[2]
    print(f'Doing {i+1} of {len(grouped)}: {dir_url} > {lemma_url} > {autoparts_compatibility_url}')
    #В список разделов записываем все, кроме корневого, у которых > min_count фраз
    if dir_url != prev_dir_url and dir_url != '' and dir_url != 'https://www.farpost.ru' and len(grouped[i]) > min_count:
        prev_dir_url = dir_url
        dir_id = dir_dict[dir_url][0]
        dir_name = dir_dict[dir_url][1]
        with open(results, 'a') as f:
           f.write(f'{"#"*80}\n')
           f.write(f'{dir_name}\t{dir_url}\t{dir_id} (раздел)\n')
           f.write(f'{"#"*80}\n')
           f.write(f'В корне раздела: {len(grouped[i])} шт.\n\n')
           dir_count_list.append(len(grouped[i]))
           freq_iter = 1
           for value in grouped[i]:
                print(f'\tGet search frequency for {freq_iter} of {len(grouped[i])} queries')
                freq = get_farpost_search_freq(value, dir_id)
                value_index = grouped[i].index(value)
                grouped[i][value_index] = f'{freq}\t{value}'
                freq_iter += 1
           grouped[i] = natsort.natsorted(grouped[i], reverse=True) #сортируем фразы по частотности. Использую natsort, так как дефолтная сортировка в натуральную сортировку не умеет
           for value in grouped[i]:
               f.write(f'{value} (фраза)\n')
           f.write('\n\n')

#    #Записываем в файл только те леммы, в которых > min_count фраз
#    if lemma_url != prev_lemma_url and lemma_url != '' and len(grouped[i]) > min_count:
#        prev_lemma_url = lemma_url
#        dir_id = dir_dict[dir_url][0]
#        dir_name = dir_dict[dir_url][1]
#        with open(results, 'a') as f:
#            f.write(f'{"-"*50}\n')
#            f.write(f'{lemma_url} (лемма)\t {dir_id}\t{dir_name}\t{dir_url}\n')
#            f.write(f'{"-"*50}\n')
#            f.write(f'В лемме: {len(grouped[i])} шт.\n\n')
#            lemma_count_list.append(len(grouped[i]))
#            freq_iter = 1
#            for value in grouped[i]:
#                print(f'\tGet search frequency for {freq_iter} of {len(grouped[i])} queries')
#                freq = get_farpost_search_freq(value, dir_id)
#                value_index = grouped[i].index(value)
#                grouped[i][value_index] = f'{freq}\t{value}'
#                freq_iter += 1
#            grouped[i] = natsort.natsorted(grouped[i], reverse=True) #сортируем фразы по частотности. Использую natsort, так как дефолтная сортировка в натуральную сортировку не умеет
#            for value in grouped[i]:
#                f.write(f'{value} (фраза)\n')
#            f.write('\n\n')
#
#    #В список autoparts_compatibility записываем все, в которых > min_count:
#    if autoparts_compatibility_url != prev_autoparts_compatibility_url and autoparts_compatibility_url != '' and len(grouped[i]) > 5:
#        prev_autoparts_compatibility_url = autoparts_compatibility_url
#        with open(results, 'a') as f:
#            f.write(f'{"-"*50}\n')
#            f.write(f'{autoparts_compatibility_url} (autoparts_compatibility)\n')
#            f.write(f'{"-"*50}\n')
#            f.write(f'В autoparts_compatibility: {len(grouped[i])} шт.\n\n')
#            autoparts_compatibility_count_list.append(len(grouped[i]))
#            freq_iter = 1
#            for value in grouped[i]:
#                print(f'\tGet search frequency for {freq_iter} of {len(grouped[i])} queries')
#                freq = get_farpost_search_freq(value, dir_id)
#                value_index = grouped[i].index(value)
#                grouped[i][value_index] = f'{freq}\t{value}'
#                freq_iter += 1
#            grouped[i] = natsort.natsorted(grouped[i], reverse=True) #сортируем фразы по частотности. Использую natsort, так как дефолтная сортировка в натуральную сортировку не умеет
#            for value in grouped[i]:
#                f.write(f'{value} (фраза)\n')
#            f.write('\n\n')
    i += 1
