baum_klammern = input("Auf Drehfreudigkeit zu prüfender Baum: ").strip()

#GÜLTIGKEITSTEST:

klammer_counter = 0

for klammer_position in range(len(baum_klammern)):
    if baum_klammern[klammer_position] == "(":
        klammer_counter +=1
    elif baum_klammern[klammer_position] == ")":
        klammer_counter -= 1
        if klammer_counter < 0 or (klammer_counter == 0 and klammer_position != len(baum_klammern) - 1):
            raise ValueError("Baum ist nicht gültig")

    else:
        raise ValueError("Baum beinhaltet unzulässige Zeichen")

if klammer_counter != 0 or baum_klammern[0] != "(" or baum_klammern[-1] != ")":
    raise ValueError("Baum nicht vollständig")



blaetter_liste = []


def ebene_tiefer(aktueller_knoten):

    offene_knoten.remove(aktueller_knoten)

    klammer_zaeler = 0
    nachbar_klammer_anzahl = 0
    teilbaum_start = 0
    knoten_tiefe = aktueller_knoten[1] + 1

    for klammer in range(len(aktueller_knoten[2])):
        if aktueller_knoten[2][klammer] == "(":
            klammer_zaeler += 1
        else:
            klammer_zaeler -= 1
            if klammer_zaeler == 0:
                unterbaum = aktueller_knoten[2][teilbaum_start + 1: klammer]
                nachbar_klammer_anzahl += 1
                offene_knoten.insert(nachbar_klammer_anzahl - 1, [0, knoten_tiefe, unterbaum])
                teilbaum_start = klammer + 1

    istlinks = True
    for knoten in offene_knoten[:]:
        if knoten[0] == 0:
            knoten[0] = nachbar_klammer_anzahl * aktueller_knoten[0]
        if knoten[2] == "" and istlinks:
            offene_knoten.remove(knoten)
            blaetter_liste.append(knoten)
        if knoten[2] != "" and istlinks:
            istlinks = False





offene_knoten = [[1, 0, baum_klammern[1:-1]]]


while len(offene_knoten) != 0:
    ebene_tiefer(offene_knoten[0])




istdrehfreudig = True

for i in range(len(blaetter_liste)):
    if blaetter_liste[i] == blaetter_liste[- i - 1]:
        pass
    else:
        istdrehfreudig = False

if istdrehfreudig:
    print("Dein Baum ist Drehfreudig :)")
else:
    print("Dein Baum ist leider nicht Drehfreudig")

print(blaetter_liste)

#https://stackoverflow.com/questions/21939652/insert-at-first-position-of-a-list-in-python

#((((())()())(()()((()))))((((()))())(()())(()(()))))