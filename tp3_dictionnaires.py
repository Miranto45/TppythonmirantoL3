#tp3:
import json
from collections import Counter

stock = {
    "riz": {"prix": 3200, "quantite": 50},
    "huile": {"prix": 9500, "quantite": 12},
    "sucre": {"prix": 4000, "quantite": 30},
    "savon": {"prix": 1500, "quantite": 0},
}

#1
print("1")
for produit in stock:
    infos = stock[produit]
    prix = infos["prix"]
    quantite = infos["quantite"]
    print(produit, ":", prix, "Ar, quantite", quantite)

#2
print("\n2")
valeur_totale = 0
for produit in stock:
    prix = stock[produit]["prix"]
    quantite = stock[produit]["quantite"]
    valeur_totale = valeur_totale + (prix * quantite)
print("Valeur totale du stock :", valeur_totale, "Ar")

#3
print("\n3")
ruptures = []
for produit in stock:
    quantite = stock[produit]["quantite"]
    if quantite == 0:
        ruptures.append(produit)
print(ruptures)

#4
def vendre(stock_actuel, produit, quantite_demandee):
    if produit not in stock_actuel:
        return (False, "Produit inconnu")
    
    stock_dispo = stock_actuel[produit]["quantite"]
    if stock_dispo < quantite_demandee:
        return (False, "Stock insuffisant")
    
    stock_actuel[produit]["quantite"] = stock_dispo - quantite_demandee
    return (True, "Vente reussie")
print("\n4")
print(vendre(stock, "riz", 5))
print(vendre(stock, "cafe", 1))
print(vendre(stock, "huile", 100))

#5
def ajouter_produit(stock_actuel, nom, prix, quantite):
    if nom in stock_actuel:
        return (False, "Le produit existe deja")
    
    stock_actuel[nom] = {"prix": prix, "quantite": quantite}
    return (True, "Produit ajoute")

print("\n5")
print(ajouter_produit(stock, "farine", 2800, 20))
print(ajouter_produit(stock, "riz", 3200, 10))

#6
print("\n6")
prix_hausse = {}
for produit in stock:
    ancien_prix = stock[produit]["prix"]
    nouveau_prix = round(ancien_prix * 1.10)
    prix_hausse[produit] = nouveau_prix
print(prix_hausse)

#7
print("\n7")
ventes = ["riz", "sucre", "riz", "huile", "riz"]
compteur = {}
for produit in ventes:
    if produit in compteur:
        compteur[produit] = compteur[produit] + 1
    else:
        compteur[produit] = 1
print(compteur)
print(dict(Counter(ventes)))

#8
print("\n8")
fichier = open("stock.json", "w", encoding="utf-8")
json.dump(stock, fichier, ensure_ascii=False, indent=2)
fichier.close()
fichier_lecture = open("stock.json", "r", encoding="utf-8")
stock_recharge = json.load(fichier_lecture)
fichier_lecture.close()
print("Les dictionnaires sont egaux :", stock == stock_recharge)