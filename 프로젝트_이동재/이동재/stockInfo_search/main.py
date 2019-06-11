# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 15:16:45 2019

@author: tjlee
"""

"""
기능 : PBR,PER,유동비율 기준으로 수치 입력 시 해당하는 기업 정보 들만 데이터 프레임에 저장, 엑셀로 출력, 멀티플 초이스 가능하게 만들 것 
main.py 프로그램 실행 파일. crawling 한 데이터를 받아와 세이브 함수에 보내주는 역할. 이용자를 위한 UI 제공
code_sampling.py 상장기업목록에서 기업명과 상장코드를 추출하는 프로그램. 추출한 정보를 main.py로 리턴
crawling 크롤링 함수가 정의되어 있는 패키지.
- perpbr 네이버 금융에서 해당 정보 추출
- icr 컴퍼니 가이드에서 이자보상배율 추출
- current_ratio 컴퍼니 가이드에서 유동비율 추출
value_modify 값을 수정하거나 제거하는 모듈이 담긴 패키지.
- NA_delete.py N/A 파일 제거하는 모듈. 완성된 데이터프레임에서 모든 값이 N/A 인 행을 제거하고 재조립할 것
- stock_screen.py 조건을 입력받아 조건에 맞게 DF를 재 설정해주는 모듈
save 저장관련 패키지. 중도 저장에 관련 모듈도 존재
- save_read.py ->미구현. 현재 인터넷 끊길 시 일정 시간동안 재접속이 될때까지 대기함. 그래도 안 될 경우 강제 종료. 
- 세이브 파일을 읽는 모듈. 데이터 크롤링 시도 시, 기존의 데이터가 있을 경우 '이미 데이터가 존재합니다, 갱신하겠습니까?' 로 유저에게 갱신 여부를 물어보게 함. 갱신시 다시 저장
-미완성된 데이터가 존재할 경우, 먼저 기존 엑셀 파일을 읽어 어디까지 진행되었는지 확인한 후 계속 진행하게 할 것.
- saveDB.py 세이브 함수 파일. main.py에서 DF 파일을 받아와 엑셀 처리. 엑셀은 exe 파일이 있는 위치에 stockInfo_DB 폴더를 생성하고 stockInfo.xlsx 파일로 만들것.
- 만약 기존 파일이 존재 할 경우, '이미 데이터가 존재합니다, 갱신하겠습니까?' 로 유저에게 갱신 여부를 물어보게 할 것
pandasTable Qt에서 데이터프레임을 출력하게 만들어주는 패키지 퍼옴
-pandasTable.py 데이터프레임을 모델링 해주는 PandasModel 클래스가 존재하는 모듈
"""

'''
'''
#GUI 관련 모듈
import os
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QCheckBox, QDesktopWidget, QTableView
from PyQt5.QtCore import Qt
from pandasTable.pandasTable import PandasModel
#데이터 크롤링 및 세이브 관련 패키지, 모듈
from code_data import code_sampling
from crawling import perpbr,icr, current_ratio
from value_modify import na_delete, stock_screen
from save import saveDB

class MyApp(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
################### layout design #############################################        
        #라인에디터
        self.le_per=QLineEdit()
        self.le_pbr=QLineEdit()
        self.le_icr=QLineEdit()
        self.le_cRatio=QLineEdit()
        
        #체크박스, 잠금 설정 포함
        cb_per=QCheckBox('PER',self) #PER
        cb_per.toggle()
        cb_per.stateChanged.connect(self.le_lock_per)
        
        cb_pbr=QCheckBox('PBR',self) #PBR
        cb_pbr.toggle()
        cb_pbr.stateChanged.connect(self.le_lock_pbr)
        
        cb_icr=QCheckBox('이자보상배율',self) #이자보상배율
        cb_icr.toggle()
        cb_icr.stateChanged.connect(self.le_lock_icr)
        
        cb_cRatio=QCheckBox('유동비율',self) #유동비율
        cb_cRatio.toggle()
        cb_cRatio.stateChanged.connect(self.le_lock_cRatio)
        
        #결과 브라우저
        #self.tb_result=QTextBrowser()
        self.tv_result=QTableView()
        
        #검색 버튼
        btn_search=QPushButton('검색',self)
        btn_search.clicked.connect(self.crawl_data)
        
        #체크 박스 세로로 묶기
        vbox_cb=QVBoxLayout()
        vbox_cb.addWidget(cb_per)
        vbox_cb.addWidget(cb_pbr)
        vbox_cb.addWidget(cb_icr)
        vbox_cb.addWidget(cb_cRatio)
        
        #라인 에디터 세로로 묶기
        vbox_le=QVBoxLayout()
        vbox_le.addWidget(self.le_per)
        vbox_le.addWidget(self.le_pbr)
        vbox_le.addWidget(self.le_icr)
        vbox_le.addWidget(self.le_cRatio)
        
        #검색 버튼 세로로 묶기(빈공간 삽입)
        vbox_search=QVBoxLayout()
        vbox_search.addStretch(3)
        vbox_search.addWidget(btn_search)
        
        #윗단 검색 도구 묶기
        hbox_above=QHBoxLayout()
        hbox_above.addLayout(vbox_cb)
        hbox_above.addLayout(vbox_le)
        hbox_above.addStretch(5)
        hbox_above.addLayout(vbox_search)
        
        #검색 도구와 결과창 묶기
        vbox_all=QVBoxLayout()
        vbox_all.addLayout(hbox_above,1)
        #vbox_all.addWidget(self.tb_result,5)
        vbox_all.addWidget(self.tv_result,5)
        self.setLayout(vbox_all)
########################## layout design End ##################################
##########################Window output #######################################        
        self.setWindowTitle('StockInfo_Search')
        self.setGeometry(800,800,800,600)
        self.center()
        self.show()
 ##########################Window output end ################################## 
########################### LineEdit Enable/Disable ###########################       
    def le_lock_per(self,state): #PER 체크 여부에 따라 값을 입력할 수 있는지 없는 지
        
        if state != Qt.Checked:
            self.le_per.setReadOnly(True)
            self.le_per.setText('')
            self.le_per.setStyleSheet('background: rgb(240,240,240);')
        else:
            self.le_per.setReadOnly(False)
            self.le_per.setStyleSheet('background: white;')
            
    def le_lock_pbr(self,state): #PBR 체크 여부에 따라 값을 입력할 수 있는지 없는 지
        
        if state != Qt.Checked:
            self.le_pbr.setReadOnly(True)
            self.le_pbr.setText('')
            self.le_pbr.setStyleSheet('background: rgb(240,240,240);')
        else:
            self.le_pbr.setReadOnly(False)
            self.le_pbr.setStyleSheet('background: white;')

    def le_lock_icr(self,state): #PBR 체크 여부에 따라 값을 입력할 수 있는지 없는 지
        
        if state != Qt.Checked:
            self.le_icr.setReadOnly(True)
            self.le_icr.setText('')
            self.le_icr.setStyleSheet('background: rgb(240,240,240);')
        else:
            self.le_icr.setReadOnly(False)
            self.le_icr.setStyleSheet('background: white;')

    def le_lock_cRatio(self,state): #PBR 체크 여부에 따라 값을 입력할 수 있는지 없는 지
        
        if state != Qt.Checked:
            self.le_cRatio.setReadOnly(True)
            self.le_cRatio.setText('')
            self.le_cRatio.setStyleSheet('background: rgb(240,240,240);')
        else:
            self.le_cRatio.setReadOnly(False)
            self.le_cRatio.setStyleSheet('background: white;')            
############################ LineEdit Enable/Disable END ######################
######################### 창보정 ##############################################        
    def center(self):
        
        qr=self.frameGeometry()
        cp=QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
######################### 창보정 끝 ###########################################
######################### 검색 버튼 누를 시 ####################################
    def crawl_data(self):
        
        per_text=self.le_per.text()
        pbr_text=self.le_pbr.text()
        icr_text=self.le_icr.text()
        cRatio_text=self.le_cRatio.text()
        
        BASE_DIR = os.getcwd()
        DB_DIR = os.path.join(BASE_DIR, "stockInfo_DB") #폴더나 파일이 없을 경우 에러 발생 시킬것 
        text_file=os.path.join(DB_DIR, 'stockInfo.csv')
        
        if os.path.isfile(text_file) and os.path.isdir(DB_DIR): #파일 유무 확인
            df=pd.read_csv(text_file, engine='python') #파일 읽기
            
            df=stock_screen.stock_screen(df,per_text,pbr_text,icr_text,cRatio_text)
            
            model=PandasModel(df)
            self.tv_result.setModel(model)
            
        else:
            print("파일이 존재하지 않습니다.")
######################### main.py 실행 ########################################
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
######################## main.py 끝 ###########################################
#종목 코드 샘플링
#dict1=code_sampling.code_sampling()
#
#if type(dict1) == type(dict()): # 종목 코드 샘플링 완료 유무 확인 
#    df=perpbr.perpbr(dict1) #PER,PBR 관련 데이터 크롤링 
#    df=icr.icr(df) #이자보상배율 크롤링    
#    df=current_ratio.current_ratio(df) #유동비율 크롤링    
#    df=na_delete.na_delete(df) #N/A 인덱스 제거
#     
#    saveDB.saveDB(df) #엑셀 세이브
#else:
#    print("샘플링 실패")
    

