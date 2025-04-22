class BNode:
    def __init__(self, is_leaf=True):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []

class BTree:
    def __init__(self, min_degree=2):
        self.root = BNode()
        self.t = min_degree  # Mínimo grado t (para 3 claves, t=2)
        self.resultado = ""

    def _split_child(self, parent, idx):
        t = self.t
        full_child = parent.children[idx]
        new_child = BNode(is_leaf=full_child.is_leaf)

        middle_key = full_child.keys[t - 1]
        parent.keys.insert(idx, middle_key)

        new_child.keys = full_child.keys[t:]
        full_child.keys = full_child.keys[:t - 1]

        if not full_child.is_leaf:
            new_child.children = full_child.children[t:]
            full_child.children = full_child.children[:t]

        parent.children.insert(idx + 1, new_child)

        self.resultado += f"Se dividió el nodo con {middle_key} como clave media.\n"

    def _insert_non_full(self, node, key):
        i = len(node.keys) - 1
        if node.is_leaf:
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
            self.resultado += f"Insertado {key} en nodo hoja.\n"
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1

            if len(node.children[i].keys) == 2 * self.t - 1:
                self.resultado += f"Hijo en posición {i} lleno. Se divide antes de insertar {key}.\n"
                self._split_child(node, i)

                if key > node.keys[i]:
                    i += 1
                    self.resultado += f"{key} se insertará en el hijo derecho tras división.\n"
                else:
                    self.resultado += f"{key} se insertará en el hijo izquierdo tras división.\n"

            self._insert_non_full(node.children[i], key)

    def insert(self, key):
        self.resultado = f"Insertando {key}:\n"
        r = self.root
        if len(r.keys) == 2 * self.t - 1:
            new_root = BNode(is_leaf=False)
            new_root.children.append(r)
            self.root = new_root
            self.resultado += "Raíz llena, se crea nueva raíz y se divide.\n"
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, key)
        else:
            self._insert_non_full(r, key)
        return self.resultado

    def print_tree(self):
        if not self.root:
            return "Árbol vacío"
        output = ""
        queue = [(self.root, 0)]
        current_level = 0
        line = ""
        while queue:
            node, level = queue.pop(0)
            if level > current_level:
                output += f"Nivel {current_level}: {line}\n"
                line = ""
                current_level = level
            line += str(node.keys) + " "
            if not node.is_leaf:
                for child in node.children:
                    queue.append((child, level + 1))
        output += f"Nivel {current_level}: {line}\n"
        return output


valores = [78, 393, 12, 90, 120, 1, 10, 99, 34, 54, 121, 14, 60, 35]

bt = BTree(min_degree=2)
for v in valores:
    print(bt.insert(v))
    print(bt.print_tree())
    print("=" * 60)

print("Árbol B final:")
print(bt.print_tree())
