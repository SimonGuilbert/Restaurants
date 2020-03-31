# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 09:37:08 2020

@author: Jonathan Molieres
"""
# =============================================================================
# Import
# =============================================================================
import TraitementPagesJaunes as TPJ
import csv


# =============================================================================
# Fonction
# =============================================================================
def to_CSV(donne):
    with open("data/restaurant.csv", 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["Name ", "address ", "Ville ", "Code postal ", "telephone ", "site",
                             "type de restaurant, cuisine,style cuisinaire", "Note ", "menu ", "suggestion ",
                             "prestation ", "horaire "])
        for nom_restaurant in donne.keys():
            spamwriter.writerow([nom_restaurant] + donne[nom_restaurant])
    print("CSV terminé à l'emplacement data/restaurant.csv du repertoire courant")


# =============================================================================
# Variable
# =============================================================================
url_acceuil = "https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui=restaurant&ou=haute-savoie-74"
donne = {}
if __name__ == "__main__":
    nbre_page = TPJ.nombre_de_page(url_acceuil)
    for page in range(1, 5):
        url_page = TPJ.visiter_page(url_acceuil, page)
        donne.update(TPJ.recuperation_des_donnees(url_page))
    # Creaction du CSV
    print(len(donne))
    to_CSV(donne)
