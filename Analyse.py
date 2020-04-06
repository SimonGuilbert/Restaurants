import pandas as pd
import matplotlib.pyplot as plt


class Analyse:
    def __init__(self, file):
        self.df = pd.DataFrame(pd.read_csv("data/" + file + ".csv", sep=";"))

    def Creaction_graphique(self):
        """
        :return: Permet de tracer tout les graphiques possibles
        """
        print("Creaction des graphiques en cours")
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
        plt.ylabel("Note entre 1 et 5 ")
        plt.savefig("data/Graphique/Notes.png")

    def Plot_Horraire(self):
        """
        :return: Sauvegarde le graphique en data/Graphiques/.png
        """
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
        """
        Trace le diagramme circulaire des styles culinaires des restaurants les plus fréquents
        :return: Sauvegarde le graphique en data/Graphique/Style_Culinaire.png
        """
        cuisine = {
            'Style': ["Restaurant Français", "Restaurant savoyard", "Pizzeria", "Restaurant Asiatique", "Fast-food",
                      "Autres régions du monde", "Autres"], 'Effectif': [0, 0, 0, 0, 0, 0, 0]}
        for style in self.df[self.df["Style_Culinaire"].notna()]["Style_Culinaire"]:

            if "français" in style:
                cuisine["Effectif"][0] += 1
            elif "savoyard" in style or "tartiflette" in style or "traditionnel" in style:
                cuisine["Effectif"][1] += 1
            elif "pizzeria" in style or "italien" in style:
                cuisine["Effectif"][2] += 1
            elif "asiatique" in style or "chinois" in style or "indien" in style or "japonais" in style or "thaï" in style or "vietnam" in style:
                cuisine["Effectif"][3] += 1
            elif "fast food" in style or "kebab" in style or "américain" in style or "mexicain" in style or "turc" in style or "rapide" in style or "sandwich" in style or "grec" in style:
                cuisine["Effectif"][4] += 1
            elif "monde" in style.lower():
                cuisine["Effectif"][5] += 1
            else:
                cuisine["Effectif"][6] += 1
        df_plot = pd.DataFrame(cuisine, columns=["Style", "Effectif"])
        df_plot.plot(kind='pie', y='Effectif', autopct='%1.0f%%', startangle=55,
                     labels=df_plot['Style'], legend=False, fontsize=14, figsize=(16, 8))
        plt.title("Diagramme circulaire sur les types de restaurant", fontsize=16)
        plt.savefig("data/Graphique/Style_Culinaire.png")
