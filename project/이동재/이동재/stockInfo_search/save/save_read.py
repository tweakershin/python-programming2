# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 14:08:50 2019

@author: tjlee
"""
import os

def save_read():
    
    BASE_DIR = os.getcwd()
    SAVE_DB_DIR = os.path.join(BASE_DIR, "stockInfo_DB")
    
    temp_name = "stockInfo.xlsx"
    txt_name = os.path.join(SAVE_DB_DIR, temp_name)