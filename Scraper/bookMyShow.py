# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 01:48:04 2026

@author: karan
"""

print('Hello World')

import undetected_chromedriver as uc
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# chrome_options = Options()
# service = Service("E:/DevEnv/chromedriver-win64/chromedriver.exe")

chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

driver = uc.Chrome(options=chrome_options)

driver.get('https://in.bookmyshow.com/explore/home/bengaluru')
time.sleep(3)

eventsButton = driver.find_element(By.XPATH, '//*[@id="super-container"]/div/div[1]/div[2]/div/div/div[1]/div/a[3]')
eventsButton.click()

#firstResult = driver.find_element(By.XPATH, '//*[@id="super-container"]/div[2]/div[3]/div[2]/div[3]/div/div/div[2]/a[1]')
#firstResult

soup = BeautifulSoup(driver.page_source, 'lxml')
all_events_in_pg = soup.find_all('div', class_ = 'sc-133848s-3 sc-133848s-5 gMFRkd eUdoic')
len(all_events_in_pg)

links = []
while True:
    for event in all_events_in_pg:
        link = event.find_all('a', class_ = 'sc-133848s-11 sc-1ljcxl3-1 cnWwcT buMnJU')
        for a in link:
            links.append(a.get('href'))

    driver.execute_script('window.scrollBy(0,600)')
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    all_events_in_pg = soup.find_all('div', class_ = 'sc-133848s-3 sc-133848s-5 gMFRkd eUdoic')

    links2 = list(set(links))

    if len(links2) > 200:
        break


links2
len(links2)

import pandas as pd

df = pd.DataFrame(links2, columns=['Links'])
df.to_csv('D:/linksFullRange.csv')

del df
del links

columns = [
    "Name of the event",
    "Date",
    "Time",
    "Event description",
    "Type of event",
    "Location (Bangalore only)",
    "Registration Link",
    #"Ideal group size",
    "Estimated duration",
    "Genre",
    "Age Limit",
    "Language",
    "Page Link",
    "Poster Link",
    "Price",
    "Status"
]

# Create empty DataFrame
df = pd.DataFrame(columns=columns)

print(df)

for link in links2:
    try:
        driver.get(link)
    
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        price = soup.find_all('span', class_ = 'sc-1qdowf4-0 dpaUna')
        price
        
        about = soup.find_all('div', class_ = 'sc-omw9zj-0 ieIdLv')
        about[0].text
        types = soup.find_all('div', class_ = 'sc-133848s-2 sc-133848s-12 irZrCs hoNDWQ')
        types[0].text
        img_link = soup.find('img', class_ = 'sc-1yixhh3-3 ZzXHE')
        img_link.get('src')
        #testing start
        card = soup.find_all('div', class_ = 'sc-133848s-3 sc-133848s-5 gMFRkd eApAHD')
        info = card[0].find_all('div', class_ = 'sc-1mrya4h-0 iqPDjL')
        info
        
        data_dict = {}
        for line in info:
            if line.find('img', src = 'https://assets-in.bmscdn.com/nmcms/synopsis/calendar.png'):
                data_dict['date'] = line.text
            elif line.find('img', src = 'https://assets-in.bmscdn.com/nmcms/synopsis/time.png'):
                data_dict['time'] = line.text
            elif line.find('img', src = 'https://assets-in.bmscdn.com/nmcms/synopsis/duration.png'):
                data_dict['duration'] = line.text
            elif line.find('img', src = 'https://assets-in.bmscdn.com/nmcms/synopsis/key_info/age_limit.png'):
                data_dict['age limit'] = line.text
            elif line.find('img', src = 'https://assets-in.bmscdn.com/nmcms/synopsis/genre.png'):
                data_dict['genre'] = line.text
            elif line.find('img', src = 'https://assets-in.bmscdn.com/nmcms/synopsis/language.png'):
                data_dict['language'] = line.text
            elif line.find('img', src = 'https://assets-in.bmscdn.com/nmcms/synopsis/location.png'):
                data_dict['location'] = line.text
        #testing end
    
        name_of_the_event = soup.find('h1', class_ = 'sc-7o7nez-0 fESPan').text
        reg_link = soup.find('a', class_ = 'sc-pxa29k-1 hTHppF').get('href')
    
        df.loc[len(df)] = [
            name_of_the_event,
            data_dict.get('date', None),
            data_dict.get('time', None),
            about[0].text,
            types[0].text,
            data_dict.get('location', None),
            reg_link,
            #group_size,
            data_dict.get('duration', None),
            data_dict.get('genre', None),
            data_dict.get('age limit', None),
            data_dict.get('language', None),
            link,
            img_link.get('src'),
            price[0].text,
            price[1].text
        ]
    except Exception as e:
        print(f"Skipped {link} due to error: {e}")
        continue

df.to_csv('D:/events.csv')
print(name_of_the_event)
