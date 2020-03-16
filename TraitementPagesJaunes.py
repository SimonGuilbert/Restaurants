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
        DESCRIPTION: Lien de la page d'acceuil du sit des pages Jaunes

    Returns
    -------
    TYPE: int
        DESCRIPTION: nombre de page possible
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
    """Creer les url pour changer de page
    Parameters
    ----------
    url : TYPE
        DESCRIPTION.
    page : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION:Lien avec la page
    """
    return url+"&page="+str(page)

# =============================================================================
# Traitement d'un restaurant
# =============================================================================

def recherche_site_web(resto):
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
        return "None"
    
def recuperation_des_json(url):
    """
    recuperation des donnee du restaurant en passant par le json que les pages Jaunes proposent
    Parameters
    ----------
    url : TYPE:String
        DESCRIPTION:Lien de la page de recherche

    Returns
    -------
    donne : TYPE:dictionary
        DESCRIPTION: Information retenu pour le CSV

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
        url="https://www.pagesjaunes.fr/pros/detail?bloc_id="+str(resto)#accés au differents lien
        req=Request(url,headers={"User-Agent":"Mozilla/70.0"})
        html = urlopen(req).read()
        html_soup = BeautifulSoup(html, 'html.parser')
        #recherche site 
        nom_site=recherche_site_web(resto)
        #recherche json
        recherche = html_soup.findAll("script",attrs={'type':"application/ld+json"})   
        try:
            recherche=json.loads(recherche[0].getText())[0]
            donne[recherche['name']]=[recherche["address"]["streetAddress"],recherche["address"]["postalCode"],recherche["address"]["addressLocality"],recherche["telephone"],nom_site]
        except:
            pass
    return donne
















