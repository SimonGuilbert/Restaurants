# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 10:06:47 2020

@author: Jonathan Molieres
"""
# =============================================================================
# Import
# =============================================================================
from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
# =============================================================================
# Fonction
# =============================================================================

# =============================================================================
# Traitement des différentes pages
# =============================================================================
def nombre_de_page(url):
    """
    Recupere le nombre de page d'une recherche
    Parameters
    ----------
    url : TYPE:String
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.
    """
    page=[]
    while len(page)==0:#attend de reponse
        req=Request(url, headers={"User-Agent":"Mozilla/70.0"})
        html = urlopen(req).read()
        html_soup = BeautifulSoup(html, 'html.parser')
        rows = html_soup.findAll("option")
        for row in rows:
            try:
                page.append(int(row["value"]))
            except:
                pass
    return len(page)

def visiter_page(url,page):
    """Creer les url pour changer de page"""
    return url+"&page="+str(page)

# =============================================================================
# Traitement d'un restaurant
# =============================================================================
    
def recuperation_des_json(url):
    """
    recuperation des donnee du restaurant en passant par le json que les pages Jaunes proposent
    Parameters
    ----------
    url : TYPE
        DESCRIPTION.

    Returns
    -------
    donne : TYPE
        DESCRIPTION.

    """
    req=Request(url,headers={"User-Agent":"Mozilla/70.0"})
    html = urlopen(req).read()
    html_soup = BeautifulSoup(html, 'html.parser')
    rows = html_soup.findAll("article")
    id_resto=[]
    for row in rows:
        cells =row["id"]
        id_resto.append(cells[8:]) 
    print("nombre de restaurant sur la page=",len(id_resto))
    donne={}
    for resto in id_resto:
        url="https://www.pagesjaunes.fr/pros/detail?bloc_id="+str(resto)
        req=Request(url,headers={"User-Agent":"Mozilla/70.0"})
        html = urlopen(req).read()
        html_soup = BeautifulSoup(html, 'html.parser')
        recherche = html_soup.findAll("script",attrs={'type':"application/ld+json"})
        
        try:
            recherche=json.loads(recherche[0].getText())[0]
            donne[recherche['name']]=[recherche["address"]["streetAddress"],recherche["address"]["postalCode"],recherche["address"]["addressLocality"],recherche["telephone"]]
        except:
            pass
    return donne
















