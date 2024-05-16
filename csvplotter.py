# IMPORTANT: tous les fichiers csv doivent être dans le même répertoire que ce code
#            Une image nommée "graphique.png" sera générée dans le répertoire courant
#            La configuration des graphes se fait dans la section CONFIG

import matplotlib.pyplot as plt
import os
import numpy as np


    for i, fichier in enumerate(fichiers_csv):
        print(f"{i+1}. {fichier}")
    choix = int(input("Entrez le numéro du premier fichier CSV à utiliser: ")) - 1
    choix2 = int(input("Entrez le numéro du deuxième fichier CSV à utiliser (-1 si aucun): ")) - 1
    if choix2 == -2:
        return fichiers_csv[choix], False, False
    choix3 = int(input("Entrez le numéro du troisième fichier CSV à utiliser (-1 si aucun): ")) - 1
    if choix3 == -2:
        return fichiers_csv[choix], fichiers_csv[choix2], False
    return fichiers_csv[choix], fichiers_csv[choix2], fichiers_csv[choix3]

file1, file2, file3 = choose_csv_file()

def process_file(file):
    rows = []
    for row in file:
        rows.append(row.replace(",",".").split(';'))

    header = rows[0]
    rows = rows[3:]

    time = []
    canal1 = []
    canal2 = []
    canal3 = []

    min_time = float(rows[0][0])
    for row in rows:
        time_val = float(row[0])
        if time_val < min_time:
            min_time = time_val

    for row in rows:
        time_val = float(row[0]) - min_time

        if time_val < 0:
            time_val = 0

        time.append(time_val)
        canal1.append(float(row[1]))
        if len(row) > 2:
            canal2.append(float(row[2]))
        if len(row) > 3:
            canal3.append(float(row[3]))

    return time, canal1, canal2, canal3, header

# Lecture et traitement des données du premier fichier
time1, canal1_1, canal2_1, canal3_1, header1 = process_file(open(file1, 'r').readlines())

# Lecture et traitement des données du deuxième fichier
if file2:
    time2, canal1_2, canal2_2, canal3_2, header2 = process_file(open(file2, 'r').readlines())

# Lecture et traitement des données du troisième fichier
if file3:
    time3, canal1_3, canal2_3, canal3_3, header3 = process_file(open(file3, 'r').readlines())


############################################################
############################################################
########################## CONFIG ##########################

unite_temps = "ms" # Unité de temps pour l'axe des abscisses

# Configuration des graphes du premier fichier
graphe1_1 = True
header1[1] = "Vin"
dephasage_1_1=0
decalage_vertical_1_1=0
if len(header1) > 2:
    graphe2_1 = False
    header1[2] = "Après R"
    dephasage_2_1=0
    decalage_vertical_2_1=0
if len(header1) > 3:
    graphe3_1 = False
    header1[3] = "Bornes de la résistance"
    dephasage_3_1=0
    decalage_vertical_3_1=0

# Configuration des graphes du deuxième fichier
if file2:
    graphe1_2 = False
    header2[1] = "Vin"
    dephasage_1_2=0
    decalage_vertical_1_2=0
    if len(header2) > 2:
        graphe2_2 = False
        header2[2] = "Après R"
        dephasage_2_2=0
        decalage_vertical_2_2=0
    if len(header2) > 3:
        graphe3_2 = True
        header2[3] = "Sans condensateur"
        dephasage_3_2=0
        decalage_vertical_3_2=0

# Configuration des graphes du troisième fichier
if file3:
    graphe1_3 = False
    header3[1] = "Vin"
    dephasage_1_3=0
    decalage_vertical_1_3=0
    if len(header3) > 2:
        graphe2_3 = False
        header3[2] = "Après R"
        dephasage_2_3=0
        decalage_vertical_2_3=0
    if len(header3) > 3:
        graphe3_3 = True
        header3[3] = "Avec condensateur"
        dephasage_3_3=0
        decalage_vertical_3_3=0

# Configuration des bornes des axes X
borneInfAxeY = None;borneSuppAxeY = None # None si pas de borne

# Configuration des bornes des axes Y
borneInfAxeX = 0;borneSuppAxeX = 4.5 # None si pas de borne

# Configuration d'une évenbtuelle fonction lambda
use_lambda = False
f_lambda = lambda x: np.sin(x/10) + 1
label_lambda = "SIN X/10 + 1"
dephasage_lambda = 0


############################################################
############################################################
############################################################


# Plot des canaux du premier fichier
if graphe1_1:
    x_data = [t + dephasage_1_1 if dephasage_1_1 else t for t in time1]
    y_data = [t + decalage_vertical_1_1 if decalage_vertical_1_1 else t for t in canal1_1]
    plt.plot(x_data, y_data, label=header1[1])

if canal2_1 and graphe2_1:
    x_data = [t + dephasage_2_1 if dephasage_2_1 else t for t in time1]
    y_data = [t + decalage_vertical_2_1 if decalage_vertical_2_1 else t for t in canal2_1]
    plt.plot(x_data, y_data, label=header1[2])

if canal3_1 and graphe3_1:
    x_data = [t + dephasage_3_1 if dephasage_3_1 else t for t in time1]
    y_data = [t + decalage_vertical_3_1 if decalage_vertical_3_1 else t for t in canal3_1]
    plt.plot(x_data, y_data, label=header1[3])

# Plot des canaux du deuxième fichier
if file2:
    if graphe1_2:
        x_data = [t + dephasage_1_2 if dephasage_1_2 else t for t in time2]
        y_data = [t + decalage_vertical_1_2 if decalage_vertical_1_2 else t for t in canal1_2]
        plt.plot(x_data, y_data, label=header2[1])
        
    if canal2_2 and graphe2_2:
        x_data = [t + dephasage_2_2 if dephasage_2_2 else t for t in time2]
        y_data = [t + decalage_vertical_2_2 if decalage_vertical_2_2 else t for t in canal2_2]
        plt.plot(x_data, y_data, label=header2[2])
        
    if canal3_2 and graphe3_2:
        x_data = [t + dephasage_3_2 if dephasage_3_2 else t for t in time2]
        y_data = [t + decalage_vertical_3_2 if decalage_vertical_3_2 else t for t in canal3_2]
        plt.plot(x_data, y_data, label=header2[3])

# Plot des canaux du troisième fichier
if file3:
    if graphe1_3:
        x_data = [t + dephasage_1_3 if dephasage_1_3 else t for t in time3]
        y_data = [t + decalage_vertical_1_3 if decalage_vertical_1_3 else t for t in canal1_3]
        plt.plot(x_data, y_data, label=header3[1])

    if canal2_3 and graphe2_3:
        x_data = [t + dephasage_2_3 if dephasage_2_3 else t for t in time3]
        y_data = [t + decalage_vertical_2_3 if decalage_vertical_2_3 else t for t in canal2_3]
        plt.plot(x_data, y_data, label=header3[2])

    if canal3_3 and graphe3_3:
        x_data = [t + dephasage_3_3 if dephasage_3_3 else t for t in time3]
        y_data = [t + decalage_vertical_3_3 if decalage_vertical_3_3 else t for t in canal3_3]
        plt.plot(x_data, y_data, label=header3[3])


if use_lambda:
    x = np.arange(1000)
    y = f_lambda(x)
    plt.plot(x + dephasage_lambda if dephasage_lambda else x, y, label=label_lambda)

# Configurations de l'axe
if borneSuppAxeY or borneInfAxeY:
    plt.ylim(borneInfAxeY, borneSuppAxeY) # Pour changer les bornes de l'axe des ordonnées
if borneSuppAxeX or borneInfAxeX:
    plt.xlim(borneInfAxeX, borneSuppAxeX) # Pour changer les bornes de l'axe des abscisses

plt.xlabel(f"Temps [{unite_temps}]")
plt.ylabel("Tension [V]")
plt.legend(loc='upper right')
plt.grid()
plt.savefig("graphique.png")
plt.show()
