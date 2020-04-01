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
    nbre_page = 0
    while nbre_page == 0:  # attente de reponse
        req = Request(url, data=None,
                      headers={
                          'User-Agent': "Mozilla/5.0 (windows net 10.0) AppleWebKit/537.36 (KHTML, like Gecko) " +
                                        "Chrome/35.0.1916.47 Safari/537.36 "
                      })
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
    return url + "&page=" + str(page)


# =============================================================================
# Traitement d'un restaurant
# =============================================================================

def recherche_site_web(html_soup):
    """
    Crée la liste des sites web des restaurants dont les identifiants sont donnés en paramètres
    Si le site n'existe pas ou n'est pas renseigner alors on ajout "NONE" à la liste
    :type html_soup: beautifulsoup
    :param html_soup: html du site dans le format de la bibliotheque beautifulsoup
    :return: la liste des site web des restaurants correspondant aux identifiants
    """
    div_sites = html_soup.find("div", class_="lvs-container marg-btm-s")  # div contenant l'adresse du site web
    try:
        for div in div_sites:
            site = div.find('span', class_="value")  # Recherche de l'adresse du site web
            return site.text
    except:
        return "None"


def recherche_menu(html_soup):
    """
    Crée la liste des menus des restaurants dont les identifiants sont donnés en paramètres
    Si le menu n'est pas renseigner alors on ajout "NONE" à la liste
    :type html_soup: beautifulsoup
    :param html_soup: html du site dans le format de la bibliotheque beautifulsoup
    :return: la liste des formules avec leurs prix des restaurants correspondant aux identifiants
    """

    formules = []
    try:
        div_formules = html_soup.findAll("div", class_="formule marg-btm-s row")  # div contenant les formules
        for div in div_formules:
            formule = div.find('p', class_="no-margin")  # Recherche de l'intitule de la formule
            prix = div.find('span', class_="tarif-formule")  # Recherche du prix de la formule
            formules += [formule.text, prix.text]
    except:
        formules += ["None", "None"]
    return formules


def recherche_suggestion(html_soup):
    """
    Crée la liste des suggestion des restaurants dont les identifiants sont donnés en paramètres
    Si les suggestions ne sont pas renseigner alors on ajout "NONE" à la liste
    :type html_soup: beautifulsoup
    :param html_soup: html du site dans le format de la bibliotheque beautifulsoup
    :return: la liste des suggestions avec leurs prix des restaurants correspondant aux identifiants
    """
    suggestions = []
    try:
        div_suggestions = html_soup.findAll("div", class_="marg-btm-xs row")  # div contenant les formules
        for div in div_suggestions:
            suggestion = div.find('span', class_="col-xs-10 description-mets")  # Recherche de l'intitule de la formule
            prix = div.find('span', class_="col-xs-2 tarif-mets")  # Recherche du prix de la formule
            suggestions += [suggestion.text, prix.text]
    except:
        suggestions += ["None", "None"]
    return suggestions


def recherche_prestation(html_soup):
    """
    Crée la liste des prestations des restaurants dont les identifiants sont donnés en paramètres
    Si les prestation ne sont pas renseigner alors on ajout "NONE" à la liste
    :type html_soup: beautifulsoup
    :param html_soup: html du site dans le format de la bibliotheque beautifulsoup
    :return: la liste des prestations des restaurants correspondant aux identifiants
    """
    prestations = []
    li_prestations = html_soup.findAll("li", class_="col-sm-6 marg-btm-s")  # li contenant les prestations
    try:
        for li in li_prestations:
            prestation = li.find('span')  # Recherche de l'intitule de la prestation
            prestations += [prestation.text]
    except:
        prestations += ["None"]
    return prestations


def recherche_horaires(html_soup, ):
    """
    Crée la liste des horaires des restaurants dont les identifiants sont donnés en paramètres
    Si les horaires ne sont pas renseigner alors on ajout "NONE" à la liste
    :type html_soup: beautifulsoup
    :param html_soup: html du site dans le format de la bibliotheque beautifulsoup
    :return: la liste des horaires des restaurants correspondant aux identifiants
    """
    horaires = []
    ul_horaires = html_soup.find("ul", class_="hidden liste-horaires-principaux")  # ul contenant les horaires
    try:
        li_horaires = ul_horaires.findAll("li", class_="horaire-ouvert")

        for li in li_horaires:
            jour = li.find('p')  # Recherche du jour
            heures = li.findAll("span", class_="horaire")  # Recherche des horaires pour ce jour
            un_jour = [jour.text]
            for heure in heures:  # Ajout de toutes les heures
                un_jour += [heure.text]
            horaires += un_jour
    except:
        horaires += ["None"]
    return horaires


def recherche_coord_gps(html_soup):
    try:
        div = html_soup.find("div", id="bloc-ouverture")

        url = json.loads(div.get("data-pjajax"))["url"]  # Valeur de la clé "url" du dictionnaire data-pjajax

        url = url[(len(url) - 38):]  # On enlève les 10 premiers caractères de gauche
        url = "https://www.pagesjaunes.fr/carte?" + url

        req = Request(url, headers={"User-Agent": "Mozilla/70.0"})
        html = urlopen(req).read()
        html_soup = BeautifulSoup(html, 'html.parser')
        button = html_soup.find("button",
                                class_="button secondaire-1 xs_large calculer")  # Recherche de toutes les balise button
        coord = button.get("data-pjcarto-itineraire")["xyproqualif"]
        return coord  # Retourne les coordonnées de la forme [latitude,longitude]
    except:
        return "None"


def recherche_json(html_soup):
    """"verifier les differents cas

    """
    recherche = html_soup.findAll("script", attrs={'type': "application/ld+json"})
    try:
        recherche = json.loads(recherche[0].getText())[0]
        return [recherche['name'], recherche["address"]["streetAddress"], recherche["address"]["postalCode"],
                recherche["address"]["addressLocality"], recherche["telephone"],
                recherche["servesCuisine"],
                recherche["review"][0]["reviewRating"]["ratingValue"]]

    except KeyError:
        # pas de note ni de style cuisinaire
        return [recherche['name'], recherche["address"]["streetAddress"],
                recherche["address"]["postalCode"],
                recherche["address"]["addressLocality"], recherche["telephone"],
                recherche["servesCuisine"], "None"]
    except IndexError:
        # pas de json
        return "None"


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
    sleep(4)
    req = Request(url, headers={"User-Agent": "Mozilla/70.0"})
    html = urlopen(req).read()
    html_soup = BeautifulSoup(html, 'html.parser')
    rows = html_soup.findAll("article")
    id_resto = []
    for row in rows:
        cells = row["id"]
        id_resto.append(cells[8:])
    print("nombre de restaurant sur la page=", len(id_resto))
    donne = {}

    for resto in id_resto:
        # pour chaque restaurant
        url = "https://www.pagesjaunes.fr/pros/detail?bloc_id=" + str(resto)  # accés aux differents liens
        req = Request(url, headers={"User-Agent": "Mozilla/70.0"})
        html = urlopen(req).read()
        html_soup = BeautifulSoup(html, 'html.parser')
        # recherche site
        nom_site = recherche_site_web(html_soup)
        # recherche des suggestions
        suggestion = recherche_suggestion(html_soup)
        # recherche des prestations
        prestation = recherche_prestation(html_soup)
        # recherche menu
        menu = recherche_menu(html_soup)
        # recherche horaires
        horaires = recherche_horaires(html_soup)
        # recuperation des données sur le json
        donnee_json = recherche_json(html_soup)
        # Recherche des coordonnees gps
        gps = recherche_coord_gps(html_soup)

        # ajout au dictionnaire :

        if donnee_json != "None":
            donne[donnee_json[0]] = []
            donne[donnee_json[0]].extend(nom_site)
            donne[donnee_json[0]].extend(menu)
            donne[donnee_json[0]].extend(horaires)
            donne[donnee_json[0]].extend(suggestion)
            donne[donnee_json[0]].extend(prestation)
        else:
            print("erreur")
    return donne
