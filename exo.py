"""
 Plusieurs hypothèses sont émises :
Les ages sont calculés selon :
- le cycle lunaire de 28 jours
- la saison d'une année nilotique (3 saisons de 4 mois par an soit 120 jours + 5 jours de fêtes)
- l'année solaire de 365 jours


Calculer l'age des patriaches en année solaire à la naissance de leur enfant et l'age de leur mort avec ces 3 hypothèses ?
Écrire une belle phrase pour afficher les résultats ainsi qu'un alignement des valeurs afin que tous les mots soient alignés :
format demandé :
Adam       est père à 230.00 ans et meurt à 930.00 ans

Indiqué qu'Énoch n'est pas mort mais transféré par Dieu.

En moyenne, à quel age les patriarches ont eu leur premier enfant / sont-ils morts ?

Combien de temps s'est-il passé entre la naissance d'Adam et la mort de Noé selon les 3 hypothèses ?

Quels sont ceux qui ont vu la mort de leur enfant ?

Quels descendant ont-ils connu ? (Étaient-ils toujours vivant à la naissance de ...)

Données fournies :
------------------
Adam       - 230 / 930
Seth       - 205 / 912
Enos       - 190 / 905
Caïnan     - 170 / 910
Malalehel  - 165 / 895
Jared      - 162 / 962
Énoch      - 165 / 365
Mathusalem - 167 / 969
Lamech     - 188 / 753
Noé        - 500 / 950
"""

def age(dico):
    for k, v in dico.items():
        if "Enos" in k:
            print(k , " est père à " ,  abs(v[0]) , "ans. Puis transféré à Dieu", abs(v[1]) )
        else :
            print(k , " est père à " ,  abs(v[0]) , "ans et meurt à ", abs(v[1]) , "ans")

def moyenne(dico):
    score_enfant = 0
    score_mort = 0
    for v in dico.values():
        score_enfant += v[0]
        score_mort += v[1]
    return score_enfant // len(dico), score_mort // len(dico)

dico = {
    "Adam" : [-230,930],
    "Seth" : [-210,430],
    "Enos" : [-190,90],
    "Caïnan" : [-170,90],
    "Malalehel" : [-165,895],
    "Jared" : [-162,962],
    "Mathusalem" : [-167,969],
    "Lamech" : [-188,753],
    "Noé" : [-500,950]
}
age(dico)
print("")
print("La moyenne : " , moyenne(dico))
print("")