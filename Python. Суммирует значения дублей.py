#!/usr/bin/env python3

'''
Суммирует значения строк-дублей и оставляет уникальные значения
Вход: файл со строками-дублями и числами (делитель = \t)
Выход: уникальные строки с суммированными значениями
'''

#dup_file = input('Enter file with duplicates: ')
#result = input('Enter result file: ')
dup_file = 'Теги. Локальные поиски v2.txt'
result = 'res'

with open(dup_file, 'r', encoding='cp1251') as f:
    dup_list = []
    for phrase_freq in f:
        phrase_freq = phrase_freq.strip()
        phrase_freq_list = phrase_freq.split('\t')
        phrase_freq_tuple = tuple(phrase_freq_list)
        dup_list.append(phrase_freq_tuple)

dup_dict = {}
for phrase_freq_tuple in dup_list:
    phrase = phrase_freq_tuple[0]
    freq = int(phrase_freq_tuple[1])
    dup_dict[phrase] = dup_dict.get(phrase, 0) + freq

with open(result, 'w') as f:
    for phrase, freq in dup_dict.items():
        f.write(f'{phrase}\t{freq}\n')
