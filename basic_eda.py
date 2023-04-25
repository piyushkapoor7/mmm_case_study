# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 11:29:47 2023

@author: Piyush Kapoor
"""
import pandas as pd
from data_prepration import add_color_description, read_data, join_data
import matplotlib.pyplot as plt
from sklearn.preprocessing import KBinsDiscretizer as binner
import numpy as np
from random import randint

# This Function will plot Bar Chart for each Categorical Variable w.r.t. Average Sales in respoective category of the columns
def prepare_basic_sales_view_cat(data,cols):
    for col in cols:
        profile = data.groupby(by=col,as_index=False).mean()[[col,'sales']]
        profile = profile.sort_values(by=['sales'],ascending=False)
        profile = profile.head(10)
        fig,ax = plt.subplots(figsize =(16, 9))
        colors = ['blue','red','green','purple','cyan','magenta','yellow','orange','olive']
        plt.barh(profile[col], profile['sales'], color =colors[randint(0, 8)])#,width = 0.4)
        ax.grid(b = True, color ='grey',linestyle ='-.', linewidth = 0.5,alpha = 0.2)
        plt.xlabel("Average Sales Per Category")
        plt.ylabel(col)
        ax.invert_yaxis()
        plt.savefig(col+"_profile.jpg")
        plt.close()
    pass

# Convert Continous varibales in to categorical by Binning and then plotting them
def prepare_basic_sales_view_cont(data,cols):
    col_names = []
    for col in cols:
        bins = binner(n_bins=5, strategy='uniform',encode='ordinal')
        bins.fit(data[[col]])
        bin_num_name = col+'_bin_nums'
        data[bin_num_name] = bins.transform(data[[col]])
        bin_nums = np.unique(bins.transform(data[[col]])[:,0])
        bin_names=[]
        for num in bin_nums:
            filt_data = data[data[bin_num_name]==num]
            mn = round(min(filt_data[col]),2)
            mx = round(max(filt_data[col]),2)
            bin_names.append(str(mn)+' - '+str(mx))
        bin_col_name = col+'_bin_names'
        bins = pd.DataFrame(np.column_stack((bin_nums,bin_names)),columns=[bin_num_name,bin_col_name])
        data[bin_num_name] = data[bin_num_name].astype(str)
        data = pd.merge(left=data,right=bins,on=bin_num_name)
        col_names.append(bin_col_name)
    prepare_basic_sales_view_cat(data,col_names)
    pass

# Pipeline Execution 
if __name__=="__main__":
    sales, articles, festival_flag = read_data()
    
    sales = pd.merge(left=sales,right=festival_flag,on='retailweek',how='inner')
    
    articles = add_color_description(articles)
    
    data_joined = join_data(sales,articles)
    prepare_basic_sales_view_cat(data_joined,['promo1','promo2','festivsl_flag','productgroup','category','style','main_color','sec_color','gender','month'])
    prepare_basic_sales_view_cont(data_joined,['ratio','cost'])

    
