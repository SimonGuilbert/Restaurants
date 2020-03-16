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
import pandas as pd
# =============================================================================
# Fonction
# =============================================================================

def nombre_de_page(url):
    """
    Recupere le nombre de page d'une recherche
    Parameters
    ----------
    url : TYPE
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

url_acceuil="https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui=restaurant&ou=haute-savoie-74"

if __name__ == "__main__":
    nbre_page=nombre_de_page(url_acceuil)
    print(nbre_page)#nombre de page 
    for page in range(1,nbre_page+1):
        visiter_page(url_acceuil, page)

















