# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 10:44:58 2020

@author: guillyd
"""
from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
url="https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui=restaurant&ou=haute-savoie-74"
req=Request(url,headers={"User-Agent":"Mozilla/70.0"})
html = urlopen(req).read()
html_soup = BeautifulSoup(html, 'html.parser')
rows = html_soup.findAll("article")
page=[]
print(len(rows))

#for row in rows:
#    cells =row["value"]
#    page.append(cells)
#print(page)

id_resto=[]
for row in rows:
    cells =row["id"]
    id_resto.append(cells[8:])
print(id_resto,len(id_resto))

for resto in id_resto:
    url="https://www.pagesjaunes.fr/pros/detail?bloc_id="+str(resto)
    req=Request(url,headers={"User-Agent":"Mozilla/70.0"})
    html = urlopen(req).read()
    html_soup = BeautifulSoup(html, 'html.parser')
    noms = html_soup.findAll("script['type']")
   
    print(noms)
