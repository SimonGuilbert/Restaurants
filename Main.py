# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 09:37:08 2020

@author: Jonathan Molieres
"""
# =============================================================================
# Import
# =============================================================================
import TraitementPagesJaunes as TPJ
from Folium import Carte
import pandas

# =============================================================================
# Variables
# =============================================================================
url_accueil = "https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui=restaurant&ou=haute-savoie-74"
data = TPJ.dicoVierge()

# =============================================================================
# Main
# =============================================================================
if __name__ == "__main__":

    nbre_page = TPJ.nombre_de_page(url_accueil)
    for page in range(1, nbre_page+1):
        print("Traitement de la page : " + str(page) + "/" + str(nbre_page))
        url_page = TPJ.visiter_page(url_accueil, page)
        data = TPJ.recuperation_des_donnees(url_page, data)
    df = pandas.DataFrame(data) # Création du DataFrame
    df.drop_duplicates(subset=["Nom","Code_Postal","Telephone"], keep="first")
    df.to_csv('data/Restaurants.csv', sep=';') # Creation du CSV
    # Creation de la carte HTML
    carte = Carte()
    for resto in df[(df["Longitude"].notna()) & (df["Latitude"].notna())].itertuples():
        carte.marqueur([resto.Longitude, resto.Latitude], resto.Nom, "Cliquez pour afficher le restaurant")
    carte.save("Restaurants.html")
    print("\nTraitement terminé. Vous trouverez les fichiers\n  "
          "♦ Restaurants.csv\n  ♦ Restaurants.html\n"
          "Dans le répertoire courant")
