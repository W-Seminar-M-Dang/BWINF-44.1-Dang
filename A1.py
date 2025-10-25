import sys

class Node:
    """Object for node in tree with width (1/real relative width), subtree, and depth"""

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
    """Returns list of all leaves in order from left to right"""
    leaves = []

    def search(node):
        """Searches recursively the subtree, adds child node to leaves if child node is a leaf"""

        child_nodes_subtrees = []
        bracket_counter = 0
        child_nodes_counter = 0
        child_node_start = 0

        # adds all subtrees of child notes to child_nodes_subtrees
        for bracket_index in range(len(node.subtree_str)):
            if node.subtree_str[bracket_index] == "(":
                bracket_counter += 1
            elif node.subtree_str[bracket_index] == ")":
                bracket_counter -= 1
                if bracket_counter == 0: # means that
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

    # File path as terminal argument
    with open(sys.argv[1], "r") as my_file:
        tree = my_file.read().strip()

    leaves1 = find_leaves(Node(1, 0, tree[1:-1]))

    # checks if reverted tree is the same
    if leaves1 == leaves1[::-1]:
        print("Der Baum ist Drehfreudig")
    else:
        print("Der Baum ist nicht Drehfreudig")