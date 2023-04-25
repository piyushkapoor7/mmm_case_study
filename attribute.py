# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 10:09:00 2023

@author: Piyush Kapoor
"""

import pandas as pd
from data_prepration import add_color_description, read_data, join_data
from modelling_mmm import lr_model
import warnings
warnings.filterwarnings("ignore")

feature_cols = ['sales_lag1','promo1','ratio2','festivsl_flag','promo2']


# This Function Attributes the predicted value in to Different features 
#  and also re calibrate the same to match the actual sales

def attribution(data,coeff):
    var_coeff = []
    pred = []
    attr = []
    for i in data.index:
        var_coeff_tmp = []
        for j in range(0, len(feature_cols)):
            var_coeff_tmp.append(coeff[data['productgroup'][i]][j]*data[feature_cols[j]][i])
        pred.append(sum(var_coeff_tmp))
        var_coeff.append(var_coeff_tmp)
    for i in data.index:
        attr_tmp = []
        for j in range(0,len(feature_cols)):
            attr_tmp.append((data['sales'][i]/(pred[i]))*coeff[data['productgroup'][i]][j]*data[feature_cols[j]][i])
        attr.append(attr_tmp)
    data['prediction'] = pred
    attr_cols = []
    for col in feature_cols:
        attr_cols.append(col+'_attr')
    data[attr_cols] = attr
    return data
    

# Pipeline Execution 
if __name__=="__main__":
    sales, articles, festival_flag = read_data()
    
    sales = pd.merge(left=sales,right=festival_flag,on='retailweek',how='inner')
    
    articles = add_color_description(articles)
    
    data_joined = join_data(sales,articles)
    coeff = lr_model(data_joined)
    attributed_data = attribution(data_joined, coeff)
    