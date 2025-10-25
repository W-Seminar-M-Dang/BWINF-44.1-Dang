import math
import sys

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:

    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1

        # findet Parameter m; t für Gerade durch Strecke: f(x) = mx + t

        # Spezialfall: dx = 0 → linie senkrecht, Steigung als math.inf
        if p0.x == p1.x:
            self.steepness = math.inf
        else:
            self.steepness = (p0.y - p1.y) / (p0.x - p1.x) # calculating steepness of line with dy / dx

        # Lineare Funktion: f(y) = mx + t; y_achsenabschnitt auf engl. y-intercept

        if self.steepness == math.inf:
            # linie senkrecht → schneidet nie y_achse, y_intercept als x-koordinate wo die Strecke ist
            self.y_intercept = p0.x
        else:
            self.y_intercept = p0.y - (p0.x * self.steepness) # y1 = m * x1 + t -> t = y1 - (m * x1)

        # Findet Steigung der Normalen, normale immer senkrecht zur Tangente

        if self.steepness == math.inf:
            self.normal_steepness = 0.0 # senkrecht zur y-achse ist paralell zur x-achse
        elif self.steepness == 0.0:
            self.normal_steepness = math.inf # senkrecht zur x-achse ist paralell zur y-achse
        else:
            self.normal_steepness = -1/self.steepness

def intersection(line0_steepness, line0_y_intercept, line1_steepness, line1_y_intercept):
    """Gibt x und y-koordinate des Schnittpunktes zurück, falls keiner vorhanden: return None"""

    if  line0_steepness == line1_steepness: # linien paralell
        return None

    elif line0_steepness == math.inf: # line0 ist senkrecht -> Schnittpunkt bei x = line0_y_intercept (siehe Zeile 27)
        return Point(line0_y_intercept, (line1_steepness * line0_y_intercept) + line1_y_intercept) # line0_y_intercept in Funktion von line1 einsetzen

    elif line1_steepness == math.inf:
        return Point(line1_y_intercept, (line0_steepness * line1_y_intercept) + line0_y_intercept) # line1.y_intercept in Funktion von line0 einsetzen

    else:
        intersection_x =  (line0_y_intercept - line1_y_intercept) / (line1_steepness - line0_steepness) # m1*x + t1 = m2*x +t2 -> x = (t1 - t2) / (m2 - m1)
        intersection_y = line0_steepness * intersection_x + line0_y_intercept # x_koordinate in Funktion von line0 einsetzen
        return Point(intersection_x, intersection_y)

def distance(p0, p1):
    return math.sqrt((p0.x - p1.x)**2 + (p0.y - p1.y)**2) # Satz des Pythagoras

def intersection_perpendicular_line_point(line, point):
    """Berechnet Schnittpunkt vom Lot gefällt durch point auf line und line"""

    # y-Achsenabschnitt der Normalen berechnen um in intersection() enizusetzen
    if line.normal_steepness == math.inf:
        normal_y_intercept = point.x # (siehe Zeile 27)
    else:
        normal_y_intercept = point.y - (point.x * line.normal_steepness) # y = m * x + t -> t = y - (m * x)

    # in intersection() einsetzen
    return intersection(line.steepness, line.y_intercept, line.normal_steepness, normal_y_intercept)

def is_on_line(line, point):
    if line.steepness == math.inf:
        # punkt muss auf x_koordinate von line, also line.y_intercept sein, und zwischen höchsten und tiefsten Punkt von line sein
        return line.y_intercept == point.x and min(line.p0.y, line.p1.y) <= point.y <= max(line.p0.y, line.p1.y)
    else:
        # punkt muss auf Geraden sein und im von den Endpunkten abgegrenzten Bereich sein
        return point.y == point.x * line.steepness + line.y_intercept and min(line.p0.x, line.p1.x) <= point.x <= max(line.p0.x, line.p1.x)

def distance_line_perpendicular_line(line, point):
    """Distanz zischen point und Schnittpunkt vom Lot gefällt durch point auf line und line"""
    other_point = intersection_perpendicular_line_point(line, point) # Schnittpunkt Lot gefällt durch point auf Linie

    if other_point is None:
        return None
    elif not is_on_line(line, other_point):
        return None # distanz nicht gültig
    else:
        return distance(point, other_point)

def smallest_distance(line0, line1):
    """Gibt kleinste Distanz zwischen zwei Strecken zurück"""

    distances = []

    # alle Distanzen zwischen endpunkte der Linien
    for line0_endpoint in [line0.p1, line0.p0]:
        for line1_endpoint in [line1.p1, line1.p0]:
            distances.append(distance(line0_endpoint, line1_endpoint))

    # alle Distanzen zwischen Endpunkt und anderer Linie mit distance_line_perpendicular_line() berechnet
    for line0_endpoint in [line0.p1, line0.p0]:
        distance_line_point_perpendicular = distance_line_perpendicular_line(line1, line0_endpoint)
        if distance_line_point_perpendicular is not None:
            distances.append(distance_line_point_perpendicular)
    for line1_endpoint in [line1.p1, line1.p0]:
        distance_line_point_perpendicular = distance_line_perpendicular_line(line0, line1_endpoint)
        if distance_line_point_perpendicular is not None:
            distances.append(distance_line_point_perpendicular)

    return min(distances)

def lake_points_to_lakeshores(lake_points):
    """Gibt Liste von Strecken der Ufern als Line aus Eckpunkten des Sees zurück"""
    lake_lines = []
    for point_index in range(-1, len(lake_points) - 1): # startet bei -1 um vom letzten zum ersten Punkt eine Strecke zu bilden
        lake_lines.append(Line(lake_points[point_index], lake_points[point_index + 1])) # bildet Strecke mit nächstem Punkt
    return lake_lines

if __name__ == "__main__":

    # Dateipfad als Terminalargument
    with open(sys.argv[1], "r") as my_file:
        file = my_file.read().strip()

    # Datei wird erst in Linien aufgeteilt, darin werden alle durch Leerzeichen getrennte Werte in floats umgewandelt
    lines = [list(map(float,line.split())) for line in file.splitlines()]

    path_count = int(lines[0][0])
    lakes_count = int(lines[path_count + 1][0])

    lakeshores, paths = [], []

    # Erstellt alle Wege und fügt sie zu paths hinzu
    for path_coordinates in lines[1 : path_count + 1]:
        paths.append(Line(Point(*path_coordinates[0:2]), Point(*path_coordinates[2:4])))

    current_lake_start_index = path_count + 2 # stellt Index der Linie dar, wo die Anzahl der Eckpunkte beschrieben wird
    # + 2, weil die Anzahl der Wege und Seen jeweils eine Zeile benutzen

    for lake in range(lakes_count):

        current_lake_points = []
        current_lake_length = int(lines[current_lake_start_index][0])

        # alle zeilen mit Koordinaten des Sees
        for line in lines[current_lake_start_index + 1 : current_lake_start_index + 1 + current_lake_length]:
            # alle Eckpunkte des Sees als Objekt der Klasse Point() in current_lake_points einfügen
            current_lake_points.append(Point(*line))

        # alle Ufer des Sees als Strecken aus den Punkten zu lakeshores hinzu
        lakeshores.extend(lake_points_to_lakeshores(current_lake_points))

        current_lake_start_index += (current_lake_length + 1) # zum nächsten See gehen


shortest_leash_possible = math.inf

for path in paths:
    for lakeshore in lakeshores:
        shortest_leash_possible = min(shortest_leash_possible, smallest_distance(path, lakeshore))

print(shortest_leash_possible)