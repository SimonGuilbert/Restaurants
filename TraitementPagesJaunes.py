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
from time import sleep
import numpy as np


# =============================================================================
# Traitement des différentes pages
# =============================================================================
def nombre_de_page(url):
    """
    Recupere le nombre de page d'une recherche
    :param url : Lien de la page d'acceuil du site des Pages Jaunes
    :returns : nombre de pages
    """
    nbre_page = 0
    while nbre_page == 0:  # attente de reponse
        req = Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"})
        html = urlopen(req).read()
        html_soup = BeautifulSoup(html, 'html.parser')
        row = html_soup.find("span", class_="pagination-compteur")
        try:
            nbre_page = int(row.text[9:12])
        except ValueError:
            nbre_page = int(row.text[9:11])
        except:
            nbre_page = 0

    return nbre_page


def visiter_page(url, page):
    return url + "&page=" + str(page)  # Ajout de "&page=" + numéro de page à l'URL


# =============================================================================
# Traitement d'un restaurant
# =============================================================================
def recherche_site_web(html_soup):
    """
    Récupère le site web d'un restaurant
    Si le site n'existe pas ou n'est pas renseigné alors on retourne une valeur manquante
    :param html_soup: html du site dans le format de la bibliotheque beautifulsoup
    """
    div_sites = html_soup.find("div", class_="lvs-container marg-btm-s")  # div contenant l'adresse du site web
    try:
        for div in div_sites:
            site = div.find('span', class_="value")  # Recherche de l'adresse du site web
            return site.text
    except:
        return np.nan


def recherche_menu(html_soup):
    """
    Crée la liste des repas proposés par le restaurant avec leur prix 
    Si le menu n'est pas renseigné alors on retourne une valeur manquante
    :param html_soup: html du site dans le format de la bibliotheque BeautifulSoup
    """
    formules = []
    try:
        div_formules = html_soup.findAll("div", class_="formule marg-btm-s row")  # div contenant les formules
        for div in div_formules:
            formule = div.find('p', class_="no-margin")  # Recherche de l'intitule de la formule
            prix = div.find('span', class_="tarif-formule")  # Recherche du prix de la formule
            formules.append([formule.text, prix.text])
    except:
        return None
    if not formules:
        return None
    return formules


def recherche_suggestion(html_soup):
    """
    Crée la liste des suggestion du restaurant avec leur prix 
    Si les suggestions ne sont pas renseignées alors on retourne None
    :param html_soup: html du site dans le format de la bibliotheque beautifulsoup
    """
    suggestions = []
    try:
        div_suggestions = html_soup.findAll("div", class_="marg-btm-xs row")  # div contenant les formules
        for div in div_suggestions:
            suggestion = div.find('span', class_="col-xs-10 description-mets")  # Recherche de l'intitule de la formule
            prix = div.find('span', class_="col-xs-2 tarif-mets")  # Recherche du prix de la formule
            suggestions.append([suggestion.text, prix.text])
    except:
        return None
    if not suggestions:
        return None
    return suggestions


def recherche_prestation(html_soup):
    """
    Crée la liste des prestations proposées par le restaurants
    Si les prestation ne sont pas renseignées alors on retourne une valeur manquante
    :param html_soup: html du site dans le format de la bibliotheque beautifulsoup
    """
    prestations = []
    li_prestations = html_soup.findAll("li", class_="col-sm-6 marg-btm-s")  # li contenant les prestations
    try:
        for li in li_prestations:
            prestation = li.find('span')  # Recherche de l'intitule de la prestation
            prestations += [prestation.text]
    except:
        return np.nan
    if not prestations:
        return np.nan
    return prestations


def recherche_horaires(html_soup, ):
    """
    Crée la liste des horaires d'ouverture des restaurants par jour
    Si les horaires ne sont pas renseignées alors on retourne une valeur manquante
    :param html_soup: html du site dans le format de la bibliotheque beautifulsoup
    """
    horaires = []
    ul_horaires = html_soup.find("ul", class_="hidden liste-horaires-principaux")  # ul contenant les horaires
    try:
        li_horaires = ul_horaires.findAll("li", class_="horaire-ouvert")
        for li in li_horaires:
            jour = li.find('p')  # Recherche du jour
            heures = li.findAll("span", class_="horaire")  # Recherche des horaires pour ce jour
            un_jour = [jour.text.strip("\n")]
            for heure in heures:  # Ajout de toutes les heures
                un_jour += [heure.text.strip("\n")]
            horaires += un_jour
    except:
        return np.nan
    return horaires


def recherche_coord_gps(html_soup):
    """
    Retourne la liste des coordonnees gps du restaurant au format [longitude,latitude]
    :param html_soup: html du site dans le format de la bibliotheque beautifulsoup
    """
    try:
        div = html_soup.find("div", id="bloc-ouverture")
        url_json = json.loads(div.get("data-pjajax"))["url"]  # Valeur de la clé "url" du dictionnaire data-pjajax
        url = "https://www.pagesjaunes.fr/carte?" + url_json[len(url_json) - 72:]
        sleep(3)
        req = Request(url, headers={"User-Agent": "Mozilla/70.0"})
        html = urlopen(req).read()
        html_soup = BeautifulSoup(html, 'html.parser')
        button = html_soup.find("button",
                                class_="button large-button")  # Recherche de toutes les balises button
        coord = json.loads(button.get("data-pjcarto-itineraire"))["xyproqualif"]
        return coord  # Retourne les coordonnées au format [latitude,longitude]
    except:
        return [np.nan, np.nan]


def recherche_json(html_soup):
    """ 
    Récupère toutes les données utiles dans le code source au format JSON
    :param html_soup: html du site dans le format de la bibliotheque beautifulsoup
    """
    try:
        recherche = html_soup.findAll("script", attrs={'type': "application/ld+json"})
        try:
            recherche = json.loads(recherche[0].getText())[0]
            return [recherche['name'],
                    recherche["address"]["streetAddress"],
                    recherche["address"]["postalCode"],
                    recherche["address"]["addressLocality"],
                    recherche["telephone"],
                    recherche["servesCuisine"],
                    recherche["review"][0]["reviewRating"]["ratingValue"]]
        except KeyError:
            # pas de note ni de style cuisinaire
            return [recherche['name'],
                    recherche["address"]["streetAddress"],
                    recherche["address"]["postalCode"],
                    recherche["address"]["addressLocality"],
                    recherche["telephone"]]
    except :
        return None  # pas de json


def dicoVierge():
    res = {"Nom": [], "Adresse": [], "Code_Postal": [], "Ville": [], "Telephone": [], "Site_Internet": [], "Menu": [],
           "Prix_Menu": [], "Style_Culinaire": [], "Note": [], "Suggestion": [], "Prix_Suggestion": [],
           "Prestation": [], "Horaires": [], "Longitude": [], "Latitude": []}
    return res


def recuperation_des_donnees(url, dico):
    """
    Récupération de toutes les données (JSON ou non)
    :param url : lien de la page web
    :param dico : dictionnaire qui enregistre les données de la page
    returns : le dictionnaire après intégration des données 
    """
    sleep(4)
    req = Request(url, headers={"User-Agent": "Mozilla/70.0"})
    html = urlopen(req).read()
    html_soup = BeautifulSoup(html, 'html.parser')
    rows = html_soup.findAll("article")
    id_resto = []
    for row in rows:
        cells = row["id"]
        id_resto.append(cells[8:])
    for resto in id_resto:
        # pour chaque restaurant
        url = "https://www.pagesjaunes.fr/pros/detail?bloc_id=" + str(resto)  # accés aux differents liens
        req = Request(url, headers={"User-Agent": "Mozilla/70.0"})
        html = urlopen(req).read()
        html_soup = BeautifulSoup(html, 'html.parser')
        # Recuperation des données sur le json
        donnees_json = recherche_json(html_soup)
        # Ajout d'une valeur pour chaque colonne
        dico["Nom"].append(donnees_json[0] if donnees_json is not None else np.nan)
        dico["Adresse"].append(donnees_json[1] if donnees_json is not None else np.nan)
        dico["Code_Postal"].append(donnees_json[2] if donnees_json is not None else np.nan)
        dico["Ville"].append(donnees_json[3] if donnees_json is not None else np.nan)
        dico["Telephone"].append(donnees_json[4] if donnees_json is not None else np.nan)
        dico["Site_Internet"].append(recherche_site_web(html_soup))
        menu = recherche_menu(html_soup)  # Récupération du menu
        dico["Menu"].append([m[0] for m in menu] if menu is not None else np.nan)
        dico["Prix_Menu"].append([m[1] for m in menu] if menu is not None else np.nan)
        dico["Style_Culinaire"].append(
            np.nan if donnees_json is None else (donnees_json[5] if len(donnees_json) > 5 else np.nan))
        dico["Note"].append(np.nan if donnees_json is None else (donnees_json[6] if len(donnees_json) > 5 else np.nan))
        suggestions = recherche_suggestion(html_soup)  # Récupération des suggestions
        dico["Suggestion"].append([s[0] for s in suggestions] if suggestions is not None else np.nan)
        dico["Prix_Suggestion"].append([s[1] for s in suggestions] if suggestions is not None else np.nan)
        dico["Prestation"].append(recherche_prestation(html_soup))
        dico["Horaires"].append(recherche_horaires(html_soup))
        gps = recherche_coord_gps(html_soup)  # Récupération des coordonnées GPS
        dico["Longitude"].append(gps[0])
        dico["Latitude"].append(gps[1])
    return dico
