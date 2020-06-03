# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 09:24:46 2020

@author: simon
"""

from bokeh.plotting import figure, output_file, show, save
from bokeh.layouts import layout,grid
from bokeh.palettes import Blues, Oranges
from bokeh.transform import cumsum
from Folium import Carte
import pandas as pd
from math import pi
import os.path

class AnalyseBokeh:
    def __init__(self,fichier1,fichier2 = ""):
        self.fichier1 = fichier1
        self.fichier2 = fichier2
        self.nom_departement1 = self.fichier1[22:len(fichier1)-4]
        self.df1 = pd.DataFrame(pd.read_csv(fichier1, sep=","))
        if self.fichier2 != "":
            self.df2 = pd.DataFrame(pd.read_csv(fichier2, sep=","))
            self.nom_departement2 = self.fichier2[22:len(fichier2)-4]
        else:
            self.df2 = None
        self.longueur = 375
        self.largeur = 310
        self.rayon = 0.35
        self.carteHtml()
        self.afficher()
        
# =============================================================================
# Histogramme
# =============================================================================

    def histogramme(self,df):
        couleur = ("SteelBlue" if df.equals(self.df1) else "orangered")
        titre = "Nombre de restaurants ouverts ("+(self.nom_departement1 if df.equals(self.df1) else self.nom_departement2)+")"
        dico_horaires = {"eff": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                "plage": ["00h00 - 00h59","01h00 - 01h59","02h00 - 02h59","03h00 - 03h59","04h00 - 04h59","05h00 - 05h59",
                          "06h00 - 06h59","07h00 - 07h59","08h00 - 08h59","09h00 - 09h59","10h00 - 10h59","11h00 - 11h59",
                          "12h00 - 12h59","13h00 - 13h59","14h00 - 14h59","15h00 - 15h59","16h00 - 16h59","17h00 - 17h59",
                          "18h00 - 18h59","19h00 - 19h59","20h00 - 20h59","21h00 - 21h59","22h00 - 22h59","23h00 - 23h59"]}
        for horaire_string in df[df["Horaires"].notna()]["Horaires"]:
            horaire_string = horaire_string.replace("'","").replace(" ","").replace("[","").replace("]","").replace("\\n","")
            liste_horaires = horaire_string.split(',')
            i = 0
            while i < len(liste_horaires)-1:
                if len(liste_horaires[i]) < 11: # Si c'est un nom de jour (et pas un horaire)
                    while i != len(liste_horaires)-1 and len(liste_horaires[i+1]) == 11: # Tant que c'est un horaire
                        deb = int(liste_horaires[i+1][:2])
                        fin = int(liste_horaires[i+1][6:8])+(-1 if int(liste_horaires[i+1][-2:]) == 0 else 0)
                        fin = (fin-24 if fin>23 else (23 if fin == -1 else fin))
                        j = deb
                        if deb<fin:
                            while j<=fin:
                                dico_horaires["eff"][j] += 1
                                j += 1
                        else:
                            while j<24:
                                dico_horaires["eff"][j] += 1
                                j += 1
                            j = 0
                            while j<=fin:
                                dico_horaires["eff"][j] += 1
                                j += 1
                        i+=1  
                    i+=1
                else:
                    i+=1      
    
        # Bokeh
        df = pd.DataFrame(dico_horaires) 
        df["eff"] = round(df["eff"]/6) # Chaque restaurant a à peu près 1 jour de repos par semaine
        df["eff"] = df['eff'].astype('int')
        df["horaire"] = df["plage"].str[:3]
        hist = figure(x_range=df["horaire"], plot_height=self.largeur, plot_width=self.longueur,toolbar_location=None,  
                   title=titre,tooltips=[("Restaurants ouverts", "@eff"), ("Plage horaire", "@plage")],
                   x_axis_label = "Plage horaire", y_axis_label = "Nombre de restaurants ouverts")
        hist.vbar(x='horaire', top='eff', width=0.9, source=df,
               line_color='white', fill_color=couleur, hover_fill_color = "lightgray")
        hist.xgrid.grid_line_color = None
        hist.ygrid.grid_line_color = None
        return hist
    
# =============================================================================
# Barplot    
# =============================================================================
        
    def barplot(self,df):
        couleur = ("SteelBlue" if df.equals(self.df1) else "orangered")
        titre = "Note moyenne des restaurants ("+(self.nom_departement1 if df.equals(self.df1) else self.nom_departement2)+")"
        Note = {"NoteSur5": ["1/5", "2/5", "3/5", "4/5", "5/5"], "Effectif": [0, 0, 0, 0, 0]}
        for i in df[df["Note"].notna()]["Note"]:
            Note["Effectif"][int(i) - 1] += 1
        
        # Bokeh
        df = pd.DataFrame(Note)
        barplot = figure(y_range=df["NoteSur5"],plot_height = self.largeur, plot_width = self.longueur,toolbar_location=None,
                         title=titre,
                         tooltips=[("Note moyenne", "@NoteSur5"), ("Nombre de notes", "@Effectif")],
                         x_axis_label = "Nombre de notes", y_axis_label = "Note moyenne entre 1 et 5")
        barplot.hbar(right='Effectif', y='NoteSur5', height=0.5, source=df,line_color='white',
                     fill_color=couleur, hover_fill_color = "lightgray")
        barplot.xgrid.grid_line_color = None
        barplot.ygrid.grid_line_color = None
        return barplot
    
# =============================================================================
# Pie chart
# =============================================================================
        
    def pieChart(self,fichier):
        df = (self.df1 if fichier == self.fichier1 else self.df2)
        titre = "Répartition des restaurants par type ("+(self.nom_departement1 if df.equals(self.df1) else self.nom_departement2)+")"
        cuisine = {
            'Style': ["Restaurant Français", ("Restaurant savoyard" if "74" in fichier else "Restaurant méditerranéen"), "Pizzeria", "Restaurant Asiatique", "Fast-food",
                      "Autres régions du monde", "Autres"], 'Effectif': [0, 0, 0, 0, 0, 0, 0]}
        for style in df[df["Style_Culinaire"].notna()]["Style_Culinaire"]:
            if "français" in style:
                cuisine["Effectif"][0] += 1
            elif "savoyard" in style or "tartiflette" in style or "traditionnel" in style and cuisine["Style"][1]=="Restaurant savoyard":
                cuisine["Effectif"][1] += 1
            elif "méditerranée" in style or "provençal" in style or "marocain" in style and cuisine["Style"][1]=="Restaurant méditerranéen":
                cuisine["Effectif"][1] += 1
            elif "pizzeria" in style or "italien" in style:
                cuisine["Effectif"][2] += 1
            elif "asiatique" in style or "chinois" in style or "indien" in style or "japonais" in style or "thaï" in style or "vietnam" in style:
                cuisine["Effectif"][3] += 1
            elif "fast food" in style or "kebab" in style or "américain" in style or "mexicain" in style or "turc" in style or "rapide" in style or "sandwich" in style or "grec" in style or "frites" in style:
                cuisine["Effectif"][4] += 1
            elif "monde" in style.lower():
                cuisine["Effectif"][5] += 1
            else:
                cuisine["Effectif"][6] += 1
        
        # Bokeh
        df = pd.DataFrame(cuisine)
        df['angle'] = df['Effectif']/df['Effectif'].sum() * 2*pi
        df["pourcentage"] = round((df["Effectif"]/df['Effectif'].sum())*100)
        df["pourcentage"]  = df["pourcentage"].astype('int').astype('str')+"%" # Conversion en int puis en str + "%"
        df['couleur'] = (Blues[len(df)] if fichier == self.fichier1 else Oranges[len(df)])
        pie = figure(plot_height = self.largeur, plot_width = self.longueur,title=titre, toolbar_location=None,
           tooltips=[("Type de restaurant","@Style"),("Pourcentage", "@pourcentage")], x_range=(-0.5, 1.0))
        pie.wedge(x=0, y=1, radius=self.rayon,start_angle=cumsum('angle', include_zero=True),fill_color="couleur",
                  end_angle=cumsum('angle'),line_color="white",legend = "Style", source=df,hover_fill_color = "lightgray")
        pie.axis.visible=False
        pie.grid.grid_line_color = None
        return pie
    
    
# =============================================================================
# Création des fichiers
# =============================================================================
        
    def sauvegardeGraphs(self,fichier,couleur):
        df = (self.df1 if fichier == self.fichier1 else self.df2)
        res = [self.histogramme(df)]
        res.append(self.barplot(df))
        res.append(self.pieChart(fichier))
        return res
    
         
    def afficher(self):
        output_file("Resultats/Dashboard.html")
        if self.df2 is None:
            res = grid([self.histogramme(self.df1),self.barplot(self.df1),self.pieChart(self.fichier1)],
                        ncols=3,sizing_mode='stretch_width')
        else:
            res = layout(self.sauvegardeGraphs(self.fichier1,"SteelBlue"),self.sauvegardeGraphs(self.fichier2,"orangered"), 
                         sizing_mode='stretch_both')
        save(res)
        curdoc().theme = 'dark_minimal'
        
        
    def carteHtml(self):        
        # Creation de la carte HTML
        carte = Carte()
        for resto in self.df1[(self.df1["Longitude"].notna()) & (self.df1["Latitude"].notna())].itertuples():
            carte.marqueur([resto.Longitude, resto.Latitude], resto.Nom, "Cliquez pour afficher le restaurant")
        if self.fichier2 != "":
            for resto in self.df2[(self.df2["Longitude"].notna()) & (self.df2["Latitude"].notna())].itertuples():
                carte.marqueur([resto.Longitude, resto.Latitude], resto.Nom, "Cliquez pour afficher le restaurant")
        carte.save("Restaurants.html")
        
if __name__ == "__main__":
    print("                       _\n     /\               | | \n    /  \   _ __   __ _| |_   _ ___  ___\n   / /\ \ | '_ \ / _` | | | | / __|/ _ \ \n  / ____ \| | | | (_| | | |_| \__ \  __/\n /_/    \_\_| |_|\__,_|_|\__, |___/\___|\n                          __/ |\n                         |___/ ")
    print("\n♦ Avant d'utiliser ce programme vous devez avoir généré avec succès au moins un fichier csv à l'aide du programme Main.py")
    print("\n♦ Entrez le nom du premier fichier csv que vous souhaitez analyser")
    f1 = input("Nom du fichier de la forme 'Restaurants-HAUTE-SAVOIE-74.csv' : ")
    while not os.path.isfile("Resultats/"+f1):
        print("\nLe fichier est introuvable. Veuillez réessayer")
        f1 = input("Entrez le nom du fichier de la forme 'Restaurants-HAUTE-SAVOIE-74.csv' : ")
    print("\n♦ Le premier fichier a bien été pris en compte. Voulez-vous ajouter un autre fichier à analyser ?")
    f2 = input("Répondez oui ou non : ")
    while f2 not in ["oui","non"]:
        f2 = input("Saisie incorrecte. Répondez oui ou non : ")
    if f2 == "non":
        AnalyseBokeh("Resultats/"+f1)
    else:
        f2 = input("Entrez le nom du deuxième fichier : ")
        while not os.path.isfile("Resultats/"+f2):
            print("\nLe fichier est introuvable. Veuillez réessayer : ")
            f2 = input("Entrez le nom du deuxième fichier : ")
        print("\nCréation des graphiques en cours ...")
        AnalyseBokeh("Resultats/"+f1,"Resultats/"+f2)
    print("\nTraitement terminé avec succès. Vous trouverez les fichiers :")
    print("  ♦ Dashboard.html \n  ♦ Restaurants.html\nDans le dossier Resultats du répertoire courant")
