#tp2:
import math
from collections import namedtuple

villes = [
    ("Antananarivo", -18.88, 47.51),
    ("Toamasina", -18.15, 49.40),
    ("Mahajanga", -15.72, 46.32),
    ("Fianarantsoa", -21.45, 47.09),
]

# 1
print("1")
for n, lat, lon in villes:
    print(f"{n} : {lat}, {lon}")

#2
print("\n2")
print(max(villes, key=lambda v: v[1])[0])

#3
print("\n3")
lats, lons = [v[1] for v in villes], [v[2] for v in villes]
print(min(lats), max(lats), min(lons), max(lons))

#4
print("\n4")
d = math.dist(villes[0][1:], villes[1][1:])
print(f"Tana - Toamasina : {d:.2f} degres")

#5
print("\n5")
dist_dict = {
    (villes[i][0], villes[j][0]): math.dist(villes[i][1:], villes[j][1:])
    for i in range(len(villes)) for j in range(i + 1, len(villes))
}
for (v1, v2), val in dist_dict.items():
    print(f"{v1} - {v2} : {val:.2f}")
print("Nombre de paires :", len(dist_dict))

#6
print("\n6")
try:
    villes[0][1] = -19.00
except TypeError:
    print("Erreur : un tuple ne peut pas etre modifie.")
villes[0] = (villes[0][0], -18.91, villes[0][2])
print("Ville corrigée :", villes[0])

#7
print("\n7")
Ville = namedtuple("Ville", ["nom", "latitude", "longitude"])
v_nt = [Ville(*v) for v in villes]

def haversine(v1, v2):
    phi1, phi2 = math.radians(v1.latitude), math.radians(v2.latitude)
    dphi, dlam = phi2 - phi1, math.radians(v2.longitude - v1.longitude)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2)**2
    return 2 * 6371 * math.asin(math.sqrt(a))
print(f"{v_nt[0].nom} - {v_nt[1].nom} : {haversine(v_nt[0], v_nt[1]):.0f} km")
