'''
Программа считает каунты в точной выдаче на farpost.ru
Прописаны 3 функции для счета запросов вида «товар + бренд»,«бренд» и «товар» 
Вход: файл с поисковыми запросами, URL для поиска в разделе (оканчивается на query)
Выход: файл с каунтами в точной выдаче
'''

import requests
import re

search_file = input('Enter file with search phrases: ')
brand_file = input('Enter brand file: ')
query_url = input('Enter dir URL ending with «query»: ')
result = input('Enter result file: ')


with open(search_file, 'r') as s:
    search_list = []
    for line in s:
        line = line.strip()
        search_list.append(line)

with open(brand_file, 'r') as b:
    brand_list = []
    for line in b:
	line = line.strip()
	brand_list.append(line)


#template = 'https://www.farpost.ru/auto/wheel/nuts/?query=' #Гайки
#template = 'https://www.farpost.ru/auto/caraccessories/?query=' #Автоаксессуары
#template = 'https://www.farpost.ru/auto/packs/?query=' #Багажники
#template = 'https://www.farpost.ru/auto/battery/?query=' #Аккумуляторы
#template = 'https://www.farpost.ru/auto/books-soft/?query=' #Книги
#template = 'https://www.farpost.ru/auto/audio/radio/?query=' #Магнитола
#template = 'https://www.farpost.ru/auto/sell_spare_parts/?query=' #Двигатель, бампер
#template = 'https://www.farpost.ru/auto/chemistry/motoroil/?query=' #Масла
#template = 'https://www.farpost.ru/auto/chemistry/?query=' #Автохимия
template = 'https://www.farpost.ru/service/auto/repair/?query=' #Авторемонт

def searchAll (template, search_list, brand_list): #Ищет запросы с брендом
	for item in search_list:
		i = 0
		for car in brand_list:
			i += 1
			url = template + item + '+' + car
			data = requests.get(url).text
#			with open('results.txt', 'a') as f: #выводит всю страницу и прерывает программу для отладки кода
#				f.write(data)
#			break
			x = re.findall('(\d+|\d+ \d+|\d+ \d+ \d+) предложен',data)
			noResults = re.findall('Предложения по точному запросу не найдены',data)
			if noResults == ['Предложения по точному запросу не найдены']:
				x.insert(0, '0')
			print (str(i) + '. ' + url)
			print(x)
			print()
			with open('results.txt', 'a') as f:
				f.write(item + ' ' + car + ', ')
				for j in x:
					f.write(j + ', ')
				f.write('\n')

def searchWithoutBrand(template,search_list): #Ищет запросы без брендов и суммирует результат
	i = 0
	total = 0
	for item in search_list:
		i = int(i)
		i += 1
		url = template + item
		data = requests.get(url).text
#		with open('results.txt', 'a') as f: #выводит всю страницу и прерывает программу для отладки кода
#			f.write(data)
#		break
		x = re.findall('(\d+|\d+ \d+|\d+ \d+ \d+) предложен',data)
		xitem = 0
		for count in x:
			count = count.replace(' ','')
			x[xitem] = count
			xitem += 1
		noResults = re.findall('Предложения по точному запросу не найдены',data)
		if noResults == ['Предложения по точному запросу не найдены']:
			x.insert(0, '0')
		print (str(i) + '. ' + url)
		print(x)
		print()
		with open('results.txt', 'a') as f:
			f.write(item + ', ')
			for j in x:
				f.write(j + ', ')
			f.write('\n')
			total = int(total)
			total += int(x[0])
	with open('results.txt', 'a') as f:
		f.write(str(total))
	print(str(total))

def searchWithoutItem (template,brand_list): #Ищет бренды без запросов и суммирует результат
	i = 0
	for car in brand_list:
		i = int(i)
		i += 1
		url = template + car
		data = requests.get(url).text
#		with open('results.txt', 'a') as f: #выводит всю страницу и прерывает программу для отладки кода
#			f.write(data)
#		break
		x = re.findall('(\d+|\d+ \d+|\d+ \d+ \d+) предложен',data)
		xitem = 0
		for count in x:
			count = count.replace(' ','')
			x[xitem] = count
			xitem += 1
		noResults = re.findall('Предложения по точному запросу не найдены',data)
		if noResults == ['Предложения по точному запросу не найдены']:
			x.insert(0, '0')
		print (str(i) + '. ' + url)
		print(x)
		print()
		with open('results.txt', 'a') as f:
			f.write(car + ', ')
			for j in x:
				f.write(j + ', ')
			f.write('\n')

#searchWithoutBrand(template, search_list)
searchWithoutItem(template, brand_list)
#searchAll (template,search_list,brand_list)
