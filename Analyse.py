import pandas as pd
import matplotlib.pyplot as plt


class Analyse:
    def __init__(self, file):
        self.df = pd.DataFrame(pd.read_csv("data/" + file + ".csv", sep=";"))

    def Creaction_graphique(self):
        print("Creaction Des graphiques en cours")
        self.Plot_Horraire()
        self.Plot_Note()
        self.Plot_camembert_style_culinaire()
        print("Graphique Terminé, vous trouverez les fichiers :\n"
              " ♦ Note.png\n"
              " ♦ Horaire.png\n"
              " ♦ Style_culinaire.png\n"
              "dans data\graphique du repertoire courant.")

    def Plot_Note(self):
        """
        Trace le graphique du nombre d'occurences en fonction de la note attribuée
        :return: Sauvegarde le graphique en data/Graphiques/Notes.png
        """
        Note = {"NoteSur5": ["1/5", "2/5", "3/5", "4/5", "5/5"], "Effectif": [0, 0, 0, 0, 0]}
        for i in self.df[self.df["Note"].notna()]["Note"]:
            Note["Effectif"][int(i) - 1] += 1
        df_plot = pd.DataFrame(Note)
        df_plot.plot.barh(x="NoteSur5", y="Effectif")
        plt.title("Nombre d'occurences en fonction de la note attribuée")
        plt.xlabel("Nombre d'occurences")
        plt.ylabel("Note entre 0 et 5 ")
        plt.savefig("data/Graphique/Notes.png")

    def Plot_Horraire(self):
        dico_horaire = {"horaire": [], "occurence": []}

        for horaire_string in self.df[self.df["Note"].notna()]["Horaires"]:
            liste_horaires = []
            try:
                liste_horaires = horaire_string.strip("\n").strip("[").strip("]").split(',')
            except AttributeError:
                # nan values
                pass
            for horaire in liste_horaires:
                h = horaire[2: len(horaire) - 1]
                if "-" in h:
                    # plage d'horaire
                    if not h in dico_horaire["horaire"]:
                        dico_horaire["horaire"].append(h)
                        dico_horaire["occurence"].append(1)
                    else:
                        dico_horaire["occurence"][dico_horaire["horaire"].index(h)] += 1

        df_plot = pd.DataFrame(dico_horaire, columns=["horaire", "occurence"])
        df_plot.sort_values(by=["occurence"])
        df_plot.plot.bar(y="occurence", x="horaire")
        plt.title("Heure d'ouverture en fonction du nombre d'occurence")
        plt.xlabel("Nombre d'occurence")
        plt.ylabel("horaire ")
        plt.grid(True)
        plt.savefig("data/Graphique/Horaire.png")

    def Plot_camembert_style_culinaire(self):
        cuisine = {'Style': ["Restaurant Français", "divers"], 'compteur': [0, 11]}
        for i in self.df[self.df["Style_Culinaire"].notna()]["Style_Culinaire"]:
            if "français" in i:
                cuisine["compteur"][0] += 1
            elif not i in cuisine["Style"]:
                cuisine["Style"].append(i)
                cuisine["compteur"].append(1)
            else:
                cuisine["compteur"][cuisine["Style"].index(i)] += 1
        print(cuisine)
        for valeur_compteur in cuisine["compteur"][2:]:
            if valeur_compteur <= 10:
                cuisine["Style"].pop(cuisine["compteur"].index(valeur_compteur))
                cuisine['compteur'].remove(valeur_compteur)
                cuisine['compteur'][1] += 1
        print(cuisine)
        df_plot = pd.DataFrame(cuisine, columns=["Style", "compteur"], index=cuisine["Style"])
        df_plot.plot.pie(y="compteur")
        plt.title("diagramme en camembert sur les types de restaurant")
        plt.savefig("data/Graphique/Style_Culinaire.png")
