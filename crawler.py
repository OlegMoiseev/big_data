"""
Нужно написать скрипт, который скачивает все данные прошедших президентских выборов для всех избирательных участков.

Входная точка по ссылке. Затем нужно перейти на сайты региональных избирательных комиссий.
Результаты нужно сохранить в cvs-файл, sqlite базе данных или parquet-файле.
В итоге должна получиться таблица с полями: - название региона - название ТИК - номер УИК - 20 стандартных полей
из итогового протокола
"""
import time

import bs4
import pandas as pd


def read_url(url):
    """ Читает содержимое сайта """
    import urllib.request
    with urllib.request.urlopen(url) as webpage:
        text = webpage.read().decode('cp1251')
    return text


def parse_region(bs):
    regions_list = bs.find_all('a', href=True)
    i = 26
    for region in regions_list[35 + i:-3]:
        i += 1
        df = pd.DataFrame(
            columns=["Название региона", "название ТИК", "номер УИК", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                     "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"])
        region_name = region.text
        region_url = "http://notelections.online" + region['href']
        text = read_url(region_url)
        bs = bs4.BeautifulSoup(text, 'lxml')
        tiks_list = bs.find_all('a', href=True)
        print(region_name)
        for tik in tiks_list[36:-3]:
            df = parse_TIK(tik['href'], region_name, tik.text, df)
        df.to_csv(str(i) + '.csv')


def parse_TIK(url, reg_name, tik_name, df):
    real_url = "http://notelections.online" + url
    while True:
        try:
            text = read_url(real_url)
            break
        except:
            print("EXCEPTION")

    bs = bs4.BeautifulSoup(text, 'lxml')

    # print(bs.prettify())

    label_list = bs.find_all('nobr')
    # for elem in label_list:
    #     print(elem.text)

    num_uiks = 0
    for i in range(len(label_list)):
        if label_list[i].text == '1':
            num_uiks = i
            break

    start_num = num_uiks + 2
    for i in range(num_uiks - 1):
        to_parse = label_list[1 + i].text
        # print(to_parse)
        list_to_df = [reg_name, tik_name, parse_uik_num(to_parse)]
        for j in range(start_num + i, len(label_list), num_uiks + 1):
            list_to_df.append(label_list[j].text)

        # print(list_to_df)
        l_df = pd.Series(data=list_to_df, index=df.columns)
        df = df.append(l_df, ignore_index=True)
    return df


def print_full(x):
    pd.set_option('display.max_rows', len(x))
    pd.set_option('display.max_columns', 23)

    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')


def parse_uik_num(num_str):
    num_list = num_str.split('№')
    return num_list[-1]


# Получаем текст html-страницы
text = read_url("http://notelections.online/region/izbirkom?action=show&root=0&tvd=100100084849066&vrn"
                "=100100084849062&prver=0&pronetvd=null&region=0&sub_region=0&type=227&report_mode=null")

# Подключаем парсер
bs = bs4.BeautifulSoup(text, 'lxml')

parse_region(bs)
