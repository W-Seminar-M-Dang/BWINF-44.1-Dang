import sys

class Node:
    """Objekt für Knoten im Baum mit Breite 1/relative Breite, Teilbaum und Tiefe"""

    def __init__(self, width, depth, subtree_str):
        self.width = width
        self.depth = depth
        self.subtree_str = subtree_str

    # Ermöglicht Vergleich von Knoten, bei Prüfung der Symmetrie nützlich
    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return (self.width == other.width and
                self.depth == other.depth and
                self.subtree_str == other.subtree_str)

    def __hash__(self):
        return hash((self.width, self.depth, self.subtree_str))



def find_leaves(root_node):
    """Gibt Liste aller Blätter in Reihenfolge von links nach rechts zurück"""
    leaves = []

    def search(node):
        """Durchsucht rekursiv den Teilbaum, fügt Kindknoten zu Blättern hinzu, wenn Kindknoten ein Blatt ist"""

        child_nodes_subtrees = []
        bracket_counter = 0
        child_nodes_counter = 0
        child_node_start = 0

        # fügt alle Teilbäume der Kindknoten zu child_nodes_subtrees hinzu
        for bracket_index in range(len(node.subtree_str)):
            if node.subtree_str[bracket_index] == "(":
                bracket_counter += 1
            elif node.subtree_str[bracket_index] == ")":
                bracket_counter -= 1
                if bracket_counter == 0: # bedeutet, dass Teilbaum vollständig ist
                    child_nodes_counter += 1
                    child_nodes_subtrees.append(node.subtree_str[child_node_start + 1 : bracket_index])
                    child_node_start = bracket_index + 1

        for child_subtree in child_nodes_subtrees:
            if child_subtree == "":
                leaves.append(Node(node.width * child_nodes_counter, node.depth + 1, ""))
            else:
                search(Node(node.width * child_nodes_counter, node.depth + 1, child_subtree))

    search(root_node)
    return leaves


if __name__ == "__main__":

    # Dateipfad als Terminalargument
    with open(sys.argv[1], "r") as my_file:
        tree = my_file.read().strip()

    leaves1 = find_leaves(Node(1, 0, tree[1:-1]))

    # prüft, ob umgekehrter Baum derselbe ist
    if leaves1 == leaves1[::-1]:
        print("Der Baum ist Drehfreudig")
    else:
        print("Der Baum ist nicht Drehfreudig")