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

def recherche_menu(resto):
    '''
    Crée la liste des menus des restaurants dont les identifiants sont donnés en paramètres
    Si le menu n'est pas renseigner alors on ajout "NONE" à la liste
    :param id_resto: la liste des identifiants de chaque restaurant
    :return: la liste des formules avec leurs prix des restaurants correspondant aux identifiants
    '''

    url = "https://www.pagesjaunes.fr/pros/detail?bloc_id=" + str(resto)
    req = Request(url, headers={"User-Agent": "Mozilla/74.0"})
    html = urlopen(req).read()
    html_soup = BeautifulSoup(html, 'html.parser')
    formules=[]
    try:
        div_formules = html_soup.findAll("div", class_="formule marg-btm-s row")  # div contenant les formules
        for div in div_formules:
            formule = div.find('p', class_="no-margin")# Recherche de l'intitule de la formule
            prix = div.find('span', class_="tarif-formule")  # Recherche du prix de la formule
            formules  += [formule.text, prix.text]
    except:
        formules += ["None", "None"]
    return formules

def recherche_suggestion(resto):
    '''
    Crée la liste des suggestion des restaurants dont les identifiants sont donnés en paramètres
    Si les suggestions ne sont pas renseigner alors on ajout "NONE" à la liste
    :param id_resto: la liste des identifiants de chaque restaurant
    :return: la liste des suggestions avec leurs prix des restaurants correspondant aux identifiants
    '''

    url = "https://www.pagesjaunes.fr/pros/detail?bloc_id=" + str(resto)
    req = Request(url, headers={"User-Agent": "Mozilla/74.0"})
    html = urlopen(req).read()
    html_soup = BeautifulSoup(html, 'html.parser')
    suggestions=[]
    try:
        div_suggestions = html_soup.findAll("div", class_="marg-btm-xs row")  # div contenant les formules
        for div in div_suggestions:
            suggestion = div.find('span', class_="col-xs-10 description-mets")# Recherche de l'intitule de la formule
            prix = div.find('span', class_="col-xs-2 tarif-mets")  # Recherche du prix de la formule
            suggestions+=[suggestion.text, prix.text]
    except:
        suggestions+=["None", "None"]
    return suggestions

def recherche_prestation(resto):
    '''
    Crée la liste des prestations des restaurants dont les identifiants sont donnés en paramètres
    Si les prestation ne sont pas renseigner alors on ajout "NONE" à la liste
    :param id_resto: la liste des identifiants de chaque restaurant
    :return: la liste des prestations des restaurants correspondant aux identifiants
    '''

    url = "https://www.pagesjaunes.fr/pros/detail?bloc_id=" + str(resto)
    req = Request(url, headers={"User-Agent": "Mozilla/74.0"})
    html = urlopen(req).read()
    html_soup = BeautifulSoup(html, 'html.parser')
    prestations=[]
    li_prestations = html_soup.findAll("li", class_="col-sm-6 marg-btm-s")  # li contenant les prestations
    try:
        for li in li_prestations:
            prestation = li.find('span')# Recherche de l'intitule de la prestation
            prestations+=[prestation]
    except:
        prestations+=["None"]
    return prestations

def recherche_horaires(resto):
    '''
    Crée la liste des horaires des restaurants dont les identifiants sont donnés en paramètres
    Si les horaires ne sont pas renseigner alors on ajout "NONE" à la liste
    :param id_resto: la liste des identifiants de chaque restaurant
    :return: la liste des horaires des restaurants correspondant aux identifiants
    '''

    url = "https://www.pagesjaunes.fr/pros/detail?bloc_id=" + str(resto)
    req = Request(url, headers={"User-Agent": "Mozilla/74.0"})
    html = urlopen(req).read()
    html_soup = BeautifulSoup(html, 'html.parser')
    horaires=[]
    ul_horaires = html_soup.find("ul", class_="hidden liste-horaires-principaux")  # ul contenant les horaires
    li_horaires = ul_horaires.findAll("li" , class_="horaire-ouvert")
    try:
        for li in li_horaires:
            jour = li.find('p')# Recherche du jour
            heures=li.findAll("span", class_="horaire") # Recherche des horaires pour ce jour
            un_jour=[jour.text]
            for heure in heures : # Ajout de toutes les heures
                un_jour+=[heure.text]
            horaires+=un_jour
    except:
        horaires+=["None"]
    return horaires
    
def recuperation_des_donnees(url):
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
















