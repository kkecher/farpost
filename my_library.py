#!/usr/bin/env python3

def get_farpost_search_freq(query_url, dir_id):
    '''
    Собирает статистику локальных поисков за год
    Вход: строка в формате: {query}\t{URL, соответствующий query}; id раздела
    Выход: статистика по локальным поискам за год
    '''
    import requests
    import json
    import re
    
    query_url_1 = 'http://query-info.srv.loc/api/regexp?query=%5E'
    #query_url_2 = query
    query_url_3 = '%24&dirId='
    #query_url_4 = dir_id
    query_url_5 = '&withSubDirs=1&cityId=0&from=2019-01-01&to=2019-12-31'
    query_url = query_url.strip()
    query_url = re.sub(r'^\d+\t', '', query_url, flags=re.IGNORECASE) #удаляем старую частотность, если она есть
    query = query_url.split('\t')[0]
    query = query.replace('+', '%5C%2B').replace(' ', '+').replace('.', '%5C.').replace('\\', '%5C%5C')
    url = query_url_1 + query + query_url_3 + dir_id + query_url_5
    response = requests.get(url)
    query_json = json.loads(response.text)
    try:
        freq = query_json['queries'][0]['users']
    except:
        freq = 'АХТУНГ!!! ' + str(url)
    return(freq)

def convert_url_to_cyr(string):
    '''
    Переводит строку в URL-формате на кириллицу. Знаю, что лютый колхоз, но добиться корректного перевода стандартными функциями не смог.
    Вход: строка в URL-формате
    Выход: строка на кириллице
    '''
    string = string.replace('%E0', 'а').replace('%E1', 'б').replace('%E2', 'в').replace('%E3', 'г').replace('%E4', 'д').replace('%E5', 'е').replace('%E6', 'ж').replace('%E7', 'з').replace('%E8', 'и').replace('%E9', 'й').replace('%EA', 'к').replace('%EB', 'л').replace('%EC', 'м').replace('%ED', 'н').replace('%EE', 'о').replace('%EF', 'п').replace('%F0', 'р').replace('%F1', 'с').replace('%F2', 'т').replace('%F3', 'у').replace('%F4', 'ф').replace('%F5', 'х').replace('%F6', 'ц').replace('%F7', 'ч').replace('%F8', 'ш').replace('%F9', 'щ').replace('%FA', 'ъ').replace('%FB', 'ы').replace('%FC', 'ь').replace('%FD', 'э').replace('%FE', 'ю').replace('%FF', 'я').replace('%C0', 'А').replace('%C1', 'Б').replace('%C2', 'В').replace('%C3', 'Г').replace('%C4', 'Д').replace('%C5', 'Е').replace('%C6', 'Ж').replace('%C7', 'З').replace('%C8', 'И').replace('%C9', 'Й').replace('%CA', 'К').replace('%CB', 'Л').replace('%CC', 'М').replace('%CD', 'Н').replace('%CE', 'О').replace('%CF', 'П').replace('%D0', 'Р').replace('%D1', 'С').replace('%D2', 'Т').replace('%D3', 'У').replace('%D4', 'Ф').replace('%D5', 'Х').replace('%D6', 'Ц').replace('%D7', 'Ч').replace('%D8', 'Ш').replace('%D9', 'Щ').replace('%DA', 'Ъ').replace('%DB', 'Ы').replace('%DC', 'Ь').replace('%DD', 'Э').replace('%DE', 'Ю').replace('%DF', 'Я').replace('%21', '!').replace('%22', '"').replace('%23', '#').replace('%24', '$').replace('%25', '%').replace('%26', '&').replace('%27', '\'').replace('%28', '(').replace('%29', ')').replace('%2A', '*').replace('%2B', '+').replace('%2C', ',').replace('%2D', '-').replace('%2E', '.').replace('%2F', '/').replace('%3A', ':').replace('%3B', ';').replace('%3C', '<').replace('%3D', '=').replace('%3E', '>').replace('%3F', '?').replace('%40', '@').replace('%5B', '[').replace('%5C', '\\').replace('%5D', ']').replace('%5E', '^').replace('%5F', '_').replace('%60', '`').replace('%7B', '{').replace('%7C', '|').replace('%7D', '}').replace('%7E', '~').replace('%A1', '¡').replace('%A2', '¢').replace('%A3', '£').replace('%A4', '¤').replace('%A5', '¥').replace('%A6', '¦').replace('%A7', '§').replace('%A8', '¨').replace('%A9', '©').replace('%AA', 'ª').replace('%AB', '«').replace('%AC', '¬').replace('%AD', '­').replace('%AE', '®').replace('%AF', '¯').replace('%B0', '°').replace('%B1', '±').replace('%B2', '²').replace('%B3', '³').replace('%B4', '´').replace('%B5', 'µ').replace('%B6', '¶').replace('%B7', '·').replace('%B8', '¸').replace('%B9', '¹').replace('%BA', 'º').replace('%BB', '»').replace('%BC', '¼').replace('%BD', '½').replace('%BE', '¾').replace('+', ' ').replace(' на амур', '-на-амур')
    return(string)
