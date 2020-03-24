# -*- coding: utf-8 -*-

import json
import requests

print()
search = input("Введите поисковой запрос. Например,\nbq(must: [tq('directoryId', '281'), tq('type.lemma', 'мотохимия')]): ")
res = input('Введите название файла, куда записать результаты: ')

url = 'http://search-actual.srv.loc/rest/v1.4/stream'
headers = {
    # важное поле, по которому на стороне поиска можем определить, кто отправил запрос
    'User-Agent': '@glazkov' 
}
data = {
    'zone': 'default',
    'select': 'directoryId,cityId,subject',
    'q': search
#    'q': "bq(must: [tq('directoryId', '281'), tq('type.lemma', 'мотохимия')])"
#    'q': 'bq(must: [tq("directoryId", "235"), tq("cityId", "1")])'
}

print()
print('Собираю. Обожди…')

r = requests.post(url, headers=headers, data=data, stream=True)

with open(res, 'w') as f:
    for line in r.iter_lines():
    
        # skip ^Z
        if line == b'\x1a':
            continue
        
        decoded_line = line.decode('utf-8')
    
        doc_json = json.loads(decoded_line)
        values = (
            doc_json.get('cityId', 'unknown'),
            doc_json.get('directoryId', 'unknown'),
            doc_json.get('subject', 'unknown')
        )
        subject = values[2]
        subject = subject.replace('&quot;','"')
        subject = subject.replace('&amp;','&')
        subject = subject.replace('&shy;','')
        subject = subject.replace('&gt;','>')
        subject = subject.replace('&#039;','\'')
        f.write(f'{subject}\n')
