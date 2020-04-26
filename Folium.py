# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 17:42:14 2020

@author: Jonathan Molieres
"""
# =============================================================================
# import
# =============================================================================
import folium as fl


# =============================================================================
# Class
# =============================================================================
class Carte:
    def __init__(self, coord=None):

        # Coordonnées par défaut = [45.89912, 6.12871] qui correspondent à Annecy
        if coord is None:
            coord = [45.89912, 6.12871]
        self.carte = fl.Map(location=coord,zoom_start=6)

    def marqueur(self, coordonnee, popupstr, tooltip):
        """
        Place un marqueur sur la carte
        Parameters
        ----------
        coordonnee : TYPE:Liste
            DESCRIPTION: Liste des coordonnees 
        tooltip : TYPE: String 
            DESCRIPTION: Message lorsque la souris passe sur un marqueur
        popupstr : TYPE: String
            DESCRIPTION: Message lorsqu'on clique sur le marqueur

        lien pour modifier l'apparence des icones : getbootstrap.com/docs/3.3/components/
        """
        fl.Marker(coordonnee, popup='<i>' + str(popupstr) + '</i>', tooltip=tooltip,
                  icon=fl.Icon(color='black', icon_color='orange', icon='glyphicon-cutlery')).add_to(self.carte)

    def save(self, fil='index.html'):
        self.carte.save("Resultats/" + fil) # Enregistre la carte dans le dossier Resultats
