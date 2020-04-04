import pandas as pd
import matplotlib.pyplot as plt


class Analyse:
    def __init__(self, file):
        self.df = pd.DataFrame(pd.read_csv("data/" + file + ".csv", sep=";"))

    def Creaction_graphique(self):
        print("Création Des graphiques en cours")
        self.Plot_Note()
        self.Plot_Horraire()
        print("Graphique Terminé, vous trouverez les fichiers :\n"
              " ♦ Note.png\n"
              " ♦ Horaire.png\n"
              "dans data\Graphiques du repertoire courant.")

    def Plot_Note(self):
        """
        Trace le graphique du nombre d'occurences en fonction de la note attribuée
        :return: Sauvegarde le graphique en data/Graphiques/Notes.png
        """
        Note = {"NoteSur5":["1/5","2/5","3/5","4/5","5/5"], "Effectif":[0,0,0,0,0]}
        for i in self.df[self.df["Note"].notna()]["Note"]:
            Note["Effectif"][int(i)-1] += 1
        df_plot = pd.DataFrame(Note)
        df_plot.plot.barh(x="NoteSur5", y="Effectif")
        plt.title("Nombre d'occurences en fonction de la note attribuée")
        plt.xlabel("Nombre d'occurences")
        plt.ylabel("Note entre 0 et 5 ")
        #plt.grid(False)
        plt.savefig("data/Graphiques/Notes.png")

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
        plt.savefig("data/Graphiques/Horaire.png")
