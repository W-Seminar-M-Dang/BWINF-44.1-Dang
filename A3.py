class Strecke:

    def __init__(self, start_x, start_y, ende_x, ende_y):
        self.startpunkt = (start_x, start_y)
        self.endpunkt = (ende_x, ende_y)

        if start_x == ende_x:
            self.steigung = float("inf")
        else:
            self.steigung = (start_y - ende_y) / (start_x - ende_x)

        if self.steigung == float("inf"):
            self.y_achsenabschnitt = start_x
        else:
            self.y_achsenabschnitt = start_y - (start_x * self.steigung)

    def __str__(self):
        return f"Strecke von {self.startpunkt} bis {self.endpunkt}"

    def normalensteigung(self):
        if self.steigung == float("inf"):
            return 0
        elif self.steigung == 0:
            return float("inf")
        else:
            return -1 / self.steigung

def see_eckpunkte_strecken(eckpunkte):
    ufer_strecken = []
    for eckpunkt_index in range(-1, len(eckpunkte) - 1):
        ufer_strecken.append(Strecke(*eckpunkte[eckpunkt_index], *eckpunkte[eckpunkt_index + 1]))
    return ufer_strecken


def schnittpunkt(m1, t1, m2, t2):
    if m1 == m2:
        return None
    elif m1 == float("inf"):
        return t1, (m2 * t1) + t2
    elif m2 == float("inf"):
        return t2, (m1 * t2) + t1
    else:
        schnittpunkt_x =  (t2 - t1)/(m1 - m2)
        schnittpunkt_y = m1 * schnittpunkt_x + t1
        return schnittpunkt_x, schnittpunkt_y

def abstand_berechnen(p1_x, p1_y, p2_x, p2_y):
    return ((p1_x - p2_x)**2 + (p1_y - p2_y)**2) ** 0.5

def schnittpunkt_lot_durch_punkt_strecke(strecke, punkt):
    if strecke.normalensteigung() == float("inf"):
        y_achsenabschnitt_lot = punkt[0]
    else:
        y_achsenabschnitt_lot = punkt[1] - (punkt[0] * strecke.normalensteigung())
    schnittpunkt_strecke_lot = schnittpunkt(strecke.normalensteigung(), y_achsenabschnitt_lot, strecke.steigung, strecke.y_achsenabschnitt)
    return schnittpunkt_strecke_lot

def ist_auf_strecke(strecke, punkt):
    if strecke.steigung == float("inf"):
        return punkt[0] == strecke.y_achsenabschnitt and (min(strecke.endpunkt[1], strecke.startpunkt[1]) <= punkt[1] <= max(strecke.endpunkt[1], strecke.startpunkt[1]))
    else:
        return min(strecke.endpunkt[0], strecke.startpunkt[0]) <= punkt[0] <= max(strecke.endpunkt[0], strecke.startpunkt[0])

def distanz_strecke_lot_berechnen(strecke, punkt):
    schnittpunkt_strecke_lot = schnittpunkt_lot_durch_punkt_strecke(strecke, punkt)
    if schnittpunkt_strecke_lot is not None and ist_auf_strecke(strecke, schnittpunkt_strecke_lot):
        return abstand_berechnen(*punkt, *schnittpunkt_strecke_lot)
    else:
        return None

def kleinste_distanz(strecke1, strecke2):
    distanzen = []
    for p1 in [strecke1.startpunkt, strecke1.endpunkt]:
        for p2 in [strecke2.startpunkt, strecke2.endpunkt]:
            distanzen.append(abstand_berechnen(p1[0], p1[1], p2[0], p2[1]))

    for p in [strecke1.startpunkt, strecke1.endpunkt]:
        distanz = distanz_strecke_lot_berechnen(strecke2, p)
        if distanz is not None:
            distanzen.append(distanz)
    for p in [strecke2.startpunkt, strecke2.endpunkt]:
        distanz = distanz_strecke_lot_berechnen(strecke1, p)
        if distanz is not None:
            distanzen.append(distanz)
    return min(distanzen)

datei_pfad = input("Pfad zur Datei eingeben: ")

with open(datei_pfad) as datei:
    karte = datei.read()

zeilen = ([list(map(int,linie)) for linie in [zeile.split() for zeile in karte.splitlines()]])
anzahl_wege = zeilen[0][0]
anzahl_seen = zeilen[anzahl_wege + 1][0]

wege, ufer  = [], []

for weg_koordinaten in zeilen[1 : anzahl_wege + 1]:
    wege.append(Strecke(*weg_koordinaten))

aktueller_see_anfang = anzahl_wege + 2

for see in range(anzahl_seen):
    aktueller_see_eckpunkte = []
    aktueller_see_laenge = zeilen[aktueller_see_anfang][0]
    for linie in zeilen[aktueller_see_anfang + 1 : aktueller_see_anfang + aktueller_see_laenge + 1]:
        aktueller_see_eckpunkte.append(tuple(linie))
    ufer.extend(see_eckpunkte_strecken(aktueller_see_eckpunkte))
    aktueller_see_anfang = aktueller_see_anfang + aktueller_see_laenge + 1


kleinste_leine = float("inf")
for weg in wege:
    for strand in ufer:
        kleinste_leine = min(kleinste_leine, kleinste_distanz(weg, strand))

print(kleinste_leine)


#falls Winkel größer als 90 ist, schneidet sich die Funktionenschar der Normalen, also der Lote nicht mit der anderen Gerade vor dem Schnittpunkt, weshalb die Strecke direkt zwischen den Punkten am nächsten von de
# wie v- figur also immer kleiner das Lot wenn man näher zum imaginären Schnittpunkt kommt
#C:\Users\matth\Downloads\hund01.txt
#https://stackoverflow.com/questions/3371269/call-int-function-on-every-list-element
#https://stackoverflow.com/questions/7781260/how-to-represent-an-infinite-number-in-python