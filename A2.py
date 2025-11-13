import sys


class Routine:
    """Klasse für Bewegungen in einer Choreografie mit Name, Dauer und Position nach der Ausführung beginnend mit ABCDEFGHIKLMNOP"""
    
    def __init__(self, name, duration : int, pos_after):
        self.name = name
        self.duration = duration
        self.pos_after = pos_after
        
        # Summe von allen Tänzern zurückgelegten Strecke:
        # Differenz zwischen aktueller Position (Index) und ursprünglicher Startposition (ord(char.lower()) - 97)
        # ord(char.lower()) - 97 gibt Position im Alphabet zurück: a = 0, b = 1, c = 2 ...
        self.sum_dancer_overall_distance = sum([abs(index - (ord(char.lower()) - 97)) for index, char in enumerate(pos_after)])

    def __eq__(self, other): # damit zwei Figuren mit == verglichen werden können
        if not isinstance(other, Routine):
            return NotImplemented
        return (self.name == other.name and
                self.duration == other.duration and
                self.pos_after == other.pos_after)

    def __hash__(self): # damit man Routine in ein Set hinzufügen darf
        return hash((self.name, self.duration, self.pos_after))

    
starting_position = "ABCDEFGHIJKLMNOP"
    
    
def execute_routine(routine, initial_pos):
    """Gibt Position nach Ausführung der Routine ab initial_pos zurück"""
    new_pos = ""
    for dancer in routine.pos_after:
        new_pos += initial_pos[ord(dancer.lower()) - 97] # new_pos ist ein String; jeder Tänzer (Buchstabe) wird zum neuen Platz in der richtigen Reihenfolge dazu konkateniert (Fachbegriffe sind immer toll :))
    return new_pos


def find_choreos(routines, choreo_length):
    seen = set()
    results = []
    single_choreo = True

    def search(current_position, rest_sum, combination):
        if rest_sum < 0:
            return

        if rest_sum == 0:
            if current_position == starting_position:
                results.append(list(combination))
            return

        state = (current_position, rest_sum, len(combination), frozenset(combination))
        if state in seen:
            single_choreo = False
            return
        seen.add(state)

        for routine in routines:
            combination.append(routine)
            new_position = execute_routine(routine, current_position)
            search(new_position, rest_sum - routine.duration, combination)
            combination.pop()

    search(starting_position, choreo_length, [])
    return results, single_choreo


def get_routines(routines_strings):
    """Gibt Liste von Routinen als Objekt der Klasse Routine zurück, aus Strings der Routinen aus geöffneter Datei"""

    routines = []
    for routine_str in routines_strings:
        routine_name = routine_str.split(" ")[0]
        routine_duration = int(routine_str.split(" ")[1])
        routine_pos_after = routine_str.split(" ")[2]
        routines.append(Routine(routine_name, routine_duration, routine_pos_after))

    return routines

# Sonderfälle:

def max_different_routines(choreos):
    """Sucht nach Choreos mit den meisten unterschiedlichen Routinen und gibt eine zurück"""

    best_value = max(len(list(set(choreo))) for choreo in choreos) # list(set()), um doppelte Routinen zu entfernen,
    print(best_value)
    for choreo in choreos:
        if len(list(set(choreo))) == best_value:
            return choreo
    return None

def max_routines(choreos):
    """Sucht nach Choreos mit den meisten Routinen und gibt eine zurück"""

    best_value = max(len(choreo) for choreo in choreos)
    print(best_value)
    for choreo in choreos:
        if len(choreo) == best_value:
            return choreo
    return None

def min_routines(choreos):
    """Sucht nach Choreo mit den wenigsten Routinen und gibt eine zurück"""

    best_value = min(len(choreo) for choreo in choreos)
    print(best_value)
    for choreo in choreos:
        if len(choreo) == best_value:
            return choreo
    return None

def max_distance(choreos):
    """Sucht nach Choreo mit der größten von den Tänzern zurückgelegten Strecke und gibt eine zurück"""

    # Maximum aller Summen der von Tänzern zurückgelegten Strecken in jeder gültigen Choreo
    best_value = max(sum(routine.sum_dancer_overall_distance for routine in choreo) for choreo in choreos)
    print(best_value)

    for choreo in choreos:
        if sum(routine.sum_dancer_overall_distance for routine in choreo) == best_value:
            return choreo
    return None

def min_distance(choreos):
    """Sucht nach Choreo mit der kleinsten von den Tänzern zurückgelegten Strecke und gibt eine zurück"""

    # Minimum aller Summen der von Tänzern zurückgelegten Strecken in jeder gültigen Choreo
    best_value = min(sum(routine.sum_dancer_overall_distance for routine in choreo) for choreo in choreos)
    print(best_value)

    for choreo in choreos:
        if sum(routine.sum_dancer_overall_distance for routine in choreo) == best_value:
            return choreo
    return None


if __name__ == "__main__":

    # Dateipfad als Terminalargument
    with open(sys.argv[1], "r") as my_file:
        piece_of_music = my_file.read().strip()

    lines = piece_of_music.splitlines()
    piece_length = int(lines[0])
    routines_number = int(lines[1])
    routines_piece_of_music = get_routines(lines[2:2 + routines_number])

    valid_choreos, only_one_choreo = find_choreos(routines_piece_of_music, piece_length)


    def print_choreo(choreo):
        """gibt Namen aller Routinen/Figuren in der Choreo aus"""

        for routine_index in range(len(choreo)):
            print(f"{routine_index}. {choreo[routine_index].name}")
        print("\n")

    if len(valid_choreos) == 0:
        print("Keine gültigen Choreographien gefunden")
    elif len(valid_choreos) == 1 and only_one_choreo == True:
        print("Es wurde 1 gültige Choreographie gefunden:")
        print_choreo(valid_choreos[0])
    else:
        print("Choreo mit möglichst viele unterschiedliche Figuren:\n")
        print_choreo(max_different_routines(valid_choreos))

        print("Choreo mit möglichst viele Figuren:\n")
        print_choreo(max_routines(valid_choreos))

        print("Choreo mit möglichst wenige Figuren:\n")
        print_choreo(min_routines(valid_choreos))

        print("Choreo mit von allen Tanzenden zurückgelegte Distanz möglichst groß:\n")
        print_choreo(max_distance(valid_choreos))

        print("Choreo mit von allen Tanzenden zurückgelegte Distanz möglichst klein:\n")
        print_choreo(min_distance(valid_choreos))