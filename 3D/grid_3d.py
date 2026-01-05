# core/grid_3d.py

import numpy as np
from typing import Dict, Tuple, Set

EMPTY = 0
WALL = -1
REWARD = 1
PENALTY = -1

ACTIONS_3D = {
    'U': (-1, 0, 0),   # up (x-)
    'D': (1, 0, 0),    # down (x+)
    'L': (0, -1, 0),   # left (y-)
    'R': (0, 1, 0),    # right (y+)
    'B': (0, 0, -1),   # back (z-)
    'F': (0, 0, 1),    # forward (z+)
}

class GridWorld3D:
    def __init__(self, depth=4, height=4, width=4, step_cost=-0.04, reward_val=1.0, penalty_val=-1.0):
        self.depth = depth
        self.height = height
        self.width = width
        self.step_cost = step_cost
        self.reward_val = reward_val
        self.penalty_val = penalty_val
        self.walls: Set[Tuple[int, int, int]] = set()
        self.rewards: Dict[Tuple[int, int, int], float] = {}
        self.start_pos = (0, 0, 0)

    def set_cell(self, x, y, z, cell_type):
        if not (0 <= x < self.depth and 0 <= y < self.height and 0 <= z < self.width):
            return
        pos = (x, y, z)
        if cell_type == WALL:
            self.walls.add(pos)
            self.rewards.pop(pos, None)
        elif cell_type == REWARD:
            self.rewards[pos] = self.reward_val
            self.walls.discard(pos)
        elif cell_type == PENALTY:
            self.rewards[pos] = self.penalty_val
            self.walls.discard(pos)
        else:  # EMPTY or DELETE
            self.walls.discard(pos)
            self.rewards.pop(pos, None)

    def set_start(self, x, y, z):
        if 0 <= x < self.depth and 0 <= y < self.height and 0 <= z < self.width:
            self.start_pos = (x, y, z)

    def is_terminal(self, state):
        return state in self.rewards

    def is_wall(self, state):
        return state in self.walls

    def get_reward(self, state):
        return self.rewards.get(state, self.step_cost)

    def get_actions(self, state):
        if self.is_terminal(state) or self.is_wall(state):
            return []
        return list(ACTIONS_3D.keys())

    def get_next_state(self, state, action):
        x, y, z = state
        dx, dy, dz = ACTIONS_3D[action]
        nx, ny, nz = x + dx, y + dy, z + dz
        if not (0 <= nx < self.depth and 0 <= ny < self.height and 0 <= nz < self.width):
            return state
        if (nx, ny, nz) in self.walls:
            return state
        return (nx, ny, nz)

    def get_all_states(self):
        states = []
        for x in range(self.depth):
            for y in range(self.height):
                for z in range(self.width):
                    if (x, y, z) not in self.walls:
                        states.append((x, y, z))
        return states
