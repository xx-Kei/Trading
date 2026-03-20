import tkinter as tk
from collections import deque
import random

ROWS = 20
COLS = 20
CELL_SIZE = 30
ANIMATION_DELAY = 50  # milliseconds

WINDOW_SIZE = ROWS * CELL_SIZE

class GridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Animated BFS Pathfinding with Random Board")

        self.mode = "wall"  # Modes: wall, erase, start, end
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.rectangles = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.start = None
        self.end = None

        self.canvas = tk.Canvas(root, width=WINDOW_SIZE, height=WINDOW_SIZE, bg="white")
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<Button-1>", self.on_drag)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)
        tk.Button(button_frame, text="Wall Mode", command=self.set_wall_mode).pack(side="left", padx=2)
        tk.Button(button_frame, text="Erase Mode", command=self.set_erase_mode).pack(side="left", padx=2)
        tk.Button(button_frame, text="Set Start", command=self.set_start_mode).pack(side="left", padx=2)
        tk.Button(button_frame, text="Set End", command=self.set_end_mode).pack(side="left", padx=2)
        tk.Button(button_frame, text="Compute Path", command=self.compute_path).pack(side="left", padx=2)
        tk.Button(button_frame, text="Clear Board", command=self.clear_board).pack(side="left", padx=2)
        tk.Button(button_frame, text="Random Board", command=self.random_board).pack(side="left", padx=2)

        self.draw_grid()

    def draw_grid(self):
        for r in range(ROWS):
            for c in range(COLS):
                x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")
                self.rectangles[r][c] = rect

    def on_drag(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if 0 <= row < ROWS and 0 <= col < COLS:
            if self.mode == "wall":
                self.grid[row][col] = 1
                self.canvas.itemconfig(self.rectangles[row][col], fill="black")
            elif self.mode == "erase":
                self.grid[row][col] = 0
                self.canvas.itemconfig(self.rectangles[row][col], fill="white")
            elif self.mode == "start":
                self.clear_path()
                if self.start:
                    pr, pc = self.start
                    self.canvas.itemconfig(self.rectangles[pr][pc], fill="white")
                self.start = (row, col)
                self.canvas.itemconfig(self.rectangles[row][col], fill="green")
            elif self.mode == "end":
                self.clear_path()
                if self.end:
                    pr, pc = self.end
                    self.canvas.itemconfig(self.rectangles[pr][pc], fill="white")
                self.end = (row, col)
                self.canvas.itemconfig(self.rectangles[row][col], fill="red")

    # Mode buttons
    def set_wall_mode(self): self.mode = "wall"
    def set_erase_mode(self): self.mode = "erase"
    def set_start_mode(self): self.mode = "start"
    def set_end_mode(self): self.mode = "end"

    def clear_board(self):
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.start = None
        self.end = None
        for r in range(ROWS):
            for c in range(COLS):
                self.canvas.itemconfig(self.rectangles[r][c], fill="white")

    def clear_path(self):
        for r in range(ROWS):
            for c in range(COLS):
                if self.canvas.itemcget(self.rectangles[r][c], "fill") == "blue":
                    self.canvas.itemconfig(self.rectangles[r][c], fill="white")

    # BFS pathfinding
    def compute_path(self):
        if not self.start or not self.end:
            print("Set start and end first!")
            return
        self.clear_path()

        sr, sc = self.start
        er, ec = self.end

        visited = [[False for _ in range(COLS)] for _ in range(ROWS)]
        prev = [[None for _ in range(COLS)] for _ in range(ROWS)]
        queue = deque()
        queue.append((sr, sc))
        visited[sr][sc] = True

        dirs = [(-1,0),(1,0),(0,-1),(0,1)]
        found = False

        while queue:
            r, c = queue.popleft()
            if (r, c) == (er, ec):
                found = True
                break
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and not visited[nr][nc] and self.grid[nr][nc] == 0:
                    visited[nr][nc] = True
                    prev[nr][nc] = (r, c)
                    queue.append((nr, nc))

        if not found:
            print("No path found!")
            return

        path = []
        cur = (er, ec)
        while cur != (sr, sc):
            path.append(cur)
            cur = prev[cur[0]][cur[1]]
        path.reverse()
        self.animate_path(path)

    def animate_path(self, path, index=0):
        if index >= len(path):
            return
        r, c = path[index]
        if (r, c) != self.start and (r, c) != self.end:
            self.canvas.itemconfig(self.rectangles[r][c], fill="blue")
        self.canvas.after(ANIMATION_DELAY, lambda: self.animate_path(path, index+1))

    # Random board + random start/end
    def random_board(self, density=0.3):
        self.clear_board()
        # Fill walls
        for r in range(ROWS):
            for c in range(COLS):
                if random.random() < density:
                    self.grid[r][c] = 1
                    self.canvas.itemconfig(self.rectangles[r][c], fill="black")

        # Choose random start/end on empty cells
        empty_cells = [(r,c) for r in range(ROWS) for c in range(COLS) if self.grid[r][c] == 0]
        if len(empty_cells) < 2:
            print("Not enough empty cells for start/end")
            return
        self.start = random.choice(empty_cells)
        self.end = random.choice([cell for cell in empty_cells if cell != self.start])

        sr, sc = self.start
        er, ec = self.end
        self.canvas.itemconfig(self.rectangles[sr][sc], fill="green")
        self.canvas.itemconfig(self.rectangles[er][ec], fill="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = GridApp(root)
    root.mainloop()