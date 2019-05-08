#я пытался разобраться, что тут делается, но не смог:(

'''
Собирает леммы из списка объявлений и товаров
Вход: список объявлений и вьюдиров
Выход: файл с id-шниками, соответствующими им леммами и каунтами по леммам
'''

import urllib.request
import urllib.parse
import re
import json

#Получаем список URL'ов физ файла
url_file = input('Enter file with URLs: ')
result_file = input('Enter result file: ')
url_templ = input('Enter URL to «/+/» to count actuals and archives: ')

with open(url_file, 'r') as f:
    url_list = f.read().splitlines()

def get_count_actual_bul(model):
    '''
    Получает количество актуальных вьюбулов
    Вход: модель
    Выход: количество актуальных вьюбулов
    '''
    i = 0
    model_cyr_to_url = urllib.parse.quote(model) #нужна для корректной работы урлов с кириллицей
    url = url_templ + model_cyr_to_url
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
        i+=1
    except KeyboardInterrupt:
        raise
    except:
        viewbul_count = 'АХТУНГ!'
        i+=1
    return(viewbul_count)

def get_count_archive_bul(model):
    '''
    Получаем количество архивных вьюбулов
    Вход: модель
    Выход: количество актуальных вьюбулов
    '''
    i = 0
    url_templ_end = '/?status=archive' 
    model_cyr_to_url = urllib.parse.quote(model)
    url = url_templ + model_cyr_to_url + url_templ_end
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
        i+=1
    except KeyboardInterrupt:
        raise
    except:
        viewbul_count = 'АХТУНГ!'
        i+=1
    return(viewbul_count)

#Получаем лемму для каждого урла из списка урлов. Добавляем лемму в словарь и увеличиваем число лемм на 1
with open(result_file, 'w') as f:
    lemma_dict = {}
    bull_with_no_lemma_titles_dict = {}
    i = 1
    for url in url_list:
        source_page_for_lemma = urllib.request.urlopen(url)
        lemma_list = []
        model_list= []
        for line in source_page_for_lemma:
#            if lemma_list == []:
#                lemma_list = re.findall('bullLemma">(.*?)<', line.decode('cp1251')) #Find lemma for bulletin
            lemma_list_raw = re.findall('a href=".*/\+/(.*?)/', line.decode('cp1251'))
            if lemma_list_raw != []:
                lemma_list += lemma_list_raw
            if model_list == []:
                model_list = re.findall('data-field="subject" class="inplace">(.*?)<', line.decode('cp1251')) #ищем поле с моделью
        if lemma_list == []:
            lemma = 'Нет леммы'
            try:
                bull_with_no_lemma_titles_dict[url] = model_list[0]
            except:
                bull_with_no_lemma_titles_dict[url] = 'na'            
        else:
            lemma = lemma_list[len(lemma_list)-1]
#            lemma = urllib.parse.unquote_plus(lemma)
        if lemma not in lemma_dict:
            lemma_dict[lemma] = {}
        lemma_dict.get(lemma)['count_add'] = lemma_dict.get(lemma).get('count_add', 0) + 1
        lemma_count = lemma_dict.get(lemma).get('count_add')
        if 'count_actuals' not in lemma_dict.get(lemma) and lemma != 'Нет леммы':
#            count_actuals = get_count_actual_bul(lemma)
            count_actuals = 'na'
#            count_archives = get_count_archive_bul(lemma)
            count_archives = 'na'
            lemma_dict.get(lemma)['count_actuals'] = count_actuals
            lemma_dict.get(lemma)['count_archives'] = count_archives
        elif lemma == 'Нет леммы':
            lemma_dict.get(lemma)['count_actuals'] = 'na'
            lemma_dict.get(lemma)['count_archives'] = 'na'
        print(str(i) + ' of ' + str(len(url_list)) + '. ' + url + ' - ' + lemma + ' (' + str(lemma_count) + ')')
        f.write(url + ' - ' + lemma + ' (' + str(lemma_count) + ')' + '\n')
        i+=1
print()
with open(result_file, 'a') as f:
    f.write('\n' + '=======================================' + '\n'*2)
    for key, value in lemma_dict.items():
        lemma = key
        count_dicts = value
        json_counts = json.dumps(count_dicts, ensure_ascii=False) #Переводим словать в JSON для записи в файл
        f.write(lemma + ' = ' + json_counts + '\n')
    f.write('\n' + '================== НЕТ ЛЕММЫ =====================' + '\n')
    for key, value in bull_with_no_lemma_titles_dict.items():
        url = key
        model_field = value
        f.write(url + ' = ' + model_field + '\n')
    f.write('\n' + '=======================================' + '\n'*2)
    json_counts = json.dumps(lemma_dict, ensure_ascii=False) #Переводим словать в JSON для записи в файл
    f.write(json_counts)

