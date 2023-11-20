import queue


class PuzzleState:
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def __str__(self):
        return "\n".join(" ".join(map(str, row)) for row in self.puzzle)

    def __eq__(self, other):
        return self.puzzle == other.puzzle

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.puzzle))

    def get_blank_position(self):
        for i, row in enumerate(self.puzzle):
            for j, num in enumerate(row):
                if num == 0:
                    return i, j

    def get_neighbors(self):
        i, j = self.get_blank_position()
        neighbors = []

        for move in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ni, nj = i + move[0], j + move[1]

            if 0 <= ni < 3 and 0 <= nj < 3:
                new_puzzle = [row.copy() for row in self.puzzle]
                new_puzzle[i][j], new_puzzle[ni][nj] = (
                    new_puzzle[ni][nj],
                    new_puzzle[i][j],
                )
                neighbors.append(PuzzleState(new_puzzle))

        return neighbors

    def h1(self, goal_state):
        # Порівнюємо поточний стан із цільовим і обчислюємо кількість фішок, які не на своїх місцях
        return sum(
            1
            for i in range(3)
            for j in range(3)
            if self.puzzle[i][j] != goal_state.puzzle[i][j]
        )


def bfs(init_state, goal_state):
    visited = set()
    q = queue.Queue()
    q.put((init_state, 0))

    while not q.empty():
        current_state, steps = q.get()

        if current_state == goal_state:
            return steps

        if current_state not in visited:
            visited.add(current_state)

            for neighbor in current_state.get_neighbors():
                q.put((neighbor, steps + 1))

    return -1


def rbfs(current_state, goal_state, f_limit=float("inf")):
    if current_state == goal_state:
        return 0

    successors = [(neighbor, 1) for neighbor in current_state.get_neighbors()]
    if not successors:
        return float("inf")

    while True:
        best = min(successors, key=lambda x: x[1])
        if best[1] > f_limit:
            return best[1]
        alternative = min(
            successors, key=lambda x: x[1] if x[1] > best[1] else float("inf")
        )
        result = rbfs(best[0], goal_state, min(f_limit, alternative[1]))
        if result < float("inf"):
            return result
        successors.remove(best)


initial_state = PuzzleState([[1, 2, 3], [4, 5, 6], [0, 7, 8]])
goal_state = PuzzleState([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

# Використовуйте BFS
bfs_steps = bfs(initial_state, goal_state)
print(f"BFS Steps: {bfs_steps}")

# Використовуйте RBFS
rbfs_steps = rbfs(initial_state, goal_state)
print(f"RBFS Steps: {rbfs_steps}")

# Використовуйте h1
h1_value = initial_state.h1(goal_state)
print(f"h1 Value: {h1_value}")
