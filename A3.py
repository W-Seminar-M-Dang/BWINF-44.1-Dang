class Strecke:

    def __init__(self, start_x, start_y, ende_x, ende_y):
        self.start_x = start_x
        self.start_y = start_y
        self.ende_x = ende_x
        self.ende_y = ende_y

        if self.start_x == self.ende_x:
            self.steigung = None
        else:
            self.steigung = (self.start_y - self.ende_y) / (self.start_x - self.ende_x)

        if self.steigung is None:
            self.y_achsenabschnitt = None
        else:
            self.y_achsenabschnitt = self.start_y - (self.start_x * self.steigung)


def ufer_als_strecke(eckpunkte):
    ufer_strecken = []
    for eckpunkt_index in range(-1, len(eckpunkte) - 1):
        ufer_strecken.append(Strecke(*eckpunkte[eckpunkt_index], *eckpunkte[eckpunkt_index + 1]))
    return ufer_strecken


#def schnittpunkt():
#TODO: 2 Schnittpunkte zwischen zwei Geraden berechnen


#TODO: 3 Funktion: Gleichung (Steigung) der Normalen einer Funktion zurückgeben

#TODO: 4 Funktion: nimmt normale ein und andere Streckenkoordinaten, berechnung der minimalen Strecke

datei_pfad = input("Pfad zur Datei eingeben: ")

with open(datei_pfad) as datei:
    karte = datei.read()

zeilen = karte.split("\n")
anzahl_wege = int(zeilen[0])
anzahl_seen = int(zeilen[anzahl_wege + 1])

wege, ufer  = [], []

for weg_koordinaten in zeilen[1 : anzahl_wege]:
    wege.append(Strecke(*map(int, weg_koordinaten.split())))

#TODO: 1 ufer_als_strecke() implementieren

# for punkt in eckpunkte:
#     self.eckpunkte.append((int(punkt.split(" ")[0]), int(punkt.split(" ")[1])))

#https://stackoverflow.com/questions/3371269/call-int-function-on-every-list-element