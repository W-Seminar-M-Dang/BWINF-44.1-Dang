import svgwrite
from A1 import Node, find_subtrees


class DrawTree:
    """Zeichnet Bäume aus Klammernotation als SVG."""

    def __init__(self, tree_file_path, depth, thinnest_node_value):
        import os
        self.tree_name = os.path.splitext(os.path.basename(tree_file_path))[0]
        with open(tree_file_path, "r") as my_file:
            self.tree_str = my_file.read().strip()

        # Äußere Klammern entfernen (die Wurzel)
        if self.tree_str.startswith("(") and self.tree_str.endswith(")"):
            self.tree_str = self.tree_str[1:-1]

        self.depth = depth
        self.thinnest_node_value = max(1, thinnest_node_value)
        self.drawing = None
        self.used_width_per_depth = []
        self.node_layer = None
        self.line_layer = None
        self.gradients = {}

    def create_drawing(self):
        """Initialisiert die SVG-Zeichnung mit Mindestbreite 100px pro Einheit."""
        width = max(100 * self.thinnest_node_value, 100)
        height = self.depth * 100  # Keine leere Ebene unten

        self.drawing = svgwrite.Drawing(f"{self.tree_name}.svg", size=(width, height))
        self.used_width_per_depth = [0 for _ in range(self.depth + 1)]

        # Erst Nodes, dann Linien (Linien im Vordergrund)
        self.node_layer = self.drawing.add(self.drawing.g(id="nodes"))
        self.line_layer = self.drawing.add(self.drawing.g(id="lines", stroke_width=2))

        # Farbverlauf Schwarz → Rot für Blatt-Linien
        grad = self.drawing.linearGradient(start=(0, 0), end=(0, 1), id="black_to_red")
        grad.add_stop_color(offset="0%", color="black")
        grad.add_stop_color(offset="100%", color="red")
        self.drawing.defs.add(grad)
        self.gradients["black_to_red"] = grad

    # ---- Hilfsfunktionen ----

    @staticmethod
    def rectangle_center(insert, width, height=100):
        """Berechnet das Zentrum eines Rechtecks."""
        return insert[0] + width / 2, insert[1] + height / 2

    def draw_line(self, start, end, color="black", gradient_id=None):
        """Zeichnet eine Linie (optional mit Gradient)."""
        if gradient_id:
            self.line_layer.add(
                self.drawing.line(start=start, end=end, stroke=f"url(#{gradient_id})", stroke_width=2)
            )
        else:
            self.line_layer.add(self.drawing.line(start=start, end=end, stroke=color, stroke_width=2))

    def draw_node(self, insert, width, height=100, color="black"):
        """Zeichnet den Kreis in der Mitte eines Rechtecks."""
        cx, cy = DrawTree.rectangle_center(insert, width, height)
        self.node_layer.add(self.drawing.circle(center=(cx, cy), r=25, fill=color))

    def draw_node_and_rect(self, insert, size, color="black"):
        """Zeichnet ein Rechteck mit einem Knoten."""
        width, height = size
        self.node_layer.add(
            self.drawing.rect(insert=insert, size=size, fill="white", stroke="black", stroke_width=3)
        )
        self.draw_node(insert, width, height, color=color)

    def draw_leaf_and_node(self, insert, width, leaf_depth):
        """Zeichnet Blätter: Rechteck geht nach unten, Knoten bleibt oben (rot)."""
        remaining_height = (self.depth - leaf_depth) * 100
        self.node_layer.add(
            self.drawing.rect(
                insert=insert,
                size=(width, 100 + remaining_height),
                fill="white",
                stroke="black",
                stroke_width=3,
            )
        )
        # Blatt (rot)
        self.draw_node(insert, width, height=100, color="red")

    def split_subtrees(self, s):
        """Zerlegt eine Klammernotation in Teilbäume auf oberster Ebene."""
        res, balance, start = [], 0, 0
        for i, ch in enumerate(s):
            if ch == "(":
                if balance == 0:
                    start = i
                balance += 1
            elif ch == ")":
                balance -= 1
                if balance == 0:
                    res.append(s[start + 1:i])
        return res

    # ---- Hauptzeichenlogik ----

    def draw_children(self, node, insert, width, parent_center):
        """Zeichnet alle Kinder eines Knotens."""
        subtrees = self.split_subtrees(node.subtree_str)
        num_children = len(subtrees)

        if num_children == 0:
            # Blatt
            self.draw_leaf_and_node(insert, width, node.depth)
            return

        child_width = max(width / num_children, 100)
        y = node.depth * 100
        next_y = y + 100

        for i, subtree in enumerate(subtrees):
            child_x = insert[0] + i * child_width
            child_center_x = child_x + child_width / 2
            child_insert = (child_x, next_y)
            child_center = (child_center_x, next_y + 50)

            # Ist das Kind ein Blatt?
            is_leaf = len(self.split_subtrees(subtree)) == 0

            # Rechteck + Knoten zeichnen
            self.draw_node_and_rect(child_insert, (child_width, 100), color="red" if is_leaf else "black")

            # Linie: Schwarz→Rot wenn zu Blatt, sonst schwarz
            if is_leaf:
                self.draw_line(parent_center, child_center, gradient_id="black_to_red")
            else:
                self.draw_line(parent_center, child_center, color="black")

            # Rekursion
            self.draw_children(Node(child_width, node.depth + 1, subtree),
                               child_insert, child_width, child_center)

    def save(self):
        self.drawing.save()


# ---------------- TEST ----------------
if __name__ == "__main__":
    example_tree = "((()())(()))"

    with open("baum.txt", "w") as f:
        f.write(example_tree)

    baum = DrawTree("baum.txt", depth=3, thinnest_node_value=8)
    baum.create_drawing()

    # Wurzel = äußere Klammern (bereits entfernt oben)
    root = Node(width=100 * baum.thinnest_node_value, depth=0, subtree_str=baum.tree_str[1:-1])
    root_insert = (0, 0)
    baum.draw_node_and_rect(root_insert, (root.width, 100), color="black")
    root_center = DrawTree.rectangle_center(root_insert, root.width)

    baum.draw_children(root, root_insert, root.width, root_center)

    baum.save()
    print("✅ Datei 'baum.svg' erstellt (Blätter rot, Linien mit Schwarz→Rot-Gradient).")
