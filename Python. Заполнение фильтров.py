'''
Подставляет в объявления указанное значение фильтра
Вход: файл со списком id объявлений, HTML значение кнопки фильтра
Выход: объявления с заполненным фильтром

ДЛЯ ЧЕКБОКСОВ НУЖНО ИЗМЕНИТЬ КОЛИЧЕСТВО ТАБОВ!

В ЧЕКБОКСАХ ЗАПОЛНЯЕТ ТОЛЬКО ОДНО ЗНАЧЕНИЕ. ВСЕ ОСТАЛЬНЫЕ НЕ СМОЖЕТ

РАБОТАЕТ ТОЛЬКО ДЛЯ НЕРАСКРЫВАЮЩИХСЯ СПИСКОВ
'''

import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

login = input('Enter farpost login: ')
password = input('Enter farpost password: ')

id_file = input('Enter file with ids: ')

with open(id_file, 'r') as f:
    id_list = f.read().splitlines()

#Авторизуемся на farpost.ru
#browser = webdriver.Chrome(executable_path='/home/arzhanov/Documents/chromedriver', chrome_options=opt) #активировать при работе в Linux, поменять путь к chromedriver при необходимости
browser = webdriver.Chrome(executable_path='D:\OneDrive\Документы\Фарпост\chromedriver.exe', options=opt) #активировать при работе в Windows
browser.get("https://www.farpost.ru/sign?")
username_field = browser.find_element_by_id("sign")
password_field = browser.find_element_by_id("password")
username_field.send_keys(login)
password_field.send_keys(password)
browser.find_element_by_id("signbutton").click()


def radiobutton():
    '''
    Заполняет значения в радиокнопках
    Вход: HTML value значения, которое нужно заполнить
    Выход: заполненное значение
    '''
    click_button = input('Enter field HTML value: ')
    path_to_click_button = "//label[@for='" + click_button + "']"
    print(path_to_click_button)
    input('OK? ')
    i = 1
    for id_bul in id_list:
        len_id_list = len(id_list)
        print('Doing ' + str(i) + ' of ' + str(len_id_list) + '. ' + 'http://farpost.ru/' + id_bul, end = '')
        while True:
            try:
                url = 'https://www.farpost.ru/bulletin/' + id_bul + '/edit'
                browser.get(url)
                alert = browser.switch_to_alert()
                alert.accept()
                browser.find_element_by_xpath(path_to_click_button).click()
                time.sleep(1)
                if browser.find_element_by_id(click_button).is_selected():
                    break
                else:
                    continue
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                try:
                    time.sleep(1)
                    browser.find_element_by_xpath(path_to_click_button).click()
                    if browser.find_element_by_id(click_button).is_selected():
                        break
                except (KeyboardInterrupt, SystemExit):
                    raise
#                except: #не знаю, зачем это
#                    continue
        i += 1
        print()

def dropdown():
    '''
    Заполняет значение для раскрывающихся полей
    В таком виде работает ОЧЕНЬ медленно. ЕСТЬ ЛОЖНЫЕ СРАБАТЫВАНИЯ
    '''
    click_button = 'В кредит, лизинг' #указано значение для дебага
    filter_link_text = 'Дополнительно' #указано значение для дебага
    path_to_click_button = "//select[@name='spectechExtra']/option[@value='" + click_button + "']"
    actions = ActionChains(browser)
    i = 1
    for id_bul in id_list:
        len_id_list = len(id_list)
        print('Doing ' + str(i) + ' of ' + str(len_id_list) + '. ' + 'http://farpost.ru/' + id_bul, end = '')
        url = 'https://www.farpost.ru/bulletin/' + id_bul + '/edit'
        browser.get(url)
        while True:
            try:
                value_is_selected = browser.find_element_by_xpath(path_to_click_button).is_selected()
                alert = browser.switch_to_alert()
                alert.accept()
                if value_is_selected:
                    i += 1
                    print()
                    break
                browser.find_element_by_link_text(filter_link_text).click()
                actions.send_keys(Keys.ENTER)
                time.sleep(1)
                actions.perform()
                time.sleep(2)
                actions.perform()
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                try:
                    time.sleep(1)
                    value_is_selected = browser.find_element_by_xpath(path_to_click_button).is_selected()
                    if value_is_selected:
                        i += 1
                        print()
                        break
                    browser.find_element_by_link_text(filter_link_text).click()
                    actions.send_keys(Keys.ENTER)
                    time.sleep(1)
                    actions.perform()
                    i += 1
                    print()
                except (KeyboardInterrupt, SystemExit):
                    raise
                except:
                    i += 1
                    print()
                    continue

#выбираем, в каком виде фильтра заполняем значение
radiobutton()
#dropdown()
