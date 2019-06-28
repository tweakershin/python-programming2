# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 11:24:02 2019

@author: tjlee
"""
import sys
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

def current_ratio(df):
    #변수 초기화
    cnt=0
    temp_list=[]
    new_df=pd.DataFrame()
    
    for df_index in df.index:
        
        FNGUIDE_FINANCE_SEARCH_URL=f'http://comp.fnguide.com/SVO2/asp/SVD_FinanceRatio.asp?pGB=5&gicode=A{df_index}&cID=&MenuYn=N&ReportGB=&NewMenuID=104&stkGb=701'
        
        #URL 태그 추출
        try:
            resp = requests.get(FNGUIDE_FINANCE_SEARCH_URL)
            soup = BeautifulSoup(resp.content, 'html.parser')
        except: #인터넷 튕김시 대기
            print('연결 끊겼습니다. 재접속 대기중...')
            time.sleep(15)
            
            try: #다시 한 번 접속 시도
                resp = requests.get(FNGUIDE_FINANCE_SEARCH_URL)
                soup = BeautifulSoup(resp.content, 'html.parser')
            except: #접속 실패 강제 종료
                print("접속에 실패했습니다. 종료합니다.")
                time.sleep(3)
                sys.exit()
                
        #유동비율 데이터 추출
        tr_contents=soup.find_all('tr')
        
        temp_data=''
        for tr in tr_contents:
            if tr.text.find('유동비율') != -1:
                temp_data=tr.text

                break
        
        #최근 유동비율 값 추출 
        try:    
            temp_list.append(float(temp_data.split()[-1]))
            cnt+=1
            print(f'유동비율 데이터 추출 중 {cnt}/{len(df.index)}')
        except:
            temp_list.append('N/A')
            cnt+=1
            print(f'유동비율 데이터 추출 중 {cnt}/{len(df.index)}')    
            continue
        
    cratio_df=pd.DataFrame(temp_list,index=df.index, columns=['유동비율'])
    
    new_df=df.join(cratio_df, how='outer')
    
    return new_df #데이터프레임 전송