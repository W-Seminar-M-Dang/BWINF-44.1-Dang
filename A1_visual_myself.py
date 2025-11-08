import svgwrite
from A1 import Node, find_subtrees


class DrawTree:
    """Klasse für Baum, der drehfreudig ist und visualisiert werden soll"""

    def __init__(self, tree_file_path, depth, thinnest_node_value):
        import os
        self.tree_name = os.path.splitext(os.path.basename(tree_file_path))[0]  # extrahiert den Namen der Datei aus dem Pfad
        with open(tree_file_path, "r") as my_file:
            self.tree_str = my_file.read().strip()

        self.depth = depth
        self.thinnest_node_value = thinnest_node_value  # 1/Breite des schmalsten Knotens
        self.used_width_per_depth = [0 for line in range(self.depth + 1)]
        self.width = 100 * self.thinnest_node_value  # Dünnstes Blatt hat 100 px Platz (Der Kreis zur Darstellung des Knotens hat 25px Radius)
        self.height = (self.depth + 1) * 100  # Jeder ist 100px hoch, (Wurzel ist Ebene 0)
        self.drawing = svgwrite.Drawing(f"{self.tree_name}.svg", size=(self.width, self.height))

    @staticmethod
    def rectangle_center(insert, width):
        return insert[0] + 0.5 * width, insert[1] + 50

    def draw_line(self, start, end):
        self.drawing.add(self.drawing.line(start=start, end=end))

    def draw_node(self, rect_insert, rect_size):
        self.drawing.add(self.drawing.circle(
            center=DrawTree.rectangle_center(rect_insert, rect_size[0]), r="25", fill="black",))

    def draw_node_and_rect(self, insert, width):
        self.drawing.add(
            self.drawing.rect(insert=insert,size=(width, 100),fill="white",stroke="black",stroke_width=3,))
        self.draw_node(insert, (width, 100))

    def draw_leaf_and_node(self, insert, width, leaf_depth):
        self.drawing.add(
            self.drawing.rect(insert=insert,size=(width, (self.depth - leaf_depth + 1) * 100),fill="#f4e19c",stroke="black",stroke_width=3,))
        self.draw_node(insert, (width, (self.depth - leaf_depth + 1) * 100))

    def draw_child_nodes(self, node):
        """Durchsucht rekursiv den Teilbaum, fügt Kindknoten zu Blättern hinzu, wenn Kindknoten ein Blatt ist"""
        child_nodes = []
        child_nodes_subtrees = find_subtrees(node.subtree_str)
        for child_subtree in child_nodes_subtrees:
            child_nodes.append(Node(node.width * len(child_nodes_subtrees), node.depth + 1, child_subtree))
        for child_node in child_nodes:
            if child_node.subtree_str == "":
                self.draw_leaf_and_node((self.used_width_per_depth[child_node.depth], (child_node.depth * 100)), self.width / child_node.width , child_node.depth)
                self.used_width_per_depth[child_node.depth] += self.width / child_node.width
            else:
                self.draw_node_and_rect((self.used_width_per_depth[child_node.depth], (child_node.depth * 100)), self.width / child_node.width)
                self.used_width_per_depth[child_node.depth] += self.width / child_node.width
                self.draw_child_nodes(child_node)


    def save(self):
        self.drawing.save()


if __name__ == "__main__":
    tree_file = "baum.txt"

    # Parameter für den Baum
    max_depth = 2  # maximale Tiefe des Baums (anpassen falls nötig)
    thinnest_node_value = 4  # 1/Breite des schmalsten Knotens (z.B. 1 = ganzes Fenster, 2 = halb, ...)

    # Baumobjekt erstellen
    tree = DrawTree(tree_file, max_depth, thinnest_node_value)

    # Wurzelknoten erzeugen
    with open(tree_file, "r") as f:
        tree_str = f.read().strip()
    root_width = 1  # Wurzel ist "gesamte Breite" = 1/Breite
    root_depth = 0

    root = Node(root_width, root_depth, tree_str[1:-1])
    tree.draw_node_and_rect((0, 0), tree.width)


    # Rekursiv alle Kinder zeichnen
    tree.draw_child_nodes(root)

    # SVG speichern
    tree.save()
    print(f"Baum aus '{tree_file}' wurde als '{tree.tree_name}.svg' gespeichert.")
