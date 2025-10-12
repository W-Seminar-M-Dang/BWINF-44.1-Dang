#from itertools import combinations

class Figur:
    def __init__(self, name, dauer : int, danach):
        self.name = name
        self.dauer = dauer
        self.danach = danach

    def __eq__(self, other):
        if not isinstance(other, Figur):
            return NotImplemented
        return (self.name == other.name and
                self.dauer == other.dauer and
                self.danach == other.danach)

datei_pfad = input()

with open(datei_pfad) as datei:
    choreographie = datei.read()

zeile = choreographie.split("\n")

max_takte = int(zeile[0])
figuren_anzahl = int(zeile[1])
startanordnung = "ABCDEFGHIJKLMNOP"
figuren = []

for figur in zeile[2:2 + figuren_anzahl]:
    figuren.append(Figur(figur.split(" ")[0], int(figur.split(" ")[1]), figur.split(" ")[2]))

def figur_asfueren(zu_tun, position):
    neue_position = ""
    for buchstabe in zu_tun.danach:
        neue_position += position[ord(buchstabe.lower()) - 97]
    return neue_position

def figurenabfolge_richtige_taktzahl(figuren_liste, ziel_summe):
    ergebnisse = []

    def suche(kombination, rest_summe):
        if rest_summe == 0:
            ergebnisse.append(kombination[:])
            return
        if rest_summe < 0:
            return
        for fi in figuren_liste:
            kombination.append(fi)
            suche(kombination, rest_summe - fi.dauer)
            kombination.pop()

    suche([], ziel_summe)
    return ergebnisse

#def gültige_choreographien_finden():



takt_aktuell = 0

kombis = figurenabfolge_richtige_taktzahl(figuren, 32)
print(f"{len(kombis)} Kombinationen gefunden:")
for k in kombis:  # nur erste 5 drucken
    print([f.name for f in k])


#/home/dang/Downloads/44.1/A2_ChoreoGraph/choreo01.txt