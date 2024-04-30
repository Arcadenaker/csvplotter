# IMPORTANT: tous les fichiers csv doivent être dans le même répertoire que ce code
#            Une image nommée "graphique.png" sera générée dans le répertoire courant
#            La configuration des graphes se fait dans la section CONFIG

import matplotlib.pyplot as plt
import os
import numpy as np

def choisir_fichier_csv():
    fichiers = os.listdir()
    fichiers_csv = [f for f in fichiers if f.endswith('.csv')]
    if len(fichiers_csv) == 0:
        print("Aucun fichier CSV trouvé dans le répertoire.")
        exit()
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

file1, file2, file3 = choisir_fichier_csv()

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

# Configuration des graphes du premier fichier
graphe1_1 = True;header1[1] = "Vin";dephasage_1_1=0
if len(header1) > 2:
    graphe2_1 = False;header1[2] = "Après R";dephasage_2_1=0
if len(header1) > 3:
    graphe3_1 = False;header1[3] = "Bornes de la résistance";dephasage_3_1=0

# Configuration des graphes du deuxième fichier
if file2:
    graphe1_2 = True;header2[1] = "Vin";dephasage_1_2=0
    if len(header2) > 2:
        graphe2_2 = False;header2[2] = "Après R";dephasage_2_2=0
    if len(header2) > 3:
        graphe3_2 = False;header2[3] = "Bornes de la résistance";dephasage_3_2=0

# Configuration des graphes du troisième fichier
if file3:
    graphe1_3 = True;header3[1] = "Vin";dephasage_1_3=0
    if len(header3) > 2:
        graphe2_3 = False;header3[2] = "Après R";dephasage_2_3=0
    if len(header3) > 3:
        graphe3_3 = False;header3[3] = "Bornes de la résistance";dephasage_3_3=0

# Configuration des bornes des axes X
borneInfAxeY = 0;borneSuppAxeY = 3 # 0 si pas de borne

# Configuration des bornes des axes Y
borneInfAxeX = 0;borneSuppAxeX = 200 # 0 si pas de borne

# Configuration d'une évenbtuelle fonction lambda
use_lambda = True
f_lambda = lambda x: np.sin(x/10) + 1
label_lambda = "SIN X/10 + 1"
dephasage_lambda = 0


############################################################
############################################################
############################################################


# Plot des canaux du premier fichier
plt.plot([t + dephasage_1_1 for t in time1], canal1_1, label=header1[1])
if canal2_1:
    plt.plot([t + dephasage_2_1 for t in time1], canal2_1, label=header1[2])
if canal3_1:
    plt.plot([t + dephasage_3_1 for t in time1], canal3_1, label=header1[3])

# Plot des canaux du deuxième fichier
if file2:
    plt.plot([t + dephasage_1_2 for t in time2], canal1_2, label=header2[1])
    if canal2_2:
        plt.plot([t + dephasage_2_2 for t in time2], canal2_2, label=header2[2])
    if canal3_2:
        plt.plot([t + dephasage_3_2 for t in time2], canal3_2, label=header2[3])

# Plot des canaux du troisième fichier
if file3:
    plt.plot([t + dephasage_1_3 for t in time3], canal1_3, label=header3[1])
    if canal2_3:
        plt.plot([t + dephasage_2_3 for t in time3], canal2_3, label=header3[2])
    if canal3_3:
        plt.plot([t + dephasage_3_3 for t in time3], canal3_3, label=header3[3])

if use_lambda:
    x = [i for i in range(0, 1000)]
    y = [f_lambda(i) for i in x]
    plt.plot([t + dephasage_lambda for t in x], y, label=label_lambda)

# Configurations de l'axe
if borneSuppAxeY != 0 or borneInfAxeY != 0:
    plt.ylim(borneInfAxeY, borneSuppAxeY) # Pour changer les bornes de l'axe des ordonnées
if borneSuppAxeX != 0 or borneInfAxeX != 0:
    plt.xlim(borneInfAxeX, borneSuppAxeX) # Pour changer les bornes de l'axe des abscisses

plt.xlabel("Temps [µs]")
plt.ylabel("Tension [V]")
plt.legend(loc='upper right')
plt.savefig("graphique.png")
plt.show()