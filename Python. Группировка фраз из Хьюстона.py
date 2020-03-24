#!/usr/bin/env python3

'''
Группирует фразы, полученные в «Python. Собираем URL'ы из API Хьюстона.py»
Вход: файл, полученный в «Python. Собираем URL'ы из API Хьюстона.py» и «Python. Получаем ответ сервера и собираем конечные URL'ы редиректов.py» и с добавленными частотностями. Порядок столбцов: Частотность > Фраза > URL
Выход: фразы, сгруппированные по разделам, леммам и применимости

ПРИМЕЧАНИЕ 1:
Пока что группирует только по разделам, леммам и применимости! При необходимости добавлю еще фильтры

ПРИМЕЧАНИЕ 2:
Тут используется файл соответствий id раздела - URL раздела, полученый по «Python. Чтение структуры разделов из JSON.py»
'''

import re
import pandas as pd
import statistics
import natsort

#houston_file = input('Enter file with keywords: ')
#results = input('Enter results file: ')
houston_file = 'Теги. Соответствия из Хьюстона с WS в кавычках за год.txt'
results = 'res_группировка'

dir_id_name_url_file = 'Теги. Разделы.txt'
print()

def convert_url_to_cyr(string):
    '''
    Переводит строку в URL-формате на кириллицу. Знаю, что лютый колхоз, но добиться корректного перевода стандартными функциями мне не удалось
    Вход: строка в URL-формате
    Выход: строка на кириллице
    '''
    string = string.replace('%E0', 'а').replace('%E1', 'б').replace('%E2', 'в').replace('%E3', 'г').replace('%E4', 'д').replace('%E5', 'е').replace('%E6', 'ж').replace('%E7', 'з').replace('%E8', 'и').replace('%E9', 'й').replace('%EA', 'к').replace('%EB', 'л').replace('%EC', 'м').replace('%ED', 'н').replace('%EE', 'о').replace('%EF', 'п').replace('%F0', 'р').replace('%F1', 'с').replace('%F2', 'т').replace('%F3', 'у').replace('%F4', 'ф').replace('%F5', 'х').replace('%F6', 'ц').replace('%F7', 'ч').replace('%F8', 'ш').replace('%F9', 'щ').replace('%FA', 'ъ').replace('%FB', 'ы').replace('%FC', 'ь').replace('%FD', 'э').replace('%FE', 'ю').replace('%FF', 'я').replace('%C0', 'А').replace('%C1', 'Б').replace('%C2', 'В').replace('%C3', 'Г').replace('%C4', 'Д').replace('%C5', 'Е').replace('%C6', 'Ж').replace('%C7', 'З').replace('%C8', 'И').replace('%C9', 'Й').replace('%CA', 'К').replace('%CB', 'Л').replace('%CC', 'М').replace('%CD', 'Н').replace('%CE', 'О').replace('%CF', 'П').replace('%D0', 'Р').replace('%D1', 'С').replace('%D2', 'Т').replace('%D3', 'У').replace('%D4', 'Ф').replace('%D5', 'Х').replace('%D6', 'Ц').replace('%D7', 'Ч').replace('%D8', 'Ш').replace('%D9', 'Щ').replace('%DA', 'Ъ').replace('%DB', 'Ы').replace('%DC', 'Ь').replace('%DD', 'Э').replace('%DE', 'Ю').replace('%DF', 'Я').replace('%21', '!').replace('%22', '"').replace('%23', '#').replace('%24', '$').replace('%25', '%').replace('%26', '&').replace('%27', '\'').replace('%28', '(').replace('%29', ')').replace('%2A', '*').replace('%2B', '+').replace('%2C', ',').replace('%2D', '-').replace('%2E', '.').replace('%2F', '/').replace('%3A', ':').replace('%3B', ';').replace('%3C', '<').replace('%3D', '=').replace('%3E', '>').replace('%3F', '?').replace('%40', '@').replace('%5B', '[').replace('%5C', '\\').replace('%5D', ']').replace('%5E', '^').replace('%5F', '_').replace('%60', '`').replace('%7B', '{').replace('%7C', '|').replace('%7D', '}').replace('%7E', '~').replace('%A1', '¡').replace('%A2', '¢').replace('%A3', '£').replace('%A4', '¤').replace('%A5', '¥').replace('%A6', '¦').replace('%A7', '§').replace('%A8', '¨').replace('%A9', '©').replace('%AA', 'ª').replace('%AB', '«').replace('%AC', '¬').replace('%AD', '­').replace('%AE', '®').replace('%AF', '¯').replace('%B0', '°').replace('%B1', '±').replace('%B2', '²').replace('%B3', '³').replace('%B4', '´').replace('%B5', 'µ').replace('%B6', '¶').replace('%B7', '·').replace('%B8', '¸').replace('%B9', '¹').replace('%BA', 'º').replace('%BB', '»').replace('%BC', '¼').replace('%BD', '½').replace('%BE', '¾').replace('+', ' ').replace(' на амур', '-на-амур')
    return(string)

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
        word = line.split('\t')[1]
        url = line.split('\t')[2]
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

with open(results, 'w') as f:
    prev_dir_url = ''
    prev_lemma_url = ''
    prev_autoparts_compatibility_url = ''
    dir_count_list = []
    lemma_count_list = []
    autoparts_compatibility_count_list = []
    min_count = 5
    i = 0
    for col in grouped.keys():
        dir_url = col[0]
        lemma_url = col[1]
        autoparts_compatibility_url = col[2]
        #В список разделов записываем все, кроме корневого, у которых >min_count фраз
        if dir_url != prev_dir_url and dir_url != '' and dir_url != 'https://www.farpost.ru' and len(grouped[i]) > min_count:
            prev_dir_url = dir_url
            dir_id = dir_dict[dir_url][0]
            dir_name = dir_dict[dir_url][1]
            f.write(f'{"#"*80}\n')
            f.write(f'{dir_name}\t{dir_url}\t{dir_id} (раздел)\n')
            f.write(f'{"#"*80}\n')
            f.write(f'В корне раздела: {len(grouped[i])} шт.\n\n')
            dir_count_list.append(len(grouped[i]))
            grouped[i] = natsort.natsorted(grouped[i], reverse=True) #сортируем фразы по частотности. Использую natsort, так как дефолтная сортировка в натуральную сортировку не умеет
            for value in grouped[i]:
                f.write(f'{value} (фраза)\n')
            f.write('\n\n')

        #Записываем в файл только те леммы в которых >min_count фраз
        if lemma_url != prev_lemma_url and lemma_url != '' and len(grouped[i]) > min_count:
            prev_lemma_url = lemma_url
            f.write(f'{"-"*50}\n')
            f.write(f'{lemma_url} (лемма)\n')
            f.write(f'{"-"*50}\n')
            f.write(f'В лемме: {len(grouped[i])} шт.\n\n')
            lemma_count_list.append(len(grouped[i]))
            grouped[i] = natsort.natsorted(grouped[i], reverse=True) #сортируем фразы по частотности. Использую natsort, так как дефолтная сортировка в натуральную сортировку не умеет
            for value in grouped[i]:
                f.write(f'{value} (фраза)\n')
            f.write('\n\n')

        #В список autoparts_compatibility записываем все, в которых >min_count:
        if autoparts_compatibility_url != prev_autoparts_compatibility_url and autoparts_compatibility_url != '' and len(grouped[i]) > 5:
            prev_autoparts_compatibility_url = autoparts_compatibility_url
            f.write(f'{"-"*50}\n')
            f.write(f'{autoparts_compatibility_url} (autoparts_compatibility)\n')
            f.write(f'{"-"*50}\n')
            f.write(f'В autoparts_compatibility: {len(grouped[i])} шт.\n\n')
            autoparts_compatibility_count_list.append(len(grouped[i]))
            grouped[i] = natsort.natsorted(grouped[i], reverse=True) #сортируем фразы по частотности. Использую natsort, так как дефолтная сортировка в натуральную сортировку не умеет
            for value in grouped[i]:
                f.write(f'{value} (фраза)\n')
            f.write('\n\n')
        i += 1

    f.write(f'Медианное количество фраз в разделах: {statistics.median(dir_count_list)}\n')
    f.write(f'Медианное количество фраз в леммах: {statistics.median(lemma_count_list)}\n')
    f.write(f'Медианное количество фраз в autoparts_compatibility: {statistics.median(autoparts_compatibility_count_list)}\n')
    f.write(f'Общее количество фраз: {sum(dir_count_list) + sum(lemma_count_list) + sum(autoparts_compatibility_count_list)}\n')
