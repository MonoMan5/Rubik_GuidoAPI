#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 16:42:47 2018

@author: tmontagni
"""
import pandas as pd


vivaldi = pd.read_csv('vivaldi.csv', encoding = 'utf-8')
elegran = pd.read_csv('elegran.csv', encoding = 'utf-8')
streeteasy = pd.read_csv('streeteasy.csv', encoding = 'utf-8')


results1 = vivaldi.merge(streeteasy, how = 'inner', on = ['address'])
results1.to_csv('results1.csv', encoding = 'utf-8')
results1 = pd.read_csv('results1.csv', encoding = 'utf-8')

results1['price'] = results1['price'].astype(str)
results1['commoncharges'] = results1['commoncharges'].astype(str)
results1['retaxes'] = results1['retaxes'].astype(str)
results1['bedrooms'] = results1['bedrooms'].astype(str)
results1['bathrooms'] = results1['bathrooms'].astype(str)
results1['active sale listings'] = results1['active sale listings'].astype(str)
results1['active_rental_listing'] = results1['active_rental_listing'].astype(str)
results1['rented_listings'] = results1['rented_listings'].astype(str)
results1['contracts_signed'] = results1['contracts_signed'].astype(str)
results1['closed_sales_data'] = results1['closed_sales_data'].astype(str)
results1['num_active_rentals'] = results1['num_active_rentals'].astype(str)
results1['num_past_rentals'] = results1['num_past_rentals'].astype(str)
results1['num_present_sales'] = results1['num_present_sales'].astype(str)
results1['num_past_sales'] = results1['num_past_sales'].astype(str)
results1['building_units'] = results1['building_units'].astype(str)


results1 = results1.drop(columns = ['building_active_rentals', 'building_past_rentals', 'building_present_sales','building_present_sales','building_past_sales', 'building_facts'])


results2 = results1.merge(elegran, how = 'inner', on = ['description', 'price'])
results2 = results2.drop_duplicates(['price', 'address_x', 'sqft'])
results2.to_csv('results.csv', encoding = 'utf-8')

print(results1.dtypes)





# final table is results1