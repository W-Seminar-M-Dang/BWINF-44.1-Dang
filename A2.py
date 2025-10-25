import sys

class Routine:
    """Class for moves in choreography with name, duration and position after the move starting with ABCDEFGHIKLMNOP"""
    
    def __init__(self, name, duration : int, pos_after):
        self.name = name
        self.duration = duration
        self.pos_after = pos_after
        
        # sum of distance moved by every dancer:
        # difference between current position (index) and initial starting position (ord(char.lower()) - 97)
        # ord(char.lower()) - 97 returns position in alphabet: a = 0, b = 1, c = 2 ...
        self.sum_dancer_overall_distance = sum([abs(index - (ord(char.lower()) - 97)) for index, char in enumerate(pos_after)])

    def __eq__(self, other):
        if not isinstance(other, Routine):
            return NotImplemented
        return (self.name == other.name and
                self.duration == other.duration and
                self.pos_after == other.pos_after)

    def __hash__(self):
        return hash((self.name, self.duration, self.pos_after))

    
starting_position = "ABCDEFGHIJKLMNOP"
    
    
def execute_routine(routine, initial_pos):
    """Returns position after execution of routine from initial_pos"""
    new_pos = ""
    for dancer in routine.pos_after:
        new_pos += initial_pos[ord(dancer.lower()) - 97] # new_pos is a String
    return new_pos

def find_choreos(routines, choreo_length):
    """Finds all combinations of routines where at the end the duration correct and the end position is like at the start"""
    choreos = []

    def search(combination, rest_sum):

        # Tests if chorero with length of the music piece that retruns to starting position after execution
        if rest_sum == 0:
            current_position = starting_position
            for routine in combination:
                current_position = execute_routine(routine, current_position)
            if starting_position == current_position:
                choreos.append(tuple(combination))

        if rest_sum > 0:
            for routine in routines:
                new_combination = combination[:]
                new_combination.append(routine)
                search(new_combination, rest_sum - routine.duration)

    search([], choreo_length)
    return choreos

def get_routines(routines_strings):
    """Returns list of routines as Object of Routine, with Strings of routines from opened document as parameter"""

    routines = []
    for routine_str in routines_strings:
        routine_name = routine_str.split(" ")[0]
        routine_duration = int(routine_str.split(" ")[1])
        routine_pos_after = routine_str.split(" ")[2]
        routines.append(Routine(routine_name, routine_duration, routine_pos_after))

    return routines

# Special Cases:
# return first item of the list that meets condition, if more than 1 meet the same condition

def max_different_routines(choreos):
    """Searches for choreos with most different routines and returns one"""

    best_value = max(len(list(set(choreo))) for choreo in choreos) # list(set()) to remove duplicate routines,
    for choreo in choreos:
        if len(list(set(choreo))) == best_value:
            return choreo
    return None

def max_routines(choreos):
    """Searches for choreos with most routines and returns one"""

    best_value = max(len(choreo) for choreo in choreos)
    for choreo in choreos:
        if len(choreo) == best_value:
            return choreo
    return None

def min_routines(choreos):
    """Searches for choreo with the least different routines and returns one"""

    best_value = min(len(choreo) for choreo in choreos)
    for choreo in choreos:
        if len(choreo) == best_value:
            return choreo
    return None

def max_distance(choreos):
    """Searches for choreo with the most distance traveled by the performers and returns one"""

    # maximum of all sums for all distances traveled by dancers for every valid combination of routines
    best_value = max(sum(routine.sum_dancer_overall_distance for routine in choreo) for choreo in choreos)

    for choreo in choreos:
        if sum(routine.sum_dancer_overall_distance for routine in choreo) == best_value:
            return choreo
    return None

def min_distance(choreos):
    """Searches for choreo with the least distance traveled by the performers and returns one"""

    # minimum of all sums for all distances traveled by dancers for every valid combination of routines
    best_value = min(sum(routine.sum_dancer_overall_distance for routine in choreo) for choreo in choreos)

    for choreo in choreos:
        if sum(routine.sum_dancer_overall_distance for routine in choreo) == best_value:
            return choreo
    return None


if __name__ == "__main__":

    #File path as terminal argument
    with open(sys.argv[1], "r") as my_file:
        piece_of_music = my_file.read().strip()

    lines = piece_of_music.splitlines()
    piece_length = int(lines[0])
    routines_number = int(lines[1])
    routines_piece_of_music = get_routines(lines[2:2 + routines_number])

    valid_choreos = find_choreos(routines_piece_of_music, piece_length)


    def print_choreo(choreo):
        """prints name of all moves in choreo"""

        for routine_index in range(len(choreo)):
            print(f"{routine_index}. {choreo[routine_index].name}")
        print("\n")

    if len(valid_choreos) == 0:
        print("Keine gültigen Choreographien gefunden")
    elif len(valid_choreos) == 1:
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