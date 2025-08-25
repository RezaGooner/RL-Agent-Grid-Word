# RL-Agent-Grid-World Editor

An interactive **GridWorld Editor** and **Value Iteration Simulator** built with Python and Tkinter, designed for creating, editing, saving, and loading custom reinforcement learning environments.  
Perfect for experimenting with **Markov Decision Processes (MDPs)**, **policy/value visualizations**, and **agent path simulations**.


<img width="350" height="400" alt="image" src="https://github.com/user-attachments/assets/e2033780-7658-482b-8c90-6fb023700cad" />

<img width="350" height="400" alt="image" src="https://github.com/user-attachments/assets/2be6682b-2cd8-43af-8598-b886495286a4" />

---

## ✨ Features

- **Interactive GUI** built with Tkinter
- Create and modify GridWorld layouts:
  - Place **walls**, **rewards**, and **penalties**
  - Set a custom **start position**
  - Remove any cell configuration
- Change grid size (rows & columns) dynamically
- Adjust **step cost**, reward, and penalty values
- **Save** and **load** custom maps as JSON
- **Preset maps** for quick testing
- Run **Value Iteration** to compute:
  - State value function (**V**)
  - Deterministic policy
- Animate the agent following the computed policy
- Toggle between showing **values** or **policy actions**
- Supports **path visualization** and maintains visited cells

---

## 📦 Project Structure

```
RL-Agent-Grid-World/
│
├── images/                  # PNG icons for different cell types & agent
│   ├── empty.png
│   ├── wall.png
│   ├── reward.png
│   ├── penalty.png
│   ├── start.png
│   ├── agent.png
│   └── path.png
│
├── saved_maps/              # Saved and preset maps (JSON)
│   ├── preset1.json
│   ├── preset2.json
│   ├── preset3.json
│   └── *.json               # Custom user-created maps
│
├── grid.py                  # Core GridWorld environment & dynamics
├── value_iteration.py       # Value iteration algorithm implementation
├── editor.py                # GUI implementation (this file)
└── README.md                # Project documentation
```

---

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/RezaGooner/RL-Agent-Grid-World.git
   cd RL-Agent-Grid-World
   ```

2. **Install dependencies**  
   This project only requires Python’s standard library.  
   Ensure you have **Python 3.8+**.

3. **Ensure images are available**  
   The GUI depends on PNG files in the `images/` directory.

4. **Run the editor**
   ```bash
   python main.py
   ```

---

## 🕹️ Usage Guide

### Toolbar Modes
- **Wall** → Block movement; removes actions for the cell
- **Reward** → Positive terminal state
- **Penalty** → Negative terminal state
- **Start Point** → Set agent's starting position
- **Delete** → Restore a cell to empty traversable space

### Menu Options
- **File → New** → Reset grid to empty
- **File → Save Current Map** → Save environment as JSON in `saved_maps/`
- **File → Load Preset/Custom Map** → Open loader to pick a preset or saved map
- **Grid → Change Rows & Cols** → Resize the grid
- **Grid → Set Step Cost** → Adjust per-step penalty
- **Grid → Change Reward/Penalty Value** → Adjust terminal state rewards
- **View → Toggle Values/Policy** → Switch between showing value function and policy arrows

### Running Value Iteration
1. Design or load a map
2. Click **Run** (green button) to run Value Iteration
3. Agent will animate following the optimal policy

---

## 📖 How It Works

### Grid Representation
- Every state `(i, j)` has:
  - **Reward** value (`step_cost` by default)
  - **Available actions** from `ACTION_SPACE = ['U', 'D', 'L', 'R']`
  - **Transition probabilities** defined as a dictionary

### Value Iteration
- Imported from `value_iteration.py`
- Computes:
  ```
  V(s) = max_a Σ_s' P(s'|s,a) [ R(s,a,s') + γ V(s') ]
  ```
- Outputs `(V, policy)` dictionaries

### Simulation
- Starts from the `start_pos`
- Follows deterministic policy until terminal state
- Visited path is visually highlighted on the grid

---

## 💾 File Save/Load Format

- **Rewards**: `{ "i,j": value, ... }`
- **Actions**: `{ "i,j": ["U","D",...], ... }`
- **Probs**: `{ "i,j|A": { "ni,nj": probability, ... }, ... }`

---


## 📜 License

MIT License — Feel free to modify and share.

---

## 👤 Author

**Reza Gooner**  
- GitHub: [@RezaGooner](https://github.com/RezaGooner)  
- Email: RezaAsadiProgrammer@Gmail.com
