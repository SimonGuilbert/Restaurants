# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 10:44:58 2020

@author: guillyd
"""
# =============================================================================
# import
# =============================================================================
from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import pandas as pd

# =============================================================================
# Fonction
# =============================================================================
def recuperation_des_json(url):
    req=Request(url,headers={"User-Agent":"Mozilla/70.0"})
    html = urlopen(req).read()
    html_soup = BeautifulSoup(html, 'html.parser')
    rows = html_soup.findAll("article")
    id_resto=[]
    for row in rows:
        cells =row["id"]
        id_resto.append(cells[8:]) 
    print(len(id_resto))
    donne={}
    for resto in id_resto:
        url="https://www.pagesjaunes.fr/pros/detail?bloc_id="+str(resto)
        req=Request(url,headers={"User-Agent":"Mozilla/70.0"})
        html = urlopen(req).read()
        html_soup = BeautifulSoup(html, 'html.parser')
        recherche = html_soup.findAll("script",attrs={'type':"application/ld+json"})
        
        try:
            recherche=json.loads(recherche[0].getText())[0]
            print(recherche)
            donne[recherche['name']]=[recherche["address"]["streetAdress"],recherche["address"]["postalCode"],recherche["address"]["addressLocality"],recherche["telephone"]]
        except:
            pass
    print(donne)
    return donne
        
url="https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui=restaurant&ou=haute-savoie-74"

if __name__ == "__main__":
    
    donne=recuperation_des_json(url)
    print(donne)

    
    
    
    
    
    
    
    
    