# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 19:40:10 2019

@author: tjlee
"""
import sys
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

def icr(df):
    #변수 초기화
    temp_list=[]
    cnt=0
    new_df=pd.DataFrame()
    
    for df_index in df.index:
        
        FNGUIDE_FINANCE_SEARCH_URL=f'http://comp.fnguide.com/SVO2/asp/SVD_FinanceRatio.asp?pGB=5&gicode=A{df_index}&cID=&MenuYn=N&ReportGB=&NewMenuID=104&stkGb=701'
        
        #URL 태그 추출
        try:
            resp = requests.get(FNGUIDE_FINANCE_SEARCH_URL)
            soup = BeautifulSoup(resp.content, 'html.parser')
        except: #인터넷 끊김시 대기
          
            print('연결 끊겼습니다. 재접속 대기중...')
            time.sleep(15)
            
            try: #다시 한번 접속 시도
                resp = requests.get(FNGUIDE_FINANCE_SEARCH_URL)
                soup = BeautifulSoup(resp.content, 'html.parser')
            except: #접속 실패 강제 종료
                print("접속에 실패했습니다. 종료합니다.")
                time.sleep(3)
                sys.exit()

        #이자보상배율 데이터 추출
        tr_contents=soup.find_all('tr')
        
        temp_data=''
        for tr in tr_contents:
            if tr.text.find('이자보상배율') != -1:
                temp_data=tr.text

                break
        #최근 이자보상배율 데이터 추출
        try:    
            temp_list.append(float(temp_data.split()[-1]))
            cnt+=1
            print(f'이자보상배율 데이터 추출 중 {cnt}/{len(df.index)}')
        except:
            temp_list.append('N/A')
            cnt+=1
            print(f'이자보상배율 데이터 추출 중 {cnt}/{len(df.index)}')
            continue
        
    icr_df=pd.DataFrame(temp_list,index=df.index, columns=['이자보상배율'])
    
    new_df=df.join(icr_df, how='outer')
    
    return new_df #데이터프레임 전송