import sys
import svgwrite
import os

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


def find_subtrees(subtree_str):
    """Zerlegt einen Teilbaumstring in Kind-Teilbäume"""
    child_nodes_subtrees = []
    bracket_counter = 0
    child_node_start = 0

    for bracket_index in range(len(subtree_str)):
        if subtree_str[bracket_index] == "(":
            if bracket_counter == 0:
                child_node_start = bracket_index
            bracket_counter += 1
        elif subtree_str[bracket_index] == ")":
            bracket_counter -= 1
            if bracket_counter == 0:
                child_nodes_subtrees.append(subtree_str[child_node_start + 1 : bracket_index])
    return child_nodes_subtrees

def find_leaves(root_node):
    """Gibt Liste aller Blätter in Reihenfolge von links nach rechts zurück"""
    leaves = []

    def search(node):
        """Durchsucht rekursiv den Teilbaum, fügt Kindknoten zu leaves hinzu, wenn Kindknoten ein Blatt ist"""
        child_nodes_subtrees = find_subtrees(node.subtree_str)

        for child_subtree in child_nodes_subtrees:
            if child_subtree == "":
                leaves.append(Node(node.width * len(child_nodes_subtrees), node.depth + 1, ""))
            else:
                search(Node(node.width * len(child_nodes_subtrees), node.depth + 1, child_subtree))

    search(root_node)
    return leaves


class DrawTree:
    """Klasse für Baum, der drehfreudig ist und visualisiert werden soll"""

    def __init__(self, tree_file_path, depth, thinnest_node_value):
        self.tree_name = os.path.splitext(os.path.basename(tree_file_path))[0]
        with open(tree_file_path, "r") as tree_file:
            self.tree_str = tree_file.read().strip()

        self.depth = depth
        self.thinnest_node_value = thinnest_node_value
        self.used_width_per_depth = [0 for _ in range(self.depth + 1)]
        self.width = 100 * self.thinnest_node_value
        self.height = (self.depth + 1) * 100
        # Breite normal, Höhe verdoppelt (oben + unten)
        self.svgpath =os.path.join(os.path.dirname(__file__), "Aufgabe1_Bilder", f"{self.tree_name}.svg")
        self.drawing = svgwrite.Drawing(self.svgpath, size=(self.width, self.height * 2))
        self.lines = []

    @staticmethod
    def rectangle_center(insert, width):
        # Mittelpunkt eines Rechtecks (x + 0.5 Breite, y + 50px)
        return insert[0] + 0.5 * width, insert[1] + 50

    def rotate_point(self, point):
        """Rotiert Punkt um 180 um die horizontale Mittellinie und in x-Richtung"""
        return self.width - point[0], 2 * self.height - point[1]

    def draw_line(self, start, end):
        # Linie oben
        self.lines.append(self.drawing.line(start=start, end=end, stroke="black", stroke_width=2, stroke_linecap="round"))
        # Linie unten (gedreht)
        self.lines.append(
            self.drawing.line(start=self.rotate_point(start), end=self.rotate_point(end), stroke="black", stroke_width=2, stroke_linecap="round"))

    def draw_node(self, rect_insert, rect_size):
        center = DrawTree.rectangle_center(rect_insert, rect_size[0])
        # Kreis oben
        self.drawing.add(self.drawing.circle(center=center, r=25, fill="black"))
        # Kreis unten (gedreht)
        self.drawing.add(self.drawing.circle(center=self.rotate_point(center), r=25, fill="black"))

    def draw_node_and_rect(self, insert, width):
        # Rechteck oben
        self.drawing.add(self.drawing.rect(insert=insert, size=(width, 100), fill="white", stroke="black", stroke_width=3))
        insert_rot = self.rotate_point((insert[0], insert[1] + 100))  # Rechteck korrekt unten positionieren
        self.drawing.add(
            self.drawing.rect(insert=(insert_rot[0] - width, insert_rot[1]), size=(width, 100), fill="white",
                              stroke="black", stroke_width=3))
        self.draw_node(insert, (width, 100))
        # Rechteck unten (gedreht)

    def draw_leaf_and_node(self, insert, width, leaf_depth):
        height_leaf = (self.depth - leaf_depth + 1) * 100
        # Rechteck oben
        self.drawing.add(self.drawing.rect(insert=insert, size=(width, height_leaf), fill="#f4e19c", stroke="black", stroke_width=3))
        # Rechteck unten (gedreht)
        insert_rot = self.rotate_point((insert[0], (insert[1]) + 100))
        self.drawing.add(
            self.drawing.rect(insert=(insert_rot[0] - width, insert_rot[1] - (self.depth - leaf_depth)*100), size=(width, height_leaf), fill="#f4e19c",
                              stroke="black", stroke_width=3))
        self.draw_node(insert, (width, height_leaf))

    def draw_child_nodes(self, node, node_center):
        """Durchsucht rekursiv den Teilbaum und fügt Kindknoten hinzu"""
        child_nodes = []
        child_nodes_subtrees = find_subtrees(node.subtree_str)
        for child_subtree in child_nodes_subtrees:
            child_nodes.append(Node(node.width * len(child_nodes_subtrees), node.depth + 1, child_subtree))

        for child_node in child_nodes:
            width_per_child = self.width / child_node.width
            insert = (self.used_width_per_depth[child_node.depth], child_node.depth * 100)
            child_node_center = DrawTree.rectangle_center(insert, width_per_child)

            if child_node.subtree_str == "":
                self.draw_leaf_and_node(insert, width_per_child, child_node.depth)
                for depth in range(child_node.depth, self.depth + 1):
                    self.used_width_per_depth[depth] += width_per_child
                self.draw_line(node_center, child_node_center)
            else:
                self.draw_node_and_rect(insert, width_per_child)
                self.used_width_per_depth[child_node.depth] += width_per_child
                self.draw_line(node_center, child_node_center)
                self.draw_child_nodes(child_node, child_node_center)

    def draw(self):
        tree_root = Node(1, 0, self.tree_str[1:-1])
        self.draw_node_and_rect((0, 0), self.width)
        self.draw_child_nodes(tree_root, (self.width / 2, 50))

    def save(self):
        for line in self.lines:
            self.drawing.add(line)
        self.drawing.save()



if __name__ == "__main__":

    #Dateipfad als Terminalargument
    with open(sys.argv[1], "r") as my_file:
        tree = my_file.read().strip()

    leaves1 = find_leaves(Node(1, 0, tree[1:-1]))

    # prüft, ob umgekehrter Baum derselbe ist
    if leaves1 == leaves1[::-1]:
        print(True)
        print("Der Baum ist Drehfreudig")
        tree_svg = DrawTree(sys.argv[1], max([leaf.depth for leaf in leaves1]), max([leaf.width for leaf in leaves1]))
        tree_svg.draw()
        tree_svg.save()
        print(tree_svg.svgpath)
    else:
        print(False)
        print("Der Baum ist nicht Drehfreudig")