import svgwrite
from A1 import Node, find_subtrees


class DrawTree:
    """Klasse für Baum, der drehfreudig ist und visualisiert werden soll"""

    def __init__(self, tree_file_path, depth, thinnest_node_value):
        import os
        self.tree_name = os.path.splitext(os.path.basename(tree_file_path))[0]
        with open(tree_file_path, "r") as my_file:
            self.tree_str = my_file.read().strip()

        self.depth = depth
        self.thinnest_node_value = thinnest_node_value
        self.used_width_per_depth = [0 for _ in range(self.depth + 1)]
        self.width = 100 * self.thinnest_node_value
        self.height = (self.depth + 1) * 100
        # Breite normal, Höhe verdoppelt (oben + unten)
        self.drawing = svgwrite.Drawing(f"{self.tree_name}.svg", size=(self.width, self.height * 2))
        self.lines = []

    @staticmethod
    def rectangle_center(insert, width):
        # Mittelpunkt eines Rechtecks (x + 0.5 Breite, y + 50px)
        return insert[0] + 0.5 * width, insert[1] + 50

    def rotate_point(self, point):
        """Rotiert Punkt um 180° um die horizontale Mittellinie und in x-Richtung"""
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
        tree_root = Node(1, 0, tree_str[1:-1])
        tree.draw_node_and_rect((0, 0), self.width)
        tree.draw_child_nodes(tree_root, (self.width / 2, 50))

    def save(self):
        for line in self.lines:
            self.drawing.add(line)
        self.drawing.save()


if __name__ == "__main__":
    tree_file = "baum.txt"

    max_depth = 5
    thinnest_node_value_tree = 12

    tree = DrawTree(tree_file, max_depth, thinnest_node_value_tree)

    with open(tree_file, "r") as f:
        tree_str = f.read().strip()

    tree.draw()
    tree.save()
    print(f"Baum aus '{tree_file}' wurde als '{tree.tree_name}.svg' gespeichert.")
