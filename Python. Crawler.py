'''
IN PROGRESS!
ДЛЯ АДЕКВАТНОЙ РАБОТЫ НУЖНО КАК МИНИМУМ МНОГО ПОТОКОВ
'''

import urllib.request
import re

#dir_url = input('Enter viewdir URL or file: ')
dir_url = 'https://www.farpost.ru/dalnegorsk/job/vacancy/'
#results = input('Enter results file: ')
results = 'res'
print()

exclude_elements_list = ['farpost', '.html', 'http', 'page=', '#']

open(results, 'w').close()

#if '/?' in mode: #Фарпост начал по-умолчанию отправлять в город, который определился по ip, то есть Владивосток. Этот костыль это лечит и возвращает «Всю Россию»
#    mode += '&city=0'
#else:
#    mode += '?city=0'

def collect_urls(dir_url):
    '''
    Собирает заголовки объявлений из вьюдира
    Вход: URL вьюдира
    Выход: список из заголовков
    '''
    urls_list_raw = []
    urls_list = []

    print('Results will be written in file «' + str(results) + '»')
    print()

    source_page_for_urls = urllib.request.urlopen(dir_url)
    for line in source_page_for_urls:
        urls_list_raw += re.findall('href="(.*?)"', line.decode('cp1251'))
    for url in urls_list_raw:
        flag_remove = 0
        for exclude_element in exclude_elements_list:
            if exclude_element in url:
                flag_remove = 1
        if flag_remove == 0:
            urls_list.append(url)
    with open(results, 'a') as f:
        for url in urls_list:
            f.write(str(url) + '\n')
    return(urls_list)

urls_list = collect_urls(dir_url)
for url in urls_list:

#            if 'img' not in title:
#                title = title.replace('&quot;','"')
#                title = title.replace('&amp;','&')
#                title = title.replace('&shy;','')
#                title = title.replace('&gt;','>')
#                title = title.replace('&#039;','\'')
#                titles_list.append(title)
#        i+=1
#        urls_list_raw = []
#    return(titles_list)

#def collect_titles():
#    '''
#    Собирает заголовки объявлений из вьюдира
#    Вход: URL вьюдира
#    Выход: список из заголовков
#    '''
#    dir_url = mode
#    i = 1
#    titles_list_raw = []
#    titles_list = []
#
#    source_page_for_page_total = urllib.request.urlopen(dir_url) #Get number of viewbuls to count number of pages
#    for line in source_page_for_page_total:
#        viewbul_count_list = re.findall('itemsCount.*data-count="(.*?)"', line.decode('cp1251'))
#        if viewbul_count_list != []:
#            viewbul_count = viewbul_count_list[0]
#            break
#    viewbul_count = int(viewbul_count_list[0])
#    page_total = (viewbul_count // 50) + 1 #Get integer division plus 1 page
#    print('Found ' + str(page_total) + ' pages')
#    if page_total > 180:
#        page_total = 180
#        print()
#        print('DOING FIRST 180 PAGES')
#    print('Results will be written in file «' + str(results) + '»')
#    print()
#
#    while i <= page_total:
#        print('Doing page ' + str(i) + ' out of ' + str(page_total))
#        if '/?' in dir_url:
#            source_page_for_titles = urllib.request.urlopen(dir_url + '&page=' + str(i))
#        else:
#            source_page_for_titles = urllib.request.urlopen(dir_url + '?page=' + str(i))
#        for line in source_page_for_titles:
#            titles_list_raw += re.findall('.html.*?>(.*?)</a>', line.decode('cp1251'))
#        for title in titles_list_raw:
#            if 'img' not in title:
#                title = title.replace('&quot;','"')
#                title = title.replace('&amp;','&')
#                title = title.replace('&shy;','')
#                title = title.replace('&gt;','>')
#                title = title.replace('&#039;','\'')
#                titles_list.append(title)
#        i+=1
#        titles_list_raw = []
#    return(titles_list)
#
#def collect_titles_from_file():
#    '''
#    Собирает заголовки объявлений из URL-ов в файле.
#    Вход: текстовый файл 
#    Выход: список из заголовков
#    '''
#    titles_file = mode
#    titles_list_raw = []
#    titles_list = []
#    i = 1
#    with open(titles_file, 'r') as f:
#        url_list = f.readlines()
#    print('Found ' + str(len(url_list)) + ' URLs')
#    print('Результаты будут выведены в файл «' + str(results) + '»')
#    print()
#    for url in url_list:
#        print('Doing URL ' + str(i) + ' out of ' + str(len(url_list)))
#        source_page_for_titles = urllib.request.urlopen(url)
#        for line in source_page_for_titles:
#            title = re.findall('data-field="subject" class="inplace">(.*?)<nobr>', line.decode('cp1251'))
#
#            if title != []:
#                break
#        if title == []:
#            titles_list_raw += [url]
#        else:
#            titles_list_raw += title
#        i+=1
#    for title in titles_list_raw:
#        title = title.replace('&quot;','"')
#        title = title.replace('&amp;','&')
#        title = title.replace('&shy;','')
#        title = title.replace('&gt;','>')
#        title = title.replace('&#039;','\'')
#        titles_list.append(title)
#    return(titles_list)
#
#if 'http' in mode:
#    titles_list = collect_titles()
#else:
#    titles_list = collect_titles_from_file()
#with open(results, 'w') as f:
#    for title in titles_list:
#        f.write(title + '\n')
#
