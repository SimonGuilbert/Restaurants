# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 10:06:47 2020
@author: Jonathan Molieres
"""
from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
url="https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui=restaurant&ou=haute-savoie-74"
req=Request(url,headers={"User-Agent":"Mozilla/70.0"})
html = urlopen(req)
html_soup = BeautifulSoup(html, 'html.parser')
rows = html_soup.findAll("option")
page=[]
print(len(rows))
for row in rows:
    cells = row.findAll()
    page.append(cells)
print(page)
