#tp5Projet de synthese:carnet de notes
import json
from datetime import datetime
from functools import wraps

# Structure de donnees imposee:matricule-dictionnaire de l'etudiant
etudiants = {
    "L3-001": {
        "nom": "Rakoto",
        "prenom": "Soa",
        "notes": {"Python": [15, 14], "Reseaux": [12]},
    },
    "L3-002": {
        "nom": "Rabe",
        "prenom": "Andry",
        "notes": {"Python": [9, 13], "Reseaux": [11, 10]},
    },
}

# Liste globale:(date et heure, nom de la fonction, arguments)
historique = []

#decorateur
def journaliser(fonction):
    """Ajoute un tuple dans historique a chaque appel."""
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        resultat = fonction(*args, **kwargs)     
        maintenant = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        historique.append((maintenant, fonction.__name__, args))
        return resultat
    return enveloppe
def note_valide(fonction):
    """Refuse toute note qui n'est pas comprise entre 0 et 20."""
    @wraps(fonction)
    def enveloppe(matricule, matiere, note, *args, **kwargs):
        if not 0 <= note <= 20:
            raise ValueError(f"Note invalide ({note}) : elle doit être comprise entre 0 et 20")
        return fonction(matricule, matiere, note, *args, **kwargs)
    return enveloppe
def etudiant_existe(fonction):
    """Vérifie que le matricule (premier argument) existe."""
    @wraps(fonction)
    def enveloppe(matricule, *args, **kwargs):
        if matricule not in etudiants:
            raise ValueError(f"Matricule inconnu : {matricule}")
        return fonction(matricule, *args, **kwargs)
    return enveloppe


#fonction

@journaliser
def ajouter_etudiant(matricule, nom, prenom):
    """Crée un étudiant. Refuse un matricule deja existant."""
    if matricule in etudiants:
        raise ValueError(f"Le matricule {matricule} existe deja")
    etudiants[matricule] = {"nom": nom, "prenom": prenom, "notes": {}}
@etudiant_existe
@note_valide
@journaliser
def ajouter_note(matricule, matiere, note):
    """Ajoute une note, cree la matiere si besoin."""
    etudiants[matricule]["notes"].setdefault(matiere, []).append(note)
@etudiant_existe
def moyenne_matiere(matricule, matiere):
    """Moyenne d'un étudiant dans une matiere (0 si aucune note)."""
    notes = etudiants[matricule]["notes"].get(matiere, [])
    if not notes:
        return 0.0
    return sum(notes) / len(notes)
@etudiant_existe
def moyenne_generale(matricule):
    """Moyenne des moyennes de matieres."""
    matieres = etudiants[matricule]["notes"]
    moyennes = [moyenne_matiere(matricule, m) for m in matieres]
    if not moyennes:
        return 0.0
    return sum(moyennes) / len(moyennes)
def classement():
    """Liste de tuples (nom complet, moyenne), triee par moyenne decroissante."""
    liste = [
        (f"{e['prenom']} {e['nom']}", moyenne_generale(matricule))
        for matricule, e in etudiants.items()
    ]
    return sorted(liste, key=lambda t: t[1], reverse=True)


def majors():
    """Dictionnaire matiere -> nom du meilleur etudiant."""
    resultat = {}
    meilleures_moyennes = {}
    for matricule, e in etudiants.items():
        for matiere in e["notes"]:
            moyenne = moyenne_matiere(matricule, matiere)
            if matiere not in meilleures_moyennes or moyenne > meilleures_moyennes[matiere]:
                meilleures_moyennes[matiere] = moyenne
                resultat[matiere] = f"{e['prenom']} {e['nom']}"
    return resultat
def sauvegarder(fichier):
    """Enregistre le carnet en JSON."""
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(etudiants, f, ensure_ascii=False, indent=2)
def charger(fichier):
    """Relit le carnet depuis un fichier JSON."""
    with open(fichier, "r", encoding="utf-8") as f:
        donnees = json.load(f)
    etudiants.clear()
    etudiants.update(donnees)

#Affichage
@etudiant_existe
def afficher_bulletin(matricule):
    e = etudiants[matricule]
    print(f"Bulletin de {e['prenom']} {e['nom']} ({matricule})")
    for matiere, notes in e["notes"].items():
        print(f"  {matiere} : {notes} -> moyenne {moyenne_matiere(matricule, matiere):.2f}")
    print(f"  Moyenne generale : {moyenne_generale(matricule):.2f}")
def afficher_classement():
    for rang, (nom, moyenne) in enumerate(classement(), start=1):
        print(f"{rang}. {nom} {moyenne:.2f}")
def afficher_majors():
    for matiere, nom in majors().items():
        print(f"{matiere} : {nom}")
def afficher_historique():
    if not historique:
        print("Historique vide")
    for date, nom_fonction, arguments in historique:
        print(f"{date} | {nom_fonction} | {arguments}")


#MENU

def menu():
    while True:
        print("\nCARNET DE NOTES:")
        print("1. Ajouter un etudiant")
        print("2. Ajouter une note")
        print("3. Afficher un bulletin")
        print("4. Afficher le classement")
        print("5. Afficher les majors")
        print("6. Afficher l'historique")
        print("7. Sauvegarder")
        print("8. Quitter")
        choix = input("Votre choix : ").strip()
        try:
            if choix == "1":
                matricule = input("Matricule : ")
                nom = input("Nom : ")
                prenom = input("Prenom : ")
                ajouter_etudiant(matricule, nom, prenom)
                print("Étudiant ajoute.")
            elif choix == "2":
                matricule = input("Matricule : ")
                matiere = input("Matiere : ")
                note = float(input("Note : "))
                ajouter_note(matricule, matiere, note)
                print("Note ajoutee.")
            elif choix == "3":
                afficher_bulletin(input("Matricule : "))
            elif choix == "4":
                afficher_classement()
            elif choix == "5":
                afficher_majors()
            elif choix == "6":
                afficher_historique()
            elif choix == "7":
                sauvegarder("carnet.json")
                print("Carnet sauvegarde dans carnet.json")
            elif choix == "8":
                print("Au revoir !")
                break
            else:
                print("Choix invalide.")
        except ValueError as erreur:
            print("Erreur :", erreur)
if __name__ == "__main__":
    menu()
