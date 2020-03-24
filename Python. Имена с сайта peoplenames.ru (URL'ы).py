#!/usr/bin/env python3

'''
Собирает имена и их синонимы из peoplenames.ru
Вход: список URL'ов
Выход: список имен с синонимами
'''

import requests
import re

#url_list = input('Enter file with URLs: ')
#result = input('Enter result file: ')

url_list = 'res_peoplename_url'
result = 'res_peoplename_name'

with open(url_list, 'r', encoding='utf8') as f:
    url_list = f.read().splitlines()

def get_name(source_code):
    name = re.findall(r'<h1>(.*?)<', source_code)
    if name == []:
        name = ''
    else:
        name = name[0]
    return(name)

def get_synonyms(source_code):
    synonyms = re.findall(r'Производные:(.*?)<\/p>', source_code)
    if synonyms == []:
        synonyms = ''
    else:
        synonyms = synonyms[0]
        synonyms = re.sub(r'<a href="\/name\/.*?>', '', synonyms, flags=re.IGNORECASE) 
        synonyms = re.sub(r'<\/a>', '', synonyms, flags=re.IGNORECASE) 
        synonyms = re.sub(r'<\/b>', '', synonyms, flags=re.IGNORECASE) 
    return(synonyms)

def get_other_languages(source_code):
    other_language_form = re.findall(r'"name__languages">(?:.*\n){1,}.*?<\/table>', source_code)
    if other_language_form == []:
        other_language_form = ''
    else:
        other_language_form = other_language_form[0]
        other_language_form = re.sub(r'"name__languages">\n', '', other_language_form, flags=re.IGNORECASE)
        other_language_form = re.sub(r'.*<\/?tr>', '', other_language_form, flags=re.IGNORECASE)
        other_language_form = re.sub(r'.*<\/table>', '', other_language_form, flags=re.IGNORECASE)
        other_language_form = re.sub(r'.*?<td>', '', other_language_form, flags=re.IGNORECASE)
        other_language_form = re.sub(r'<\/td>\n', ', ', other_language_form, flags=re.IGNORECASE)
        other_language_form = re.sub(r'\n', ', ', other_language_form, flags=re.IGNORECASE)
        other_language_form = re.sub(r', ,', ',', other_language_form, flags=re.IGNORECASE)
        other_language_form = re.sub(r'  ', ' ', other_language_form, flags=re.IGNORECASE)
        other_language_form = re.sub(r' $', '', other_language_form, flags=re.IGNORECASE)
        other_language_form = re.sub(r'\s?,$', '', other_language_form, flags=re.IGNORECASE)
    return(other_language_form)


i = 1
for url in url_list:
    print (f'Doing {i} of {len(url_list)} urls')
    try:
        source_code = requests.get(url)
        source_code = source_code.text
        name = get_name(source_code)
        synonyms = get_synonyms(source_code)
        other_language_form = get_other_languages(source_code)
    except KeyboardInterrupt:
        raise
    except:
        name = 'АХТУНГ'
        other_language_forms = 'АХТУНГ'
        synonyms = 'АХТУНГ'
    i += 1
    with open(result, 'a') as f:
        try:
            f.write(f'{name} - {url}\n')
        except KeyboardInterrupt:
            raise
        except:
            name = 'АХТУНГ'
            f.write(f'{name} - {url}\n')
        f.write('-'*35 + '\n')
        f.write('Производные: ')
        try:
            f.write(f'{synonyms}')
        except KeyboardInterrupt:
            raise
        except:
            synonyms = 'АХТУНГ'
            f.write(f'{synonyms}')
        f.write('\n')
        f.write('Другие языки: ')
        try:
            f.write(f'{other_language_form}')
        except KeyboardInterrupt:
            raise
        except:
            other_language_form = 'АХТУНГ'
            f.write(f'{other_language_form}')
        f.write('\n'*2)
