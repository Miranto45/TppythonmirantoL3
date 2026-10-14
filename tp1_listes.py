#tp1:Les notes d'une classe
notes = [12, 8, 15, 17, 9, 11, 14, 6, 13, 16]
#1
print("1")
moyenne = sum(notes) / len(notes)
print(f"{len(notes)} notes, moyenne {moyenne:.2f}, min {min(notes)}, max {max(notes)}")

#2
print("\n2")
admis = [n for n in notes if n >= 10]
print(admis)                                  
print(len(notes) - len(admis), "ajournes")   

#3
print("\n3")
print(sorted(notes))                          
meilleures = sorted(notes, reverse=True)[:3]  
print(meilleures)                             

#4
print("\n4")
apres_deliberation = [min(n + 2, 10) if n < 10 else n for n in notes]
print(apres_deliberation)

#5
def histogramme(notes):
    tranches = {"0-4": (0, 4), "5-9": (5, 9), "10-14": (10, 14), "15-20": (15, 20)}
    for nom, (debut, fin) in tranches.items():
        nombre = len([n for n in notes if debut <= n <= fin])
        print(f"{nom} | {'*' * nombre}".rstrip())
print("\n5")
histogramme(notes)

# 6
def rang(notes, note):
    classement = sorted(notes, reverse=True)
    return classement.index(note) + 1
print("\n6")
print(rang(notes, 14))  

#7
print("\n7")
autres = [15, 6, 18]
fusion = []
for n in notes + autres:
    if n not in fusion:        
        fusion.append(n)
print(fusion)
