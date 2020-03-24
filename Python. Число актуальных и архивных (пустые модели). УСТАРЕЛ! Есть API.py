'''
ПРОВЕРИТЬ КОРРЕКТНОСТЬ РАБОТЫ! КАЖЕТСЯ, В URL ГДЕ-ТО НЕ ДОПИСЫВАЕТСЯ / ПЛЮСОМ ЛЕММЫ
Собирает количество актуальных и архивных предложений в разделе
Вход: файл со списком моделей, URL раздела с «/+/» на конце
Выход: файл со списком урлов, числом актуальных предложений и числом предложений в архиве

Считает каунты во вьюдире, поэтому объявления под пессимизацией НЕ подсчитаются.
'''

import urllib.request
import urllib.parse
import re

models = input('Enter file with models: ')
dir_url = input('Enter URL finished by «/+/»: ')
results = input('Enter result file: ')
#dir_url = 'https://www.farpost.ru/auto/moto/sale/+'
#https://www.farpost.ru/auto/moto/spares/+
#https://www.farpost.ru/auto/moto/atv/+
#https://www.farpost.ru/auto/moto/moped/+
#https://www.farpost.ru/auto/moto/snow/+

with open(models) as f:
    list_models = f.read().splitlines()

def get_count_actual_bul(): #получаем количество актуальных вьюбулов
    '''
    Получает количество актуальных вьюбулов
    Вход: список моделей list_models
    Выход: словарь с моделями и количеством актуальных предложений по ним
    '''
    i = 0
    list_model_url = []
    dict_model_count = {}
    for model in list_models: #создаем урлы для моделей
        model_cyr_to_url = urllib.parse.quote(model) #если модель на кириллице, изменяем ее в URL-формат
        url = dir_url + model_cyr_to_url + '/?city=0' #добавляем /?city=0, чтобы считать по всей России
        list_model_url.append(url)
    for url in list_model_url:
        try:
            source_page_for_page_total = urllib.request.urlopen(url)
            for line in source_page_for_page_total:
                    viewbul_count_list = re.findall('itemsCount.*data-count="(.*?)"', line.decode('cp1251'))
                    if viewbul_count_list != []:
                            viewbul_count = viewbul_count_list[0]
                            break
            if viewbul_count_list != []:
                    viewbul_count = int(viewbul_count_list[0])
            else:
                    viewbul_count = 0
            dict_key_model_url = dir_url + list_models[i]
            dict_model_count[dict_key_model_url] = viewbul_count
            print(str(i+1) + ' of ' + str(len(list_models)) + '. ' + list_models[i] + ' = ' + str(viewbul_count))
            i+=1
        except KeyboardInterrupt:
            raise
        except:
            dict_model_count[dict_key_model_url] = 'Ахтунг!!!'
            print(str(i+1) + ' of ' + str(len(list_models)) + '. ' + list_models[i] + ' = ' + 'Ахтунг!!!')
            i+=1
    print('Done with actuals')
    print()
    return(dict_model_count)

def get_count_archive_bul(): #Count number of archive bulletins
    '''
    Получает количество архивных вьюбулов
    Вход: список моделей list_models
    Выход: словарь с моделями и количеством архивных предложений по ним
    '''
    i = 0
    list_model_url = []
    dict_model_count = {}
    dir_url_end = '/?status=archive' 
    for model in list_models: #создаем урлы для моделей
        model_cyr_to_url = urllib.parse.quote(model) #если модель на кириллице, то изменяем ее в URL-формат
        url = dir_url + model_cyr_to_url + dir_url_end + '&city=0'
        list_model_url.append(url)
    i = 0
    for url in list_model_url:
        try:
            source_page_for_page_total = urllib.request.urlopen(url)
            for line in source_page_for_page_total:
                    viewbul_count_list = re.findall('itemsCount.*data-count="(.*?)"', line.decode('cp1251'))
                    if viewbul_count_list != []:
                            viewbul_count = viewbul_count_list[0]
                            break
            if viewbul_count_list != []:
                    viewbul_count = int(viewbul_count_list[0])
            else:
                    viewbul_count = 0
            dict_key_model_url = dir_url + list_models[i]
            dict_model_count[dict_key_model_url] = viewbul_count
            print(str(i+1) + ' of ' + str(len(list_models)) + '. ' + list_models[i] + ' = ' + str(viewbul_count))
            i+=1
        except KeyboardInterrupt:
            raise
        except:
            dict_model_count[dict_key_model_url] = 'Ахтунг!!!'
            print(str(i+1) + ' of ' + str(len(list_models)) + '. ' + list_models[i] + ' = ' + 'Ахтунг!!!')
            i+=1
    print('Done with archive')
    print()
    return(dict_model_count)

dict_model_actual_count = get_count_actual_bul()
dict_model_archive_count = get_count_archive_bul()

with open(results, 'w') as f:
    i = 1
    try:
        for key, value in dict_model_actual_count.items():
            f.write(str(i) + '. ' + key + '# = ' + str(value) + ' = ' + str(dict_model_archive_count[key]) + '\n')
            f.write(str(i) + '. ' + key + '?status=archive' + '# = ' + str(dict_model_archive_count[key]) + '\n')
            i+=1
    except:
        f.write(str(i) + ' = ' + 'Ахтунг!!!')
        i+=1
