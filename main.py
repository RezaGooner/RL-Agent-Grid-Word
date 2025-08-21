import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel
import os, json
from grid import GridWorld, ACTION_SPACE
from value_iteration import value_iteration

CELL_SIZE = 80
SAVE_DIR = "saved_maps"

class GridEditorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GridWorld Editor")

        os.makedirs(SAVE_DIR, exist_ok=True)

        self.rows = 3
        self.cols = 4
        self.step_cost = -0.1
        self.start_pos = (0, 0)
        self.edit_mode = "wall"
        self.show_values = False
        
        self.V = {}
        self.policy = {}
        self.agent_pos = None
        self.visited_cells = set()
        self.start_text_override = None
        
        self.images = {}
        self.load_images()
        self.make_empty_grid()

        self.create_toolbar()

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack()
        self.update_canvas_size()
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.create_menubar()
        self.draw_grid()

    def load_images(self):
        try:
            self.images["empty"] = tk.PhotoImage(file="images/empty.png")
            self.images["wall"] = tk.PhotoImage(file="images/wall.png")
            self.images["reward"] = tk.PhotoImage(file="images/reward.png")
            self.images["penalty"] = tk.PhotoImage(file="images/penalty.png")
            self.images["start"] = tk.PhotoImage(file="images/start.png")
            self.images["agent"] = tk.PhotoImage(file="images/agent.png")
            self.images["path"] = tk.PhotoImage(file="images/path.png")
        except Exception as e:
            messagebox.showerror("Image Load Error", str(e))

    def create_toolbar(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        modes = [
            ("Wall", "wall"),
            ("Reward", "reward"),
            ("Penalty", "penalty"),
            ("Start Point", "start"),
            ("Delete", "clear"),
        ]
        for text, mode in modes:
            tk.Button(toolbar, text=text, command=lambda m=mode: self.set_edit_mode(m)).pack(side=tk.LEFT, padx=2, pady=2)

        tk.Button(toolbar, text="Run", bg="lightgreen", command=self.run_value_iteration).pack(side=tk.LEFT, padx=8, pady=2)

    def create_menubar(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.reset_grid)
        file_menu.add_command(label="Save Current Map", command=self.save_map)
        file_menu.add_command(label="Load Preset/Custom Map", command=self.show_map_loader)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        grid_menu = tk.Menu(menubar, tearoff=0)
        grid_menu.add_command(label="Change Rows & Cols", command=self.change_size)
        grid_menu.add_command(label="Set Step Cost", command=self.change_step_cost)
        grid_menu.add_command(label="Change Reward Value", command=self.change_reward_value)
        grid_menu.add_command(label="Change Penalty Value", command=self.change_penalty_value)
        menubar.add_cascade(label="Grid", menu=grid_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Toggle Values/Policy", command=self.toggle_show_values)
        menubar.add_cascade(label="View", menu=view_menu)

        self.root.config(menu=menubar)

    def set_edit_mode(self, mode):
        self.edit_mode = mode

    def toggle_show_values(self):
        self.show_values = not self.show_values
        self.draw_grid()

    def make_empty_grid(self):
        rewards = {}
        actions = {}
        probs = {}
        for i in range(self.rows):
            for j in range(self.cols):
                rewards[(i, j)] = self.step_cost
                actions[(i, j)] = ACTION_SPACE
                for a in ACTION_SPACE:
                    ni, nj = i, j
                    if a == 'U': ni = max(0, i - 1)
                    if a == 'D': ni = min(self.rows - 1, i + 1)
                    if a == 'L': nj = max(0, j - 1)
                    if a == 'R': nj = min(self.cols - 1, j + 1)
                    probs[((i, j), a)] = {(ni, nj): 1.0}

        self.grid = GridWorld(self.rows, self.cols, self.start_pos)
        self.grid.set(rewards, actions, probs)

    def update_canvas_size(self):
        width = self.cols * CELL_SIZE
        height = self.rows * CELL_SIZE
        self.canvas.config(width=width, height=height)
        self.root.geometry(f"{width+50}x{height+120}")

    def draw_grid(self, show_agent=False):
        self.canvas.delete("all")
        for i in range(self.rows):
            for j in range(self.cols):
                x = j * CELL_SIZE + CELL_SIZE // 2
                y = i * CELL_SIZE + CELL_SIZE // 2
                img_key = "empty"
                if (i, j) == self.start_pos and self.start_text_override is None:
                    img_key = "start"
                elif (i, j) in self.visited_cells and (i, j) != self.agent_pos:
                    img_key = "path"
                elif (i, j) not in self.grid.actions:
                    if (i, j) in self.grid.rewards:
                        if self.grid.rewards[(i, j)] > 0:
                            img_key = "reward"
                        elif self.grid.rewards[(i, j)] < 0:
                            img_key = "penalty"
                        else:
                            img_key = "wall"
                    else:
                        img_key = "wall"

                if img_key in self.images:
                    self.canvas.create_image(x, y, image=self.images[img_key])
                else:
                    self.canvas.create_rectangle(j*CELL_SIZE, i*CELL_SIZE,
                                                 (j+1)*CELL_SIZE, (i+1)*CELL_SIZE,
                                                 outline="black", fill="white")

                if self.start_text_override == (i, j):
                    self.canvas.create_text(x, y, text="start", fill="blue", font=("Arial", 14, "bold"))

                if self.show_values and (i, j) != self.agent_pos:
                    val_text = ""
                    if self.V and (i, j) in self.V:
                        val_text = f"{self.V[(i, j)]:.2f}"
                    elif self.policy and (i, j) in self.policy:
                        val_text = list(self.policy[(i, j)].keys())[0]
                    if val_text:
                        self.canvas.create_text(x, y, text=val_text, fill="black")

        if show_agent and self.agent_pos:
            ax = self.agent_pos[1] * CELL_SIZE + CELL_SIZE // 2
            ay = self.agent_pos[0] * CELL_SIZE + CELL_SIZE // 2
            self.canvas.create_image(ax, ay, image=self.images["agent"])

    def on_canvas_click(self, event):
        j = event.x // CELL_SIZE
        i = event.y // CELL_SIZE
        if not (0 <= i < self.rows and 0 <= j < self.cols):
            return

        if self.edit_mode == "wall":
            if (i, j) in self.grid.actions:
                del self.grid.actions[(i, j)]
            if (i, j) in self.grid.rewards and self.grid.rewards[(i, j)] == self.step_cost:
                del self.grid.rewards[(i, j)]
        elif self.edit_mode == "reward":
            self.grid.rewards[(i, j)] = 5
            if (i, j) in self.grid.actions:
                del self.grid.actions[(i, j)]
        elif self.edit_mode == "penalty":
            self.grid.rewards[(i, j)] = -5
            if (i, j) in self.grid.actions:
                del self.grid.actions[(i, j)]
        elif self.edit_mode == "start":
            self.start_pos = (i, j)
            self.grid.start = self.start_pos
        elif self.edit_mode == "clear":
            self.grid.rewards[(i, j)] = self.step_cost
            self.grid.actions[(i, j)] = ACTION_SPACE

        self.draw_grid()

    def change_size(self):
        try:
            new_rows = int(simpledialog.askstring("Input", "Number of rows:", parent=self.root))
            new_cols = int(simpledialog.askstring("Input", "Number of cols:", parent=self.root))
        except (ValueError, TypeError):
            return
        self.rows = new_rows
        self.cols = new_cols
        self.make_empty_grid()
        self.update_canvas_size()
        self.draw_grid()

    def change_step_cost(self):
        try:
            new_cost = float(simpledialog.askstring("Input", "Enter new step cost:", parent=self.root))
        except (ValueError, TypeError):
            return
        self.step_cost = new_cost
        for (i, j) in list(self.grid.rewards.keys()):
            if (i, j) in self.grid.actions and self.grid.rewards[(i, j)] == self.step_cost:
                self.grid.rewards[(i, j)] = new_cost
        self.draw_grid()

    def change_reward_value(self):
        try:
            new_reward = float(simpledialog.askstring("Input", "Enter new reward value:", parent=self.root))
        except (ValueError, TypeError):
            return
        for pos in self.grid.rewards:
            if self.grid.rewards[pos] > 0:
                self.grid.rewards[pos] = new_reward
        self.draw_grid()

    def change_penalty_value(self):
        try:
            new_penalty = float(simpledialog.askstring("Input", "Enter new penalty value:", parent=self.root))
        except (ValueError, TypeError):
            return
        for pos in self.grid.rewards:
            if self.grid.rewards[pos] < 0:
                self.grid.rewards[pos] = new_penalty
        self.draw_grid()

    def reset_grid(self):
        self.visited_cells.clear()
        self.agent_pos = None
        self.start_text_override = None
        self.make_empty_grid()
        self.draw_grid()


    def save_map(self):
        name = simpledialog.askstring("Save Map", "Enter map name:", parent=self.root)
        if not name:
            return
        data = {
            "rows": self.rows,
            "cols": self.cols,
            "start_pos": self.start_pos,
            "rewards": {f"{i},{j}": v for (i, j), v in self.grid.rewards.items()},
            "actions": {f"{i},{j}": v for (i, j), v in self.grid.actions.items()},
            "probs": {
                f"{i},{j}|{a}": {f"{ni},{nj}": p for (ni, nj), p in dest.items()}
                for ((i, j), a), dest in self.grid.probs.items()
            }
        }
        with open(os.path.join(SAVE_DIR, f"{name}.json"), "w") as f:
            json.dump(data, f)
        messagebox.showinfo("Saved", f"Map '{name}' saved successfully!")

    def load_map(self, path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
            self.rows = data["rows"]
            self.cols = data["cols"]
            self.start_pos = tuple(data["start_pos"])
            self.grid = GridWorld(self.rows, self.cols, self.start_pos)

            self.grid.rewards = {tuple(map(int, k.split(","))): v for k, v in data["rewards"].items()}
            self.grid.actions = {tuple(map(int, k.split(","))): v for k, v in data["actions"].items()}
            self.grid.probs = {
                (tuple(map(int, key.split("|")[0].split(","))), key.split("|")[1]):
                    {tuple(map(int, dest_key.split(","))): prob for dest_key, prob in dests.items()}
                for key, dests in data["probs"].items()
            }

            self.update_canvas_size()
            self.draw_grid()
        except Exception as e:
            messagebox.showerror("Error", f"Could not load map: {e}")



    def show_map_loader(self):
        win = Toplevel(self.root)
        win.title("Load Map")
        presets = [
            ("Preset Map 1", os.path.join(SAVE_DIR, "preset1.json")),
            ("Preset Map 2", os.path.join(SAVE_DIR, "preset2.json")),
            ("Preset Map 3", os.path.join(SAVE_DIR, "preset3.json")),
        ]
        for name, path in presets:
            tk.Button(win, text=name, command=lambda p=path: (self.load_map(p), win.destroy())).pack(fill="x", pady=2)

        tk.Label(win, text="--- Saved Maps ---").pack(pady=5)
        for file in os.listdir(SAVE_DIR):
            if file.endswith(".json") and not file.startswith("preset"):
                tk.Button(win, text=file[:-5], command=lambda p=os.path.join(SAVE_DIR, file): (self.load_map(p), win.destroy())).pack(fill="x", pady=1)

    def run_value_iteration(self):
        self.V, self.policy = value_iteration(self.grid)
        self.draw_grid()
        self.simulate_policy(self.policy)

    def simulate_policy(self, policy, delay=500):
        self.visited_cells.clear()
        self.grid.reset()
        self.agent_pos = None
        self.start_text_override = None
        path = [self.grid.current_state()]
        start_state = path[0]
        while not self.grid.game_over():
            s = self.grid.current_state()
            if s not in policy:
                break
            action = list(policy[s].keys())[0]
            self.grid.move(action)
            path.append(self.grid.current_state())
        terminal_state = path[-1]
        def step_animation(index):
            if index < len(path):
                self.agent_pos = path[index]
                if self.agent_pos == start_state:
                    self.start_text_override = start_state
                if self.agent_pos != start_state:
                    self.visited_cells.add(self.agent_pos)
                if self.agent_pos == terminal_state:
                    if terminal_state in self.grid.rewards and self.grid.rewards[terminal_state] > 0:
                        del self.grid.rewards[terminal_state]
                self.draw_grid(show_agent=True)
                self.root.after(delay, lambda: step_animation(index + 1))
            else:
                self.draw_grid(show_agent=True)
        step_animation(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = GridEditorGUI(root)
    root.mainloop()
