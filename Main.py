# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 09:37:08 2020

@author: Jonathan Molieres
"""
# =============================================================================
# Import
# =============================================================================
import TraitementPagesJaunes as TPJ
import pandas

# =============================================================================
# Affichage des départements français
# =============================================================================
def listeDep(): # Affiche la liste des départements français
    df = pandas.DataFrame(pandas.read_csv("data/departements-france.csv",sep=","))
    return df
    

# =============================================================================
# Variables
# =============================================================================
print(" ____  _ \n|  _ \(_)\n| |_) |_  ___ _ ____   _____ _ __  _   _  ___ \n|  _ <| |/ _ \ '_ \ \ / / _ \ '_ \| | | |/ _ \ \n| |_) | |  __/ | | \ V /  __/ | | | |_| |  __/\n|____/|_|\___|_| |_|\_/ \___|_| |_|\__,_|\___|")
print("\n♦ Choisissez le code du département à traiter. \n♦ Entre 01 et 95 \n♦ Ou bien entre 971 et 976 pour les DOM-TOM")                                
choix = input("Choix du département, par exemple 74 : ")  

url_accueil = "https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui=restaurant&ou="+choix    

for dep in listeDep()[listeDep()["code_departement"] == choix]["nom_departement"]:
    nom_dep = dep.upper() # Recherche du nom du département choisi               

data = TPJ.dicoVierge()

# =============================================================================
# Main
# =============================================================================
if __name__ == "__main__":

    nbre_page = TPJ.nombre_de_page(url_accueil)
    print("\n♦ Vous avez choisi de traiter les restaurants de "+nom_dep+"\n")
    print("♦ Création du fichier CSV en cours ...\n")
    print("♦ Le temps de traitement est estimé à 3 heures\n")
    print("♦ Une fois le traitement terminé, vous pourrez générer un dashboard "+
          "en exécutant le programme 'AnalyseBokeh.py'.\n\n")
    for page in range(1, nbre_page+1):
        print("Traitement de la page : " + str(page) + "/" + str(nbre_page)) 
        url_page = TPJ.visiter_page(url_accueil, page)
        try:
            data = TPJ.recuperation_des_donnees(url_page, data)
        except:
            print("ATTENTION : impossible de lire la page "+url_page)
    df = pandas.DataFrame(data) # Création du DataFrame
    df = df.drop_duplicates(subset=["Nom","Code_Postal","Telephone"], keep="first")
    fichier = "Restaurants"+"-"+nom_dep+"-"+choix+".csv"
    df.to_csv("Resultats/"+fichier, sep=";") # Creation du CSV
    print("\nTraitement terminé. Vous trouverez le fichier",fichier,"dans le dossier Resultats du répertoire courant")
