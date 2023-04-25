# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 16:07:08 2023

@author: Piyush Kapoor
"""
import pandas as pd
import webcolors


sales_file_path = "sales.txt"
article_file_path = "article_attributes.txt"
festival_file_path = 'festival_flag.txt'
google_trends = 'google_trends.txt'


def read_data():
    try:
        sales = pd.read_csv(sales_file_path,sep=';')
    except:
        print("Sales File Not found in Current Working Directory")
    try:
        articles = pd.read_csv(article_file_path,sep=';')
    except:
        print("Article file mentined is not found in current working directory")
    try:
        festival_flag = pd.read_csv(festival_file_path,sep='\t')
    except:
        print("Mentioned Festical Flag file not found in Current Working Directory")
    return sales, articles, festival_flag

# Code to COnvert RGB Color Code Actual Color WOrd in English
# Code Picked From https://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green-with-python
def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

def add_color_description(data):
    main_col = []
    sec_col = []
    for i in data.index:
        r_m = data['rgb_r_main_col'][i]
        g_m = data['rgb_g_main_col'][i]
        b_m = data['rgb_b_main_col'][i]
        r_c = data['rgb_r_sec_col'][i]
        g_c = data['rgb_g_sec_col'][i]
        b_c = data['rgb_b_sec_col'][i]
        main_col.append(get_colour_name((r_m,g_m,b_m))[1])
        sec_col.append(get_colour_name((r_c,g_c,b_c))[1])
    data['main_color'] = main_col
    data['sec_color'] = sec_col
    return data
    pass

# Perfrom Below Opertions :
# (1) Join Sales & Product Attribute Data
# (2) Combine Google Trends Data
# (3) Creat a Lag Variable fror Column Sales to get Sales Value in Last Week
# (4) Create a varaible ratio2 i.e. Directly Propotional to Sales in order to get positive Co efficient in Modelling
 
def join_data(sales,articles):
    data = pd.merge(left=sales,right=articles,left_on='article',right_on='article',how='inner')
    data['month'] = data['retailweek'].str.slice(5, 7)
    gt_data = pd.read_csv(google_trends,sep='\t')
    data = pd.merge(left=data,right=gt_data,on='retailweek',how='inner')
    week= data[['retailweek']].drop_duplicates().reset_index().drop(columns=['index'])
    week['weekid'] = week.index
    week['weekId_l1'] = week['weekid']+1
    data = pd.merge(left=data,right=week,on='retailweek',how='inner')
    data = pd.merge(left=data,right=data[['weekId_l1','article','sales','country']],left_on=['weekid','article','country'],right_on=['weekId_l1','article','country'],how='inner')
    data = data[['country', 'article', 'sales_x', 'regular_price', 'current_price',
       'ratio', 'retailweek', 'promo1', 'promo2', 'festivsl_flag',
       'productgroup', 'category', 'cost', 'style', 'sizes', 'gender',
       'rgb_r_main_col', 'rgb_g_main_col', 'rgb_b_main_col', 'rgb_r_sec_col',
       'rgb_g_sec_col', 'rgb_b_sec_col', 'main_color', 'sec_color', 'month',
       'google_trends', 'sales_y']]
    data = data.rename(columns={'sales_x':'sales','sales_y':'sales_lag1'})
    data['ratio2'] = data['regular_price']/data['current_price']
    return data



# Pipeline Execution 
if __name__=="__main__":
    sales, articles, festival_flag = read_data()
    
    sales = pd.merge(left=sales,right=festival_flag,on='retailweek',how='inner')
    
    articles = add_color_description(articles)
    
    data_joined = join_data(sales,articles)
    
    

