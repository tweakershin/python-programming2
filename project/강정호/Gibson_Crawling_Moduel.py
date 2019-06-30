#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
from pprint import pprint
import os
import pandas as pd 
        
intro = """Les-Paul, SG, ES, Acoustic, Designer, Bass 를 'crl.run( )'안에 입력하세요.\n입력한 값에 대한 깁슨 홈페이지에 있는 모든 깁슨 모델을 제공합니다."""
maker = 'jhkang1517@gmail.com'

BASE_DIR = os.getcwd()

class crl():
    def __init__(self, base_dir):
        self.base_dir = BASE_DIR
    
    def run(model):         
        PICTURE_DIR = os.path.join(BASE_DIR, 'guitar_pictures_{}'.format(model))
        
        if not os.path.exists(PICTURE_DIR):
            os.makedirs(PICTURE_DIR)
    
        guitar_list = []
        gibson_usl = "https://www.gibson.com/Guitars/" + model
        resp = requests.get(gibson_usl) 
        soup = BeautifulSoup(resp.content, 'html.parser') 
        gibson_contents = soup.find('div', class_='row pb-5').find_all('div', class_='col-sm-12 col-md-6 col-lg-4 px-2 mb-4')

        for div in gibson_contents:
            guitar_dict = {}

            a_tag = div.find('h4').find('a')
            guitar_dict['link'] = 'https://www.gibson.com'+a_tag['href'] 
            guitar_dict['name'] = a_tag.text
    
            b_tag = div.find('div', class_='price-label ml-3').find('span')
            guitar_dict['price'] = b_tag.text.strip()
            
            detail_resp = requests.get('https://www.gibson.com'+a_tag['href'])
            detail_soup = BeautifulSoup(detail_resp.content, 'html.parser')
            detail_content = detail_soup.find('div', class_='gibson-card py-4')
    
            d_tag = detail_content.find('div', class_='spec-section body-specs pb-4 mb-4')
            e_tag = detail_content.find('div', class_='spec-section neck-specs mb-4')
            f_tag = detail_content.find('div', class_='spec-section hardware-specs mb-4')
            g_tag = detail_content.find('div', class_='spec-section electronics-specs mb-4')
            h_tag = detail_content.find('div', class_='spec-section miscellaneous-specs mb-4')

            guitar_dict['Body'] = d_tag.text.strip('\nBody\n\n ').split("\n\n\n")
            guitar_dict['Neck'] = e_tag.text.strip('\nNeck\n\n ').split("\n\n\n")
            guitar_dict['Hardware'] = f_tag.text.strip('\nHardware\n\n ').split("\n\n\n")
            guitar_dict['Electronics'] = g_tag.text.strip('\nElectronics\n\n ').split("\n\n\n")
            guitar_dict['Miscellaneous'] = h_tag.text.strip('\nMiscellaneous\n\n ').split("\n\n\n")
    
            guitar_list.append(guitar_dict)
    
            c_tag = div.find('img')
            img_url = c_tag['src']
            img_resp = requests.get(img_url)
            p_filename = img_url.split('/')[-4:]
            filename = "".join(p_filename)
            guitar_picture_path = os.path.join(PICTURE_DIR, filename)  
            with open(guitar_picture_path, 'wb') as f:
                f.write(img_resp.content)

        print("총",len(guitar_list),"개의 결과물이 있습니다." )
        print("Gibson Accessory Kit의 주소는 https://www.gibson.com/Gear/Accessories/G-CAREKIT1 입니다.")
        return  guitar_list

