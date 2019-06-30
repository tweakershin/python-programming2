# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 09:29:03 2019

@author: tjlee
"""

'''
새로운 요소들이 추가 될 때 마다 계속 컬럼을 추가해 줘야 한다... 수정 해야함
'''
import pandas as pd

def na_delete(df):
    #변수 초기화
    flag=0 #N/A 유무 확인
    flag_df=0 #데이터프레임 첫 값 입력   
    new_df=pd.DataFrame()
    na_cnt=0
    
    for df_index in df.index:
        cnt=0 #첫번째 데이터(기업명) 스킵
        for df_data in df.loc[df_index]:
            if cnt==0:
                cnt+=1
                
                continue
            if df_data !='N/A' :
                flag=1
                break
        if flag==1: #데이터가 하나라도 있는 인덱스 DF에 누적
            #DF화
            
            if flag_df==0: #첫 배열 생성
                new_df=pd.DataFrame(df.loc[df_index]).T
                new_df.columns=df.columns
                na_cnt+=1
                print(f'N/A 데이터 분류중 {na_cnt}/{len(df.index)}')
                
                flag_df=1
            else:
                temp_df=pd.DataFrame(df.loc[df_index]).T
                temp_df.columns=df.columns
                new_df=new_df.append(temp_df)
                na_cnt+=1
                print(f'N/A 데이터 분류중 {na_cnt}/{len(df.index)}')
                
            flag=0
        else: #메세지 전송용
            na_cnt+=1
            print(f'N/A 데이터 분류중 {na_cnt}/{len(df.index)}')
    
    return new_df