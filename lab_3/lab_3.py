class AVLNode:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        if node is None:
            return 0
        return node.height

    def update_height(self, node):
        if node is not None:
            node.height = 1 + max(self.height(node.left), self.height(node.right))

    def get_balance(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)

    def rotate_right(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self.update_height(y)
        self.update_height(x)

        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self.update_height(x)
        self.update_height(y)

        return y

    def insert(self, node, key, data):
        if node is None:
            return AVLNode(key, data)

        if key < node.key:
            node.left = self.insert(node.left, key, data)
        else:
            node.right = self.insert(node.right, key, data)

        self.update_height(node)

        balance = self.get_balance(node)

        if balance > 1:
            if key < node.left.key:
                return self.rotate_right(node)
            else:
                node.left = self.rotate_left(node.left)
                return self.rotate_right(node)

        if balance < -1:
            if key > node.right.key:
                return self.rotate_left(node)
            else:
                node.right = self.rotate_right(node.right)
                return self.rotate_left(node)

        return node

    def search(self, node, key):
        if node is None or node.key == key:
            return node

        if key < node.key:
            return self.search(node.left, key)
        else:
            return self.search(node.right, key)

    def edit(self, node, key, new_data):
        to_edit = self.search(node, key)
        if to_edit is not None:
            to_edit.data = new_data

    def get_min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete(self, node, key):
        if node is None:
            return node

        if key < node.key:
            node.left = self.delete(node.left, key)
        elif key > node.key:
            node.right = self.delete(node.right, key)
        else:
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp

            temp = self.get_min_value_node(node.right)
            node.key = temp.key
            node.right = self.delete(node.right, temp.key)

        if node is None:
            return node

        self.update_height(node)

        balance = self.get_balance(node)

        if balance > 1:
            if self.get_balance(node.left) >= 0:
                return self.rotate_right(node)
            else:
                node.left = self.rotate_left(node.left)
                return self.rotate_right(node)

        if balance < -1:
            if self.get_balance(node.right) <= 0:
                return self.rotate_left(node)
            else:
                node.right = self.rotate_right(node.right)
                return self.rotate_left(node)

        return node


# Ваш графічний інтерфейс тут
# Можна використовувати бібліотеки, такі як Tkinter, PyQt, або інші для створення GUI

# Приклад використання:

avl_tree = AVLTree()

# Додавання записів
avl_tree.root = avl_tree.insert(avl_tree.root, 10, "Data for key 10")
avl_tree.root = avl_tree.insert(avl_tree.root, 20, "Data for key 20")
avl_tree.root = avl_tree.insert(avl_tree.root, 30, "Data for key 30")

# Пошук запису
search_result = avl_tree.search(avl_tree.root, 20)
if search_result:
    print("Found:", search_result.key, search_result.data)
else:
    print("Not found")

# Редагування запису
avl_tree.edit(avl_tree.root, 20, "New data for key 20")

# Видалення запису
avl_tree.root = avl_tree.delete(avl_tree.root, 20)
