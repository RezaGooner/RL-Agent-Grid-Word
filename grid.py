import numpy as np 

ACTION_SPACE = ('U', 'D', 'L', 'R')

class GridWorld:
    def __init__(self, rows, cols, start): 
        self.rows = rows
        self.cols = cols
        self.i = start[0]
        self.j = start[1]
        self.start = start

    def set(self, rewards, actions, probs): 
        # reward: a dictionary of {(r,c): r} ==> {(0,3): 1, ...}
        # actions: a dictionary of {(r,c): [actions]} ==> {(0,0): ['R', 'D'], ...}
        # probs: a dictionary of {((r,c), a): (r', c'): p } ==> {((0,0), 'R'): {(0,1): 0.5, (1,0):0.5} , ...}

        self.rewards = rewards
        self.actions = actions 
        self.probs = probs

    def set_state(self, s): 
        self.i = s[0]
        self.j = s[1]

    def current_state(self): 
        return (self.i, self.j)

    def is_terminal(self, s): 
        return s not in self.actions

    def move(self, a): 
        s = (self.i, self.j)
        next_states_probs = self.probs[(s,a)]
        next_states = list(next_states_probs.keys())
        next_probs = list(next_states_probs.values())

        idx = np.random.choice(len(next_states), p = next_probs)

        s2 = next_states[idx]

        # update the current state
        self.i, self.j = s2

        #return a reward if any
        return self.rewards.get(s2, 0)

    def game_over(self):
        return (self.i, self.j) not in self.actions

    def all_states(self): 
        return set(self.actions.keys() | self.rewards.keys()) 

    def reset(self): 
        self.i, self.j = self.start
        return self.start
