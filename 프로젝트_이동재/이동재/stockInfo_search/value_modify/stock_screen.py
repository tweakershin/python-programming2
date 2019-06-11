# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 09:06:31 2019

@author: tjlee
"""
import pandas as pd

def stock_screen(df,per,pbr,icr,cRatio):
    new_df=pd.DataFrame()
    flag=0
    for idx in df.index:
        try:
            if float(df['PER'][idx])>=float(per) :
                if flag==0:
                    new_df=pd.DataFrame(df.loc[idx])
                    new_df=new_df.T
                    flag=1
                else:
                    temp_df=pd.DataFrame(df.loc[idx])
                    temp_df=temp_df.T
                    new_df=new_df.append(temp_df,ignore_index=True)
        except:
            continue
    return new_df