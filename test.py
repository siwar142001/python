#-------------------------------------------
# Programme principal
#-------------------------------------------

# !!! utilisez bien ma_var pour stocker le résultat de vos opérations !!!!

# Inversion d'une chaîne de caractères
ma_var = "Arcreane"
ma_new_var = ""
for i in range(len(ma_var) - 1, -1, -1):
    ma_new_var += ma_var[i]
ma_var = ma_new_var
print(ma_var)

#-------------------------------------------
# Comptage d'occurrences dans une liste
#-------------------------------------------

ma_liste = [2, 65, 42, 53, 27, 2, 42, 27, 2, 53, 53, 53, 65, 21, 27, 53, 2, 53, 65, 27]

def nb_occurence(x):
    score = 0
    for val in ma_liste:
        if x == val:
            score += 1
    return score

print(nb_occurence(53))

#-------------------------------------------
# Dessin d'un tapis avec une diagonale inversée
#-------------------------------------------

# Demande de la taille du tapis
print("Please enter the size you want your carpet to be : ")
size = int(input())

def draw_carpet(size):
    # Impression de la bordure supérieure
    print("+" + "-" * size + "+")

    # Contenu du tapis avec la diagonale
    for i in range(size - 1):
        line = "|"
        for j in range(size):
            if j == size - i - 1:  # Diagonale inversée
                line += " "
            else:
                line += "#"
        line += "|"
        print(line)

    # Impression de la bordure inférieure
    print("+" + "-" * size + "+")

# Test de la fonction
draw_carpet(size)

#-------------------------------------------
# Génération de listes
#-------------------------------------------

# Liste de 1 à 6
My_List = [i for i in range(1, 7)]
print(My_List)

# Liste des nombres impairs
My_List_impair = [x for x in My_List if x % 2 == 1]
print(My_List_impair)

#-------------------------------------------
# Création d'un mot à partir de deux variables
#-------------------------------------------

# !!! utilisez bien ma_var1 et ma_var2 pour vos opérations !!!!
# Créer un mot à partir des 2 premières lettres de ma_var1 et des 3 dernières lettres de ma_var2

ma_var1 = "Arcanine"
ma_var2 = "Arcanine"

# Extraire les 2 premières lettres de ma_var1 et les 3 dernières lettres de ma_var2
combinaison = ma_var1[:2] + ma_var2[-3:]

print("Mot créé :", combinaison)
print(combinaison)
