#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 16:09:50 2018

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
	htmls1 = htmls[htmls.str.contains("ListingDetail") == True]
	htmls2 = htmls1.drop_duplicates()
	return htmls2

#driver goes to processed htmls and takes all the fucking data and saves in csv
def get_vivaldi_data(df):
    for html in processed_htmls:

        driver.get(html)

        try:
            buildingname = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[2]/header/h3[1]/span/span').text.replace(",", "")
        except:
            buildingname = ""
        try:
            aptprice = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[2]/section/div[1]/div/span[2]').text.replace(",", "")
        except:
            aptprice = ""
        try:
            aptaddress = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[2]/header/h2/span[1]').text.replace(",", "")
        except:
            aptaddress = ""
        try:
            commoncharges = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[2]/section/div[2]/div[2]/div[2]/span[2]/span[2]').text.replace(",", "")
        except:
            commoncharges = ""
        try:
            retaxes = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[2]/section/div[2]/div[2]/div[1]/span[2]/span[2]').text.replace(",", "")
        except:
            retaxes = ""
        try:
            buildingtype = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[2]/section/div[1]/div/div[1]/span[1]').text.replace(",", "")
        except:
            buildingtype = ""
        try:
            bedrooms = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[2]/section/div[2]/div[1]/div[2]/span[2]').text.replace(",", "")
        except:
            bedrooms = ""
        try:
            bathrooms = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[2]/section/div[2]/div[1]/div[3]/span[2]').text.replace(",", "")
        except:
            bathrooms = ""
        try:
            aptamenities = driver.find_element_by_xpath('//*[@id="collapseOne1"]/div[1]/div').text.replace("\n", "; ")
        except:
            aptamenities = ""
        try:
            aptnumber = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[2]/header/h2/span[2]/span').text.replace(",", "")
        except:
            aptnumber = ""
        try:
            active_sale_listing = driver.find_element_by_xpath('//*[@id="collapseOne1"]/div[2]/div/div[1]/h4/span[2]').text.replace(",", "")
        except:
            active_sale_listing = ""
        try:
            active_rental_listing = driver.find_element_by_xpath('//*[@id="collapseOne1"]/div[2]/div/div[2]/h4/span[2]').text.replace(",", "")
        except:
            active_rental_listing = ""
        try:
            rented_listings = driver.find_element_by_xpath('//*[@id="collapseOne1"]/div[2]/div/div[3]/h4/span[2]').text.replace(",", "")
        except:
            rented_listings = ""
        try:
            contracts_signed = driver.find_element_by_xpath('//*[@id="collapseOne1"]/div[2]/div/div[4]/h4/span[2]').text.replace(",", "")
        except:
            contracts_signed = ""
        try:
            closed_sales_data = driver.find_element_by_xpath('//*[@id="collapseOne1"]/div[2]/div/div[5]/h4/span[2]').text.replace(",", "")
        except:
            closed_sales_data = ""

        try:
            description = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[5]/div/section/div[1]/div').text
        except:
            description = ""

        df = df.append({'buildingname': buildingname, 'aptnumber': aptnumber, 'price': aptprice, 
						'address': aptaddress, 'commoncharges': commoncharges, 'retaxes': retaxes, 
						'buildingtype': buildingtype, 'bedrooms': bedrooms, 'bathrooms': bathrooms, 'aptamenities': aptamenities, 
						'active sale listings': active_sale_listing,
						'active_rental_listing': active_rental_listing, 'rented_listings': rented_listings, 
						'contracts_signed': contracts_signed, 'closed_sales_data': closed_sales_data, 'description': description.split()[:10]}, ignore_index=True)
    return df

# iterate through a certain amount of pages and collect the htmls on the pages.
def next_page_urls():
    wait = WebDriverWait(driver, 60)
    for i in range(num_pages):
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[5]/div/div[2]/div[1]/div/input')))
        element1 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="result-content-box"]/div[2]/div[1]/div[2]/div[1]/div[1]/h3/a')))
        get_htmls()
        nextpage = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div/div[2]/div[1]/div/input')
        nextpage.clear()
        nextpage.send_keys(i)
        buttonpress = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div/div[2]/div[1]/div/div/button[1]')
        buttonpress.click()


def sort():
	menu = driver.find_element_by_xpath('//*[@id="search-bar"]/div/div[1]/form/div[1]/div/a')
	menu.click()
	order = driver.find_element_by_xpath('//*[@id="search-bar"]/div/div[1]/form/div[1]/div/ul/li[5]')
	order.click()
	time.sleep(10)


def split_list(a_list):
    half = len(a_list)/2
    return a_list[:half]



process_data = pd.DataFrame(data = None, index = [0], columns = ['buildingname', 'aptnumber', 'price', 'address', 'commoncharges', 'retaxes', 
				'buildingtype', 'bedrooms', 'bathrooms', 'aptamenities', 'active sale listings',
				'active_rental_listing', 'rented_listings', 'contracts_signed', 'closed_sales_data', 'description'], dtype = None, copy = False)
list1 = []

######################
num_pages = 120
driver = init_driver()
goto("http://vivaldi.olridx.com/Search/Sales")
next_page_urls()

htmls = get_htmls()
processed_htmls = clean_data(htmls)

#B = split_list(processed_htmls)

Final_data = get_vivaldi_data(process_data)

Final_data.to_csv('vivaldi.csv', encoding = 'utf-8')
close()
######################
