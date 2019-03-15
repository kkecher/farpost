'''
Собирает число предложений по производителям автозапчастей для списка лемм и синонимов
Вход: файл с исходными фразами (леммы, синонимы, прочее). Мы просто ищем во вьюдире, поэтому может быть все, что угодно
Выход: файл с число предложений по производителям
'''

import urllib.request
import urllib
import re
import natsort


lemma_file = input('Enter file with phrases: ')
result = input('Enter result file: ')
print()

with open(lemma_file, 'r', encoding='utf-8') as f: #без encoding некорректно распознается кириллица
    lemma_list = f.readlines()


def collect_manuf(dir_url):
    '''
    Собирает число предложений по производителям автозапчастей для списка фраз
    Вход: список lemma_list с леммами и синонимами
    Выход: неочищенная строка с производителями и числом предложений
    '''
    source_page_for_page_total = urllib.request.urlopen(dir_url)
    for line in source_page_for_page_total:
        manuf_list = re.findall('id="manufacturer">(.*?)</label>', line.decode('cp1251'))
        if manuf_list != []:
            manuf_str = manuf_list[0]
            break
    manuf_str = str(manuf_str)
    return(manuf_str)

def clean_manuf_str(manuf_str):
    '''
    — Очищает грязную строку manuf_str с производителями и числом предложений
    — Модифицирует строку для конвертации в список предложений и каунтов внутри общего списка
    Вход: неочищенная строка с производителями и числом предложений
    Выход: очищенная и измененная строка с производителями и числом предложений
    '''
    manuf_str = re.sub(r'<optgroup label=""><option value="">любой</option>', r'', manuf_str) #убираем мусор
    manuf_str = re.sub(r'</optgroup><optgroup label="_____">', r'', manuf_str) #убираем мусор
    manuf_str = re.sub(r'</optgroup></select></span>', r'', manuf_str) #убираем мусор
    manuf_str = re.sub(r'</option>', r'', manuf_str) #убираем мусор
    manuf_str = re.sub(r'<option value=".*?>', r'[', manuf_str) #выделяем производителя
    manuf_str = re.sub(r' \(', r', ', manuf_str) #выделяем число предложения
    manuf_str = re.sub(r'\)', r'), ', manuf_str) #выделяем число предложений
    manuf_str = re.sub('\[', '(', manuf_str) #убираем мусор. Нет, перенести в начало нельзя
    manuf_str = re.sub(r', $', '', manuf_str) #убираем мусор. Нет, перенести в начало нельзя
    manuf_str = re.sub(r'&amp;', '&', manuf_str) #заменяем крявозябры амперсанда на амперсанд
    return(manuf_str)

def convert_manuf_str_to_list_of_lists(manuf_str):
    '''
    Конвертирует очищенная строку с производителями и числом предложений в список внутри списка
    Вход: очищенная и измененная строка с производителями и числом предложений
    Выход: list in list
    '''
    manuf_str = manuf_str[1:-1] #убираем первую и последнюю скобки
    manuf_count_list = []
    external_manuf_count_list = manuf_str.split('), (') #создаем внешний список со всей группой сочетаний «фраза + производитель»
    for string in external_manuf_count_list:
        internal_manuf_count_list = string.split(', ') #создаем внутренние списки с отдельными сочетаниеми «фраза + производитель» в каждом
        manuf_count_list.append(internal_manuf_count_list)
    manuf_count_list = sorted_manuf_count_list = natsort.natsorted(manuf_count_list, key=lambda x:x[1], reverse = True) #испльзуем natsort, так как родная сортировка Python не умеет в натуральную сортировку чисел
    return(manuf_count_list)

with open(result, 'a') as f:
    i = 1
    num_error = 0
    num_manuf = 0
    len_lemma_list = len(lemma_list)
    for lemma in lemma_list:
        print('Doing ' + str(i) + ' of ' + str(len_lemma_list))
        lemma = str(lemma[:-1]) #убираем символы переносов
        f.write(lemma + '\n' + '--------------------------------------' + '\n')
        try:
           lemma = urllib.parse.quote(lemma) #решает проблему кириллицы в урле (некорректно распознается)
           dir_url = 'https://www.farpost.ru/auto/sell_spare_parts/?query=' + lemma
           if '/?' in dir_url: #Фарпост начал по-умолчанию отправлять в город, который определился по ip, то есть Владивосток. Этот костыль это лечит и возвращает «Всю Россию»
               dir_url += '&city=0'
           else:
               dir_url += '?city=0'
           manuf_str = collect_manuf(dir_url)
           manuf_str = clean_manuf_str(manuf_str)
   #        f.write(manuf_str + '\n') #выводит очищенную строку с производителями в файл для дебага
           manuf_count_list = convert_manuf_str_to_list_of_lists(manuf_str)
           for elem in manuf_count_list:
               manuf = elem[0]
               count = elem[1]
               num_manuf += 1
               manuf = str(manuf)
               count = str(count)
               f.write(manuf + ' = ' + count + '\n')
           f.write('\n\n')
        except KeyboardInterrupt:
            raise
        except:
            f.write('АХТУНГ!\n\n\n')
            num_error += 1
        i += 1

print()
print('Собрано исходных фраз: ' + str(num_manuf))
num_group = int(round(num_manuf/200, 0))
print('Число групп в SEO-админке: ' + str(num_group))
print('Завершились с ошибкой: ' + str(num_error))
