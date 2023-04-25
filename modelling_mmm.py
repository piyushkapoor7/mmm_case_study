# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 15:15:20 2023

@author: Piyush Kapoor
"""
import pandas as pd
from data_prepration import add_color_description, read_data, join_data
from sklearn.linear_model import LinearRegression as LR
#from sklearn.preprocessing import OneHotEncoder as ohe
from sklearn.metrics import r2_score,mean_absolute_percentage_error as mape

import warnings
warnings.filterwarnings("ignore")


feature_cols = ['sales_lag1','promo1','ratio2','festivsl_flag','promo2']
#feature_cols = ['sales_lag1','prom','ratio2','festivsl_flag']
y_col = 'sales'


# Simple Linear Regression MOdel for Media Mix Modelling
# Ran iteration on varaibles & intercept tp get best model
 
def lr_model(data):
    prom = []
    for i in data.index:
        if((data['promo1'][i]==1) or (data['promo2'][i]==1)):
            prom.append(1)
        else:
            prom.append(0)
    data['prom'] = prom
    cats = data.productgroup.unique()
    coefficients = {}
    for cat in cats:
        filt_data = data[data.productgroup==cat]
        #enc = ohe(handle_unknown='ignore')
        #enc.fit(filt_data[['month']])
        #filt_data[['jan','feb','march','apr','may','june','july','aug','sept','oct','nov','dec']] = enc.transform(filt_data[['month']]).toarray()
        print("\n",cat)
        #filt_data['ratio2'] = filt_data['regular_price']/data['current_price']
        x = filt_data[feature_cols]
        y = filt_data[[y_col]]
         
        lr_model = LR(fit_intercept = False,positive=True)
        lr_model.fit(x,y)
        pred = lr_model.predict(x)
        print('R - sq : ',r2_score(y,pred))
        print("MAPE:",mape(y,pred))
        print(lr_model.coef_[0])
        coefficients.update({cat:lr_model.coef_[0]})
        print(lr_model.intercept_)
    return coefficients
    pass

# Pipeline Execution 
if __name__=="__main__":
    sales, articles, festival_flag = read_data()
    
    sales = pd.merge(left=sales,right=festival_flag,on='retailweek',how='inner')
    
    articles = add_color_description(articles)
    
    data_joined = join_data(sales,articles)
    coeff = lr_model(data_joined)
    #attributed_data = attribute(data_joined, coeff)
    
    
    
    
    