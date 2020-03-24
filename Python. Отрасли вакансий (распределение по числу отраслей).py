'''
Считает число объявлений по количеству указанных в них отраслях
Вход: файл в формате «[URL объявления] — ["отрасль 1","отрасль 2", etc]» (получается в скрипте «Python. Отрасли вакансий с низкоуровневого поиска.py»)
Выход: файл, отсортированный в обратном порядке, в формате «[число отраслей] = [число объявлений] = [процент объявлений]»
'''

import natsort

industry_file = input('Enter file with industries: ')
result = input('Enter result file: ')
dict_industry = {}

try:
    with open(industry_file, encoding='utf8') as f:
        for line in f:
            (key, val) = line.split(' — ')
            dict_industry[key] = val
except:
    with open(industry_file, encoding='cp1251') as f:
        for line in f:
            (key, val) = line.split(' — ')
            dict_industry[key] = val

def count_industries(dict_industry):
    '''
    Суммирует объявления с одинаковым числом отраслей
    Вход: dict_industry
    Выход: запись с числом объявлений и отраслей в конец файла results
    '''
    num_of_industries_dict = {}
    check_sum = 0
    num_of_bulletins = len(dict_industry)
    for id_, industry_ in dict_industry.items():
        industry_ = industry_[2:-3]
        industry_list = industry_.split('","')
        if len(industry_) < 3: #отрабатываем объявления без отраслей
            num_of_industries = 0
        else:
            num_of_industries = len(industry_list)
# печатает отрасли для дебага
#        print(industry_)
#        print(industry_list)
#        print(num_of_industries)
#        input('enter')
        num_of_industries_str = str(num_of_industries) + ' отраслей'
        num_of_industries_dict[num_of_industries_str] = num_of_industries_dict.get(num_of_industries_str, 0) + 1
    with open(result, 'w') as f:
        for industry, num in natsort.natsorted(num_of_industries_dict.items(), reverse=True):
            check_sum += num
            percent_of_bulletins = round(num/num_of_bulletins*100, 2)
            f.write(industry + ' = ' + str(num) + ' = ' + str(percent_of_bulletins) + '%\n')
        f.write('\n')
        if check_sum != num_of_bulletins:
            f.write('AHTUNG!!!! CHECK SUMS DON\'T EVEN\n')
            f.write('number of bulletins = ' + str(num_of_bulletins) + '\n')
            f.write('check_sum = ' + str(check_sum))
        else:
            f.write('Checksum is OK = ' + str(check_sum))

count_industries(dict_industry)
