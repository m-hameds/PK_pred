# -*- coding: utf-8 -*-
"""scrapping.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11kmy7h0Ilgw2JfjHYFpfw1RGczqjd_vL
"""

import matplotlib
matplotlib.use('Agg')

!pip install selenium
!pip install bs4
!pip install html5lib
import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import filedialog as fd
from tkinter import *
from bs4 import BeautifulSoup
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

import os
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt

class Chemist:

    def  __init__(self):
        self.iter1 = 0
        self.iter2 = 0
        self.smiles= []


    def CSV_Input(self):
        self.filename = fd.askopenfilename(filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        self.df = pd.read_csv(self.filename)
        self.data = self.df["ID"].to_list()
        
    def CSV_Input2(self):
        self.filename = fd.askopenfilename(filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        self.df = pd.read_csv(self.filename)
        self.da = self.df["Canonical SMILES"].to_list()

        for x in self.da:
            self.smiles.append(x)
        

    def driver_setup(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximize")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome("chromedriver.exe", options=chrome_options)

    def lanch_url(self):
        for chemi in self.data:
            self.driver.get("https://pubchem.ncbi.nlm.nih.gov/")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "input"))).send_keys(chemi)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "input"))).send_keys(Keys.ENTER)
            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//a[@data-action='featured-result-link']"))).click()
                self.extract(chemi)
            except:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[@class='breakword']"))).click()
                self.extract(chemi)
    def extract(self, chemi):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//main[@id='main-content']"))).click()

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html5lib")
        
        id = soup.find("section", attrs={"id":"Canonical-SMILES"})
        formula = id.find("div", attrs={"class":"section-content-item"})
        formula = formula.find("p").text
        print(chemi +": "+formula)
        self.smiles.append(formula)
        self.Save_CSV(formula)

    def extract2(self):
        WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.TAG_NAME, "h3"))).click()
        self.dataframe ={}
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html5lib")
        
        body = soup.find("tbody")
        tr = body.find_all("tr")
        for i in tr:
            td = i.find_all("td")
            self.dataframe.update({td[1].text:str(td[2].text)})
            print(td[1].text)
            print(td[2].text)

    def Save_CSV(self, smiles):
        df = pd.read_csv('data.csv')
        df.loc[self.iter2, "Canonical SMILES"] = smiles
        df.to_csv('data.csv', index=False)
        self.iter2 += 1

    def Save_CSV2(self):
        df = pd.read_csv('data.csv')

        for i in self.dataframe:
            df.loc[self.iter1, i] = self.dataframe[i]

        df.to_csv('data.csv', index=False)
        print("Number of Descriptor: ", self.iter1)
        self.iter1 += 1

    def lanch_URL2(self):
    
        for s in self.smiles:
            self.driver.get("http://www.scbdd.com/padel_desc/index/")
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.ID, "id_Smiles"))).send_keys(s)
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//input[@type='submit']"))).click()
            self.extract2()
            self.Save_CSV2()
        

if __name__ == "__main__":
    chemist = Chemist()    
    chemist.CSV_Input()
    chemist.driver_setup()
    chemist.lanch_url()
    chemist.lanch_URL2()
