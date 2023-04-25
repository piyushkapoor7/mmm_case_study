# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 11:02:19 2023

@author: Piyush Kapoor
"""
import pandas as pd
from data_prepration import add_color_description, read_data, join_data
from modelling_mmm import lr_model
from attribute import attribution
import warnings
warnings.filterwarnings("ignore")

feature_cols = ['sales_lag1','promo1','ratio2','festivsl_flag','promo2']

# This Function computes the Contribution of Each feature column in the Actaul Sales Value
# Additionally it profiles the Mean Contribution of Each feature for Each Product Group
def compute_contribution(data):
    contri_cols = ['productgroup']
    attri_cols = []
    for col in feature_cols:
        attri_cols.append(col+'_attr')
    for col in feature_cols:
        contri_cols.append(col+'_percent_contri')
        data[col+'_percent_contri'] = round((data[col+'_attr']/data[attri_cols].sum(axis=1))*100,2)
    contri_matrix = data.groupby(by='productgroup',as_index=False).mean().round(2)[contri_cols]   
    return data,contri_matrix


# Complete End to End Pipleine Run
if __name__=="__main__":
    sales, articles, festival_flag = read_data()
    
    sales = pd.merge(left=sales,right=festival_flag,on='retailweek',how='inner')
    
    articles = add_color_description(articles)
    
    data_joined = join_data(sales,articles)
    coeff = lr_model(data_joined)
    data_joined = attribution(data_joined, coeff)
    data_joined,contri = compute_contribution(data_joined)
    contri.to_excel("Contribution by Product Category.xlsx")
    data_joined.to_excel("Final Data.xlsx")