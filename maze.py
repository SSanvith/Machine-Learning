import tkinter as tk
import random

# --- Constants ---
ROWS = 25
COLS = 25
CELL_SIZE = 24
WALL_THICKNESS = 2
WINDOW_BG = '#f2f2f2'
CANVAS_BG = 'white'
PATH_COLOR = 'red'
DOT_COLOR = '#4287f5'
START_COLOR = '#5cb85c' # Green
END_COLOR = '#d9534f'   # Red


# --- Main Application Class ---
class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Generator & Solver")
        self.root.configure(bg=WINDOW_BG)
        self.root.resizable(False, False)

        # Frame for controls
        control_frame = tk.Frame(root, bg=WINDOW_BG, padx=10, pady=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Buttons
        self.generate_btn = tk.Button(control_frame, text="Generate Maze", command=self.generate_new_maze)
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        self.solve_btn = tk.Button(control_frame, text="Solve Maze", command=self.solve_maze, state=tk.DISABLED)
        self.solve_btn.pack(side=tk.LEFT, padx=5)
        
        # Canvas for drawing the maze
        canvas_width = COLS * CELL_SIZE
        canvas_height = ROWS * CELL_SIZE
        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg=CANVAS_BG, highlightthickness=0)
        self.canvas.pack(padx=10, pady=(0, 10))

        self.grid = []
        self.solution_path = []
        self.generate_new_maze()

    def generate_new_maze(self):
        """Resets and creates a new maze from scratch."""
        self.solve_btn.config(state=tk.NORMAL)
        self.solution_path = []
        self._create_grid()
        self._generate_maze_structure(0, 0)
        self.draw_maze()

    def _create_grid(self):
        """Initializes the grid with all walls present."""
        self.grid = []
        for r in range(ROWS):
            row = []
            for c in range(COLS):
                # Each cell has walls: [North, East, South, West]
                cell = {'walls': [True, True, True, True], 'visited': False}
                row.append(cell)
            self.grid.append(row)

    def _generate_maze_structure(self, r, c):
        """Recursive backtracking (DFS) algorithm to carve paths."""
        stack = [(r, c)]
        self.grid[r][c]['visited'] = True
        
        while stack:
            current_r, current_c = stack[-1]
            neighbors = []
            
            # Check potential neighbors
            # North
            if current_r > 0 and not self.grid[current_r - 1][current_c]['visited']:
                neighbors.append((current_r - 1, current_c, 0, 2)) # r, c, wall_to_remove, opposite_wall
            # East
            if current_c < COLS - 1 and not self.grid[current_r][current_c + 1]['visited']:
                neighbors.append((current_r, current_c + 1, 1, 3))
            # South
            if current_r < ROWS - 1 and not self.grid[current_r + 1][current_c]['visited']:
                neighbors.append((current_r + 1, current_c, 2, 0))
            # West
            if current_c > 0 and not self.grid[current_r][current_c - 1]['visited']:
                neighbors.append((current_r, current_c - 1, 3, 1))

            if neighbors:
                next_r, next_c, wall_idx, opposite_wall_idx = random.choice(neighbors)
                
                # Remove walls
                self.grid[current_r][current_c]['walls'][wall_idx] = False
                self.grid[next_r][next_c]['walls'][opposite_wall_idx] = False
                
                self.grid[next_r][next_c]['visited'] = True
                stack.append((next_r, next_c))
            else:
                stack.pop()

    def draw_maze(self):
        """Draws the entire maze structure on the canvas."""
        self.canvas.delete("all")
        
        # Draw start and end markers
        self.canvas.create_rectangle(0, 0, CELL_SIZE, CELL_SIZE, fill=START_COLOR, outline="")
        self.canvas.create_rectangle((COLS-1)*CELL_SIZE, (ROWS-1)*CELL_SIZE, COLS*CELL_SIZE, ROWS*CELL_SIZE, fill=END_COLOR, outline="")

        for r in range(ROWS):
            for c in range(COLS):
                x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                walls = self.grid[r][c]['walls']
                
                if walls[0]: # North wall
                    self.canvas.create_line(x1, y1, x2, y1, fill='black', width=WALL_THICKNESS)
                if walls[1]: # East wall
                    self.canvas.create_line(x2, y1, x2, y2, fill='black', width=WALL_THICKNESS)
                if walls[2]: # South wall
                    self.canvas.create_line(x1, y2, x2, y2, fill='black', width=WALL_THICKNESS)
                if walls[3]: # West wall
                    self.canvas.create_line(x1, y1, x1, y2, fill='black', width=WALL_THICKNESS)
        
        if self.solution_path:
            self.draw_solution()

    def solve_maze(self):
        """Solves the maze using A* algorithm."""
        self.solve_btn.config(state=tk.DISABLED)
        path = self._a_star_search()
        if path:
            self.solution_path = path
            self.draw_solution()
        else:
            print("No solution found.")

    def _a_star_search(self):
        """A* pathfinding algorithm implementation."""
        start = (0, 0)
        end = (ROWS - 1, COLS - 1)
        
        open_list = {start}
        came_from = {}
        
        g_score = { (r,c): float('inf') for r in range(ROWS) for c in range(COLS) }
        g_score[start] = 0
        
        f_score = { (r,c): float('inf') for r in range(ROWS) for c in range(COLS) }
        f_score[start] = abs(start[0] - end[0]) + abs(start[1] - end[1]) # Heuristic
        
        while open_list:
            current = min(open_list, key=lambda pos: f_score[pos])
            
            if current == end:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]

            open_list.remove(current)
            r, c = current
            walls = self.grid[r][c]['walls']
            
            # Check neighbors
            # North
            if not walls[0]:
                neighbor = (r - 1, c)
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + (abs(neighbor[0] - end[0]) + abs(neighbor[1] - end[1]))
                    if neighbor not in open_list:
                        open_list.add(neighbor)
            # East
            if not walls[1]:
                neighbor = (r, c + 1)
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + (abs(neighbor[0] - end[0]) + abs(neighbor[1] - end[1]))
                    if neighbor not in open_list:
                        open_list.add(neighbor)
            # South
            if not walls[2]:
                neighbor = (r + 1, c)
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + (abs(neighbor[0] - end[0]) + abs(neighbor[1] - end[1]))
                    if neighbor not in open_list:
                        open_list.add(neighbor)
            # West
            if not walls[3]:
                neighbor = (r, c - 1)
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + (abs(neighbor[0] - end[0]) + abs(neighbor[1] - end[1]))
                    if neighbor not in open_list:
                        open_list.add(neighbor)
                        
        return None # No path found

    def draw_solution(self):
        """Draws the solution path on the canvas."""
        if not self.solution_path:
            return
            
        # Draw line for path
        path_coords = []
        for r, c in self.solution_path:
            x = c * CELL_SIZE + CELL_SIZE / 2
            y = r * CELL_SIZE + CELL_SIZE / 2
            path_coords.extend([x, y])
        
        self.canvas.create_line(path_coords, fill=PATH_COLOR, width=3, capstyle=tk.ROUND)

        # Draw dots on each cell in the path
        dot_radius = 3
        for r, c in self.solution_path:
            x = c * CELL_SIZE + CELL_SIZE / 2
            y = r * CELL_SIZE + CELL_SIZE / 2
            self.canvas.create_oval(x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius, fill=DOT_COLOR, outline="")

# --- Main execution ---
if __name__ == "__main__":
    main_window = tk.Tk()
    app = MazeApp(main_window)
    main_window.mainloop()