# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 12:03:11 2019

@author: tjlee
"""

import os

def saveDB(df):
 #   flag = 0 #기존 데이터 존재 시에 갱신을 할지 말지 정하게 해주는 변수
    
    BASE_DIR = os.getcwd()
    SAVE_DB_DIR = os.path.join(BASE_DIR, "stockInfo_DB")
    
    if not os.path.exists(SAVE_DB_DIR):
        os.makedirs(SAVE_DB_DIR)
    
    temp_name = "stockInfo.xlsx"

        
    txt_name = os.path.join(SAVE_DB_DIR, temp_name)
    
    df.to_excel(txt_name, sheet_name='sheet1')
        