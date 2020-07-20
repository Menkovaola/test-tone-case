import urllib
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

import requests
import random
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import os

from predict_sentiment import get_polarity_coefficient
import re

USER_AGENTS = [
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/57.0.2987.110 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/61.0.3163.79 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
     'Gecko/20100101 '
     'Firefox/55.0'),  # firefox
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/61.0.3163.91 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/62.0.3202.89 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/63.0.3239.108 '
     'Safari/537.36'),  # chrome
]


def search_google(term):
    r = requests.Session()
    r.headers = {"user-agent": random.choice(USER_AGENTS)}
    address = f"https://google.ru/search?hl=ru&q={urllib.request.quote(term.encode('cp1251'))}"
    screenshot(address, 'google', term)
    res = r.get(address)

    soup = BeautifulSoup(res.content, "html.parser")

    results = []
    for i, g in enumerate(soup.find_all('div', class_='rc')):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            title = g.find('h3').text
            description = g.find('span', class_='st').text
            description = re.sub('[\W_]+', ' ', description)
            item = {
                'query': query,
                'search_engine': 'google',
                'position': i + 1,
                "title": title,
                "link": link,
                'description': description,
                'polarity': get_polarity_coefficient(description)
            }
            results.append(item)

    return results


def search_yandex(term):
    r = requests.Session()
    r.headers = {"user-agent": random.choice(USER_AGENTS)}
    address = f"https://yandex.com/search/?text={urllib.request.quote(term.encode('cp1251'))}"

    res = r.get(address)
    soup = BeautifulSoup(res.content, "html.parser")

    screenshot(address, 'yandex', term)

    results = []
    for i, g in enumerate(soup.find_all('div', class_='organic typo typo_text_m typo_line_s i-bem')):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            title = g.find('div', class_='organic__url-text').text
            description = g.find('div', class_='text-container typo typo_text_m typo_line_m organic__text').text
            description = re.sub('[\W_]+', ' ', description)
            item = {
                'query': query,
                'search_engine': 'yandex',
                'position': i + 1,
                "title": title,
                "link": link,
                'description': description,
                'polarity': get_polarity_coefficient(description)
            }
            results.append(item)

    return results


def screenshot(address, search, term):
    today = datetime.now()
    fold = today.strftime('%Y%m%d')
    if os.path.exists(fold):
        address_fold = "./" + today.strftime('%Y%m%d')
    else:
        os.mkdir("./" + today.strftime('%Y%m%d'))
        address_fold = "./" + today.strftime('%Y%m%d')

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(address)

    filename = str(f"SERP_{search}_{term}'.png")
    driver.save_screenshot(address_fold + '/' + filename)

    driver.close()


df = pd.DataFrame(columns=['query', 'search_engine', 'position', 'title', 'link', 'description', 'polarity'])

queries = ['яблоко', 'абрикос', 'киви']
for query in queries:
    time.sleep(5)
    df = df.append(search_yandex(query))
    df = df.append(search_google(query))

df.to_csv('output.csv', header=True)
df.to_excel("output.xlsx",
            sheet_name='Sheet_name_1')