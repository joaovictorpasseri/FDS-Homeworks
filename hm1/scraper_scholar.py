#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import urllib.request
import nbconvert
import pandas as pd
import time


# In[2]:


def scrape(author_name):
    url = "http://scholar.google.com.br/"
    autor = author_name
    
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(100)
    
    entrada_autor = driver.find_element_by_id("gs_hdr_tsi")
    entrada_autor.send_keys(autor)
    clicar = driver.find_element_by_id('gs_hdr_tsb')
    clicar.click()
    
    continue_link = driver.find_element_by_link_text(autor)
    continue_link.click()
    
    mostrar_mais = driver.find_element_by_id('gsc_bpf_more')
    x = mostrar_mais.get_property('disabled')==False 

    while x:
        mostrar_mais.click()
        time.sleep(2)
        x = mostrar_mais.get_property('disabled')==False

    html = BeautifulSoup(driver.page_source)

    tabela = html.find('table',{'id':'gsc_a_t'})
    papers = []
    trabalhos = tabela.find_all('td',{"class":'gsc_a_t'})
    for trabalhos in tabela.find_all('td',{"class":'gsc_a_t'}):
        titulo = trabalhos.find('a')
        titulo = titulo.contents[0]
        autores = trabalhos.find('div',{'class':'gs_gray'})
        autores = autores.contents[0].split(',')    
        autores = [i.strip() for i in autores]
        if autores[-1]=='...':
            autores.pop()
        papers.append({'title':titulo,'authors':autores})

    driver.quit()
    return papers
    
    

