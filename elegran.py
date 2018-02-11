#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 07:28:14 2018

@author: tmontagni
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# going to the page url
def goto(url):
	driver.get(url)

# close the browser
def close():
	driver.close()

# initiate driver - either in headless or not
def init_driver():
#    options = Options()
#    options.add_argument('--headless')
#    options.add_argument('--disable-gpu')
#    driver = webdriver.Chrome("/Applications/chromedriver", chrome_options = options)
    driver = webdriver.Chrome("/Applications/chromedriver")
    return driver

# get all the htmls from the page and saving them
def get_htmls():
    list_links = driver.find_elements_by_tag_name('a')
    for i in list_links:
        list1.append(i.get_attribute('href'))

	
    series = pd.Series(list1)
    return series

# cleaning htmls from garbage
def clean_data(df):
	df = df[df.str.contains("listings") == True]
	df = df.drop_duplicates()
	return df

#driver goes to processed htmls and takes all the fucking data and saves in csv
def get_elegran_data(df):
    for html in processed_htmls:

        driver.get(html)
        try:
            address = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/div[2]/div[1]/h1/a')
        except:
            address = "not available"
        try:
            description = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/div[1]/div[5]/div/div/p')
        except:
            pass
        try:
            price = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/div[2]/div[2]/dl[1]/dd/em/span')  
            price = price.str.replace(',','')
            price = price.str.replace('$','')
        except:
            pass
        try:
            df = df.append({'address': address.get_attribute('text'), 'description': description.text.split()[:10], 'price': price.text}, ignore_index=True)
        except:
            pass

    return df

# iterate through a certain amount of pages and collect the htmls on the pages.
def next_page_urls():
    goto('https://www.elegran.com/nyc/search/sales')
    wait = WebDriverWait(driver, 60)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="list-search"]/div/div/div/div[7]/ul/li[1]/div[2]/h4')))
    time.sleep(3)
    get_htmls()
    for i in numbers:
        goto('https://www.elegran.com/nyc/search/sales/?page=' + i)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="list-search"]/div/div/div/div[7]/ul/li[1]/div[2]/h4')))
        time.sleep(3)
        get_htmls()

def sort():
	menu = driver.find_element_by_xpath('//*[@id="search-bar"]/div/div[1]/form/div[1]/div/a')
	menu.click()
	order = driver.find_element_by_xpath('//*[@id="search-bar"]/div/div[1]/form/div[1]/div/ul/li[5]')
	order.click()
	time.sleep(10)


numbers = list(range(2, 591))
numbers = [str(x) for x in numbers]
process_data = pd.DataFrame(data = None, index = [0], columns = ['address', 'description', 'price'], dtype = None, copy = False)
list1 = []

######################
driver = init_driver()
goto("https://www.elegran.com/nyc/search/sales")
next_page_urls()
processed_html = get_htmls()
processed_htmls = clean_data(processed_html)
Final_data = get_elegran_data(process_data)
Final_data.to_csv('elegran.csv', encoding = 'utf-8')
close()
######################