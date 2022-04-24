# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 12:52:44 2022

@author: Nico
"""

from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# import csv
import os
import pandas as pd
import requests as req
import re

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

   

def scrap_movies_it(user_url,i):
    df = pd.DataFrame({'title': [], 'date': [], 'avg_rating': [], 'my_rating': []})
    url = user_url + str(i)+'&orderby=0'
    driver.get(url)
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "qc-cmp2-ui")))
        driver.find_element_by_class_name("css-v43ltw").click()
    except:
        pass
    
    sections = driver.find_elements(By.CLASS_NAME,"user-ratings-wrapper")
    for section in sections:
        films = section.find_elements(By.CLASS_NAME,"user-ratings-movie-item")
        for film in films:
            title = film .find_element(By.CLASS_NAME, 'mc-title').text
            date_regex = re.compile('\s?\([12]\d{3}\)')
            date = re.search(date_regex, title)
            date = re.sub('[()]', '', date.group())
            title = re.sub(date_regex, '', title)        
            parent = film.parent
            my_rating = parent.find_element(By.CLASS_NAME, 'ur-mr-rat').text
            avg_rating = film.find_element(By.CLASS_NAME, 'avgrat-box').text
            new_row = {'title': title, 'date': date, 'my_rating': my_rating, 'avg_rating': avg_rating}
            df = df.append(new_row,ignore_index=True)

    if req.get(user_url + str(i+1)+'&orderby=0'):        
        return pd.concat([df, scrap_movies_it(user_url,i+1)], ignore_index=True)
    else: 
        print('Done!')
        return df
        

def scrap_movies(user_url):
    user_url = user_url + '&p='
    return scrap_movies_it(user_url,1)



if __name__ == '__main__':
    
    driver = webdriver.Chrome(dname+'\chromedriver.exe')     
    
    user1 = 'https://www.filmaffinity.com/us/userratings.php?user_id=2683806'
    user2 = 'https://www.filmaffinity.com/es/userratings.php?user_id=515396'
    user3 = 'https://www.filmaffinity.com/es/userratings.php?user_id=6906529'
    users = {'user1':user1, 'user2':user2, 'user3': user3}
    
    for user in users:        
        df = scrap_movies(users[user])
        df.to_excel(str(user) + '.xlsx', index=False)
        # df.to_csv(str(user) + '.xlsx', index=False)




