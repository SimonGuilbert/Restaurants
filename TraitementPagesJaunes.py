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


def recherche_suggestion(html_soup):
    """
    Crée la liste des suggestion du restaurant avec leur prix 
    Si les suggestions ne sont pas renseignées alors on retourne None
    :param html_soup: html du site dans le format de la bibliotheque beautifulsoup
    """
    suggestions = ""
    try:
        div_suggestions = html_soup.findAll("div", class_="marg-btm-xs row")  # div contenant les formules
        for div in div_suggestions:
            suggestion = div.find('span', class_="col-xs-10 description-mets")  # Recherche de l'intitule de la formule
            suggestions += suggestion.text+" / "
    except:
        return np.nan
    if suggestions == "":
        return np.nan
    return suggestions[:len(suggestions)-3]


def recherche_prestation(html_soup):
    """
    Crée la liste des prestations proposées par le restaurants
    Si les prestation ne sont pas renseignées alors on retourne une valeur manquante
    :param html_soup: html du site dans le format de la bibliotheque beautifulsoup
    """
    prestations = ""
    li_prestations = html_soup.findAll("li", class_="col-sm-6 marg-btm-s")  # li contenant les prestations
    try:
        for li in li_prestations:
            prestation = li.find('span')  # Recherche de l'intitule de la prestation
            prestations += prestation.text+" / "
    except:
        return np.nan
    if prestations == "":
        return np.nan
    return prestations[:len(prestations)-3]


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
    except:
        return None  # pas de json


def dicoVierge():
    res = {"Nom": [], "Adresse": [], "Code_Postal": [], "Ville": [], "Telephone": [], "Site_Internet": [],
           "Style_Culinaire": [], "Note": [], "Suggestion": [], "Prestation": [],
           "Horaires": [], "Longitude": [], "Latitude": []}
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
        if donnees_json is not None:
            dico["Nom"].append(donnees_json[0])
            dico["Adresse"].append(donnees_json[1])
            dico["Code_Postal"].append(donnees_json[2])
            dico["Ville"].append(donnees_json[3])
            dico["Telephone"].append(donnees_json[4])
            dico["Site_Internet"].append(recherche_site_web(html_soup))
            dico["Style_Culinaire"].append(donnees_json[5] if len(donnees_json) > 5 else np.nan)
            dico["Note"].append(donnees_json[6] if len(donnees_json) > 5 else np.nan)
            dico["Suggestion"].append(recherche_suggestion(html_soup))
            dico["Prestation"].append(recherche_prestation(html_soup))
            dico["Horaires"].append(recherche_horaires(html_soup))
            gps = recherche_coord_gps(html_soup)  # Récupération des coordonnées GPS
            try:
                dico["Longitude"].append(gps[0])
                dico["Latitude"].append(gps[1])
            except:
                dico["Longitude"].append(np.nan)
                dico["Latitude"].append(np.nan)
    return dico
