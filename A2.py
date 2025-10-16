#from itertools import combinations

class Figur:
    def __init__(self, name, dauer : int, danach):
        self.name = name
        self.dauer = dauer
        self.danach = danach
        self.strecke = sum([abs(index - (ord(char.lower()) - 97)) for index, char in enumerate(danach)])

    def __eq__(self, other):
        if not isinstance(other, Figur):
            return NotImplemented
        return (self.name == other.name and
                self.dauer == other.dauer and
                self.danach == other.danach)

    def __hash__(self):
        return hash((self.name, self.dauer, self.danach))

    def __str__(self):
        return self.name

def figur_ausfueren(zu_tun, position):
    neue_position = ""
    for buchstabe in zu_tun.danach:
        neue_position += position[ord(buchstabe.lower()) - 97]
    return neue_position

def gueltige_figurenkombinationen(figuren_liste, ziel_summe):
    kombinationen = []

    def suche(kombination, rest_summe):

        if rest_summe == 0:
            stellung = startanordnung
            for fig in kombination:
                stellung = figur_ausfueren(fig, stellung)
            if startanordnung == stellung:
                kombinationen.append(tuple(kombination))

        if rest_summe > 0:
            for fi in figuren_liste:
                kombination.append(fi)
                suche(kombination, rest_summe - fi.dauer)
                kombination.pop()

    suche([], ziel_summe)
    return kombinationen

def figurenabfolge_ausgeben(figurenabfolge):
    print("\n")
    for figuren_index in range(len(figurenabfolge)):
        print(f"{figuren_index}. {figurenabfolge[figuren_index]}")
    print("\n")

datei_pfad = input("Pfad zur Datei eingeben: ")

with open(datei_pfad) as datei:
    choreographie = datei.read()

zeile = choreographie.split("\n")

max_takte = int(zeile[0])
figuren_anzahl = int(zeile[1])
startanordnung = "ABCDEFGHIJKLMNOP"
figuren = []

for figur in zeile[2:2 + figuren_anzahl]:
    figuren.append(Figur(figur.split(" ")[0], int(figur.split(" ")[1]), figur.split(" ")[2]))


def max_unterschiedliche_figuren(alle_kombinationen):
    bester_wert = max(len(list(set(x))) for x in alle_kombinationen)
    for kombination in alle_kombinationen:
        if len(list(set(kombination))) == bester_wert:
            return kombination
    return None


def max_figuren(alle_kombinationen):
    bester_wert = max(len(x) for x in alle_kombinationen)
    for kombination in alle_kombinationen:
        if len(kombination) == bester_wert:
            return kombination
    return None

def min_figuren(alle_kombinationen):
    bester_wert = min(len(x) for x in alle_kombinationen)
    for kombination in alle_kombinationen:
        if len(kombination) == bester_wert:
            return kombination
    return None

def max_strecke(alle_kombinationen):
    bester_wert = max(sum(y.strecke for y in x) for x in alle_kombinationen)
    for kombination in alle_kombinationen:
        if sum(y.strecke for y in kombination) == bester_wert:
            return kombination
    return None

def min_strecke(alle_kombinationen):
    bester_wert = min(sum(y.strecke for y in x) for x in alle_kombinationen)
    for kombination in alle_kombinationen:
        if sum(y.strecke for y in kombination) == bester_wert:
            return kombination
    return None


strategien = [
    max_unterschiedliche_figuren,
    max_figuren,
    min_figuren,
    max_strecke,
    min_strecke]

figurenabfolgen = gueltige_figurenkombinationen(figuren, max_takte)

if len(figurenabfolgen) == 0:
    print("Es wurden 0 gültige Kombinationen gefunden.")
elif len(figurenabfolgen) == 1:
    print("Es wurden 1 gültige Kombinationen gefunden.")
    figurenabfolge_ausgeben(figurenabfolgen[0])
else:
    print(f"""
Es wurden {len(figurenabfolgen)} gültige Kombinationen gefunden.

Es wird die beste Kombination in den folgenden Kathegorien ausgegeben:""")

    print("(1) Möglichst viele unterschiedliche Figuren:")
    figurenabfolge_ausgeben(max_unterschiedliche_figuren(figurenabfolgen))

    print("(2) Möglichst viele Figuren:")
    figurenabfolge_ausgeben(max_figuren(figurenabfolgen))

    print("(3) Möglichst wenige Figuren:")
    figurenabfolge_ausgeben(min_figuren(figurenabfolgen))

    print("(4) Zurückgelegte Strecke aller Tanzenden insgesamt möglichst groß:")
    figurenabfolge_ausgeben(max_strecke(figurenabfolgen))

    print("(5) Zurückgelegte Strecke aller Tanzenden insgesamt möglichst klein:")
    figurenabfolge_ausgeben(min_strecke(figurenabfolgen))


#C:\Users\matth\Downloads\choreo01.txt
#https://stackoverflow.com/questions/1227121/compare-object-instances-for-equality-by-their-attributes
#https://stackoverflow.com/questions/6764909/how-to-remove-all-duplicate-items-from-a-list