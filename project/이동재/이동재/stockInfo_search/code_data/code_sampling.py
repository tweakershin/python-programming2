# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 15:44:21 2019

@author: tjlee
"""
import os
import pandas as pd


def code_sampling():
    #엑셀 데이터 읽기 
    BASE_DIR = os.getcwd()
    DB_DIR = os.path.join(BASE_DIR, "code_data") #폴더나 파일이 없을 경우 에러 발생 시킬것 
    text_file=DB_DIR+'\\company_list.xlsx'
    if os.path.isfile(text_file):
        df=pd.read_excel(text_file, sheet_name='company_list')
        
        #데이터 전처리(종목코드 문자화)
        temp_code={}
        temp_cd_list=[]
        temp_title_list=[]
        cnt=0
        
        for df_code in df['종목코드']:
            
            #종목코드 6자리 문자열로 변환 
            str_df_code=str(df_code)
            if len(str_df_code) == 6:
                temp_cd_list.append(str_df_code)
            else:
                len_cd=len(str_df_code)
                temp_cd_list.append("0"*(6-len_cd) + str_df_code)
                
            #기업명 추출
            temp_title_list.append(df['회사명'][cnt])
            cnt+=1
        
            
        temp_code['종목코드']=temp_cd_list
        temp_code['회사명']=temp_title_list
        
        #DF 생성, 리턴 
    ###    new_df=pd.DataFrame(temp_code)
        
        return temp_code
    
    else:
        ("상장기업목록이 존재하지 않습니다. 목록을 code_data 폴더에 넣어주세요.")
        
        return '-999'

