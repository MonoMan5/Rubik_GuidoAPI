#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 21:51:56 2018

@author: tmontagni
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
from random import randint
import pandas as pd


# going to the page url
def goto(url):
	driver.get(url)

# close the browser
def close():
	driver.close()

# initiate driver - either in headless or not
def init_driver():
    service_args = [
            '--proxy = 45.77.26.129',
            '--proxy-type = https',
            ]

    options = Options()
    #options.add_argument('--headless')
    #options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--profile-directory=Default')
    options.add_argument("--incognito")
    options.add_argument("--disable-plugins-discovery");
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome("/Applications/chromedriver", service_args = service_args)
    return driver

def clean_data(dt):
	for i in dt:
		cleaned = dt.str.split(',').str[0]
		return cleaned
	
def create_urls(dt):
    for i in dt:
        urls = 'https://streeteasy.com/building/' + dt
        urls = urls.dropna(axis=0, how='all')
        urls = urls.drop_duplicates()
        return urls

def delay():
	timeDelay1 = random.randrange(6,15)
	time.sleep(timeDelay1)


def scrape_data(dt,fr):
    for i in dt:
        time.sleep(2)
        goto(i)
        delay()
        address = i.replace('-',' ')
        address = address.replace('https://streeteasy.com/building/', '')
        try:
            building_streeteasy_address = driver.find_element_by_xpath("""//*[@id="content"]/main/div[4]/article[2]/h2""").text
        except:
            building_streeteasy_address = "URL was not found"
        try:
            building_active_rentals = driver.find_element_by_xpath("""//*[@id="present_rentals"]""").text
        except:
            building_active_rentals = "0 active rentals (N/A per ft² avg, N/A avg price)"
        try:
            building_present_sales = driver.find_element_by_xpath("""//*[@id="present_sales"]""").text
        except:
            building_present_sales = "0 active sale (N/A per ft² avg, N/A avg price)"
        try:
            building_past_sales = driver.find_element_by_xpath("""//*[@id="all_past_sales"]/a""").text
        except:
            building_past_sales = "0 past sales (N/A per ft² avg, N/A avg price)"
        try:
            building_past_rentals = driver.find_element_by_xpath("""//*[@id="all_past_rentals"]/a""").text
        except:
            building_past_rentals = "0 past rentals (N/A per ft² avg, N/A avg price)"
        try:
            building_amenities = driver.find_element_by_xpath("""//*[@id="content"]/main/div[4]/article[3]/section[3]/div/div""").text.replace("\n", "; ")
        except:
            building_amenities = "no building amenities"
        try:
            building_facts = driver.find_element_by_xpath("""//*[@id="content"]/main/div[4]/article[2]/div[1]""").text
        except:
            building_facts = "no building facts" 
        try:
            building_neighborhood = driver.find_element_by_xpath("""//*[@id="content"]/main/div[4]/article[2]/div[2]/span/a""").text
        except:
            building_neighborhood = "neighborhood not found"
        
        print(building_streeteasy_address)
        fr = fr.append({'address': address, 'building_streeteasy_address': building_streeteasy_address, 'building_active_rentals': building_active_rentals, 'building_past_rentals': building_past_rentals, 'building_present_sales': building_present_sales, 'building_past_sales': building_past_sales, 'building_amenities': building_amenities, 'building_facts': building_facts, 'neighborhood': building_neighborhood}, ignore_index = True)
    return fr

def present_rentals_parser(dt):
	dt['num_active_rentals'] = dt['building_active_rentals'].str.split(' ').str[0]
	try:
		dt['avg_price_active_rentals'] = dt['building_active_rentals'].str.split(' ').str[7]
		dt['avg_sqft_active_rentals'] = dt['building_active_rentals'].str.split(' ').str[3]
		dt['avg_sqft_active_rentals'] = dt['avg_sqft_active_rentals'].str.replace("""(""", '')
	except:
		dt['avg_price_active_rentals'] = dt['building_active_rentals'].str.split(' ').str[3]
		dt['avg_price_active_rentals'] = dt['avg_price_active_rentals'].str.replace("""(""", '')

def past_rentals_parser(dt):
	dt['num_past_rentals'] = dt['building_past_rentals'].str.split(' ').str[0]
	try:
		dt['avg_price_past_rentals'] = dt['building_past_rentals'].str.split(' ').str[7]
		dt['avg_sqft_past_rentals'] = dt['building_past_rentals'].str.split(' ').str[3]
		dt['avg_sqft_past_rentals'] = dt['avg_sqft_past_rentals'].str.replace("""(""", '')
	except:
		dt['avg_price_past_rentals'] = dt['building_past_rentals'].str.split(' ').str[3]
		dt['avg_price_past_rentals'] = dt['avg_price_past_rentals'].str.replace("""(""", '')

def present_sales_parser(dt):
	dt['num_present_sales'] = dt['building_present_sales'].str.split(' ').str[0]
	try:
		dt['avg_price_present_sales'] = dt['building_present_sales'].str.split(' ').str[7]
		dt['avg_sqft_present_sales'] = dt['building_present_sales'].str.split(' ').str[3]
		dt['avg_sqft_present_sales'] = dt['avg_sqft_present_sales'].str.replace("""(""", '')
	except:
		dt['avg_price_present_sales'] = dt['building_present_sales'].str.split(' ').str[3]
		dt['avg_price_present_sales'] = dt['avg_price_present_sales'].str.replace("""(""", '')
        
def past_sales_parser(dt):
	dt['num_past_sales'] = dt['building_past_sales'].str.split(' ').str[0]
	try:
		dt['avg_price_past_sales'] = dt['building_past_sales'].str.split(' ').str[7]
		dt['avg_sqft_past_sales'] = dt['building_past_sales'].str.split(' ').str[3]
		dt['avg_sqft_past_sales'] = dt['avg_sqft_past_sales'].str.replace("""(""", '')
	except:
		dt['avg_price_past_sales'] = dt['building_past_sales'].str.split(' ').str[3]
		dt['avg_price_past_sales'] = dt['avg_price_past_sales'].str.replace("""(""", '')

################
def facts_parser(dt):
    dt['building_units'] = dt['building_facts'].str.extract('(^\d*)')
################


random_num = str(randint(100, 999))
random_num1 = str(randint(1000, 9999))
process_data = pd.DataFrame(data = None, index = [0], columns = ['address', 'building_streeteasy_address', 'building_active_rentals', 'building_past_rentals', 'building_present_sales', 'building_past_sales', 'neighborhood'],
                            dtype = None, copy = False)

data = pd.read_csv('vivaldi.csv', encoding = 'utf-8')
driver = init_driver()
to_url = data['address']
urls = create_urls(to_url)
urls = urls.astype(str)
pre_process = scrape_data(urls, process_data)

final1 = present_rentals_parser(pre_process)
final2 = past_rentals_parser(pre_process)
final3 = present_sales_parser(pre_process)
final4 = past_sales_parser(pre_process)
final5 = facts_parser(pre_process)

print(pre_process)

pre_process.to_csv('streeteasy.csv', encoding = 'utf-8')
close()







