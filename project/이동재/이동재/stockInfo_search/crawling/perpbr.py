# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 15:26:46 2019

@author: tjlee
"""
import sys
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

def perpbr(cd_list):
    #변수 초기화
    COMPANY_KEY='기업명'
    CODE_KEY='종목코드'
    df=pd.DataFrame()
    flag=0
    index_list=[]
    count=0

    for cd in cd_list[CODE_KEY]:
        
        
        #URL 태그 추출
        NAVER_FINANCE_SEARCH_URL='https://finance.naver.com/item/main.nhn?'
        
        params = {
                'code' : cd 
                }
        try:  
            resp = requests.get(NAVER_FINANCE_SEARCH_URL, params=params)
            soup = BeautifulSoup(resp.content, 'html.parser')
        except: #인터넷 튕김 시 될 때까지 대기
            print('연결 끊겼습니다. 재접속 대기중...')
            time.sleep(15)
            
            try: #다시한번 접속 시도
                resp = requests.get(NAVER_FINANCE_SEARCH_URL, params=params)
                soup = BeautifulSoup(resp.content, 'html.parser')
            except: #접속 실패 강제 종료
                print("접속에 실패했습니다. 종료합니다.")
                time.sleep(3)
                sys.exit()
        
        #per 테이블 추출 
        try: #데이터가 존재하지 않는 기업들 스킵을 위한 예외처리
            per_contents=soup.find(attrs={'class' : 'aside_invest_info'}).find(attrs={'class' : 'per_table'})
            em_contents=per_contents.find_all('em')
            
            #기업명 추출 
            title_contents=soup.find(attrs={'class':'wrap_company'}).find('h2')
            
            #값 추출 
            temp_list=[]
            temp_list.append(title_contents.text)
            for em in em_contents:
                temp_list.append(em.text)
            
            #DF화
            if flag==0: #첫 배열 생성
                df=pd.DataFrame(temp_list).T
                df.columns=['기업명','PER','EPS','PER(krx)','EPS(krx)','추정PER','추정EPS','PBR','BPS','배당수익률']
                count+=1
                print(f'{df[COMPANY_KEY][0]} PBR,PER 추출 완료 {count}/{len(cd_list[CODE_KEY])}')
                index_list.append(cd)
                flag=1
            else: #이후 배열 삽입
                temp_df=pd.DataFrame(temp_list).T
                temp_df.columns=['기업명','PER','EPS','PER(krx)','EPS(krx)','추정PER','추정EPS','PBR','BPS','배당수익률']
                df=df.append(temp_df, ignore_index=True)
                count+=1
                print(f'{temp_df[COMPANY_KEY][0]} PBR,PER 추출 완료 {count}/{len(cd_list[CODE_KEY])}')
                index_list.append(cd)
                     
        except:
            count+=1
            print(f'{temp_df[COMPANY_KEY][0]} PBR,PER 추출 불가(없는데이터) {count}/{len(cd_list[CODE_KEY])}')
            continue
        
        
    df.index=index_list
    return df #데이터프레임 전송