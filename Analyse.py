import pandas as pd
import matplotlib.pyplot as plt


class Analyse:
    def __init__(self, file):
        self.df = pd.DataFrame(pd.read_csv("data/" + file + ".csv", sep=";"))

    def Creaction_graphique(self):
        print("Creaction Des graphiques en cours")
        self.Plot_Horraire()
        self.Plot_Note()
        print("Graphique Terminé, vous trouverez les fichiers :\n"
              " ♦ Note.png\n"
              " ♦ Horaire.png\n"
              "dans data\graphique du repertoire courant.")

    def Plot_Note(self):
        """
        Trace le graphique des note en fonction du nombre de fois quelle apparaisse

        :return: Graphique en PNG
        """
        Note = {'note': [], 'compteur': []}
        for i in self.df[self.df["Note"].notna()]["Note"]:
            if not i in Note["note"]:
                Note["note"].append(i)
                Note["compteur"].append(1)
            else:
                Note["compteur"][Note["note"].index(i)] += 1
        df_plot = pd.DataFrame(Note, columns=["note", "compteur"])
        df_plot.sort_values(by=["compteur"])
        df_plot.plot.bar(x="compteur", y="note")
        plt.title("Note en fonction du nombre d'occurence")
        plt.xlabel("Nombre d'occurence")
        plt.ylabel("Note entre 0 et 5 ")
        plt.grid(True)
        plt.savefig("data/Graphique/Note.png")

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
