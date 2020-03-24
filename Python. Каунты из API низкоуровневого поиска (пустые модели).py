#!/usr/bin/env python3

'''
Собирает каунты из API низкоуровневого поиска
Вход: файл со списком моделей, файл с результатами. Пользуюсь редко, поэтому URL прописываю в коде.
Выход: файл с каунтами
'''

import urllib.request
import timeit

models_file = input('Введите файс с моделями: ')
results = input('Введите файл с результатами: ')
print()

start_time = timeit.default_timer()

with open (models_file, 'r', encoding='utf8') as f:
    models = f.read().splitlines()

counts = {}
i = 0
for model in models:
    i += 1
    print(f'Doing {i} of {len(models)}')
    try:
        model_url = urllib.parse.quote(model)
    
        url_actual = 'http://search-actual.srv.loc/rest/v1.4/count/?query=directoryId%20in%20%28253%2C%20282%2C%20519%2C%20516%2C%20855%29%20and%20model.index%20%3D%20%27' + str(model_url) + '%27&sort=&zone=default'
        url_archive = 'http://search-actual.srv.loc/rest/v1.4/count/?query=directoryId%20in%20%28253%2C%20282%2C%20519%2C%20516%2C%20855%29%20and%20model.index%20%3D%20%27' + str(model_url) + '%27&sort=&zone=archive'
    
        source_page_for_count_actual = urllib.request.urlopen(url_actual)
        source_page_for_count_archive = urllib.request.urlopen(url_archive)
    
        count_actual = int(source_page_for_count_actual.read())
        count_archive = int(source_page_for_count_archive.read())
    
        counts[model] = (count_actual, count_archive)
    except Exception:
        counts[model] = ('АХТУНГ', 'АХТУНГ')

with open (results, 'w') as f:
    for model, count in counts.items():
        f.write(f'{model} = {count[0]} = {count[1]}\n')

print()
stop_time = timeit.default_timer()
program_time = stop_time-start_time
program_time_hour = int(program_time // 3600)
program_time_min = int((program_time - program_time_hour*3600) // 60)
program_time_sec = int(round(program_time - program_time_min*60 - program_time_hour*3600))
print('I have finished your dirty wish.')
print(f'It took {program_time_hour}:{program_time_min}:{program_time_sec} of my life, silly bastard!') 
print()
