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
def recherche_identifiant_resto(url):
    '''
    Recherche les identifiants de tous les restaurants d'une page
    :return: la liste des ces identifiants
    '''
    req=Request(url,headers={"User-Agent":"Mozilla/74.0"})
    html = urlopen(req).read()
    html_soup = BeautifulSoup(html, 'html.parser')
    rows = html_soup.findAll("article") #Balise contenant toutes les informations sur un resto
    id_resto=[]
    for row in rows:
        cells =row["id"] #Recherche des identifiants
        id_resto.append(cells[8:])  #Suppression des termes en trop
    return id_resto


def recuperation_des_json(id_resto):
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
    #print(donne)
    return donne

def recherche_site_web(id_resto):
    '''
    Crée la liste des sites web des restaurants dont les identifiants sont donnés en paramètres
    Si le site n'existe pas ou n'est pas renseigner alors on ajout "NONE" à la liste
    :param id_resto: la liste des identifiants de chaque restaurant
    :return: la liste des site web des restaurants correspondant aux identifiants
    '''

    url = "https://www.pagesjaunes.fr/pros/detail?bloc_id=" + str(resto)
    req = Request(url, headers={"User-Agent": "Mozilla/74.0"})
    html = urlopen(req).read()
    html_soup = BeautifulSoup(html, 'html.parser')
    div_sites=html_soup.find("div" , class_="lvs-container marg-btm-s") # div contenant l'adresse du site web
    try:
        for div in div_sites:
            site=div.find('span', class_="value") # Recherche de l'adresse du site web
            return site.text
    except :
        return None

        
url = "https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui=restaurant&ou=haute-savoie-74"
    
if __name__ == "__main__":
    identifiants=recherche_identifiant_resto()
    liste_sites_web=recherche_site_web(identifiants)
    print(liste_sites_web)
    donne=recuperation_des_json(url)
    print(donne)
    
