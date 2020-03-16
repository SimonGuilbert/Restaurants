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
    with open("restaurant.csv",'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',quotechar=';',quoting=csv.QUOTE_MINIMAL)
        for nom_restaurant in donne.keys():
            print([nom_restaurant]+donne[nom_restaurant])
            spamwriter.writerow([nom_restaurant]+donne[nom_restaurant])
# =============================================================================
# Variable
# =============================================================================
url_acceuil="https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui=restaurant&ou=haute-savoie-74"
donne={}
if __name__ == "__main__":
    nbre_page=TPJ.nombre_de_page(url_acceuil)
    for page in range(1,3):
        url_page=TPJ.visiter_page(url_acceuil, page)
        donne.update(TPJ.recuperation_des_json(url_page))
    print(len(donne))

    # Creaction du CSV
    to_CSV(donne)
        

