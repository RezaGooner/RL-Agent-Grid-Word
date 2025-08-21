import numpy as np 
from grid import simple_grid, windy_grid, negative_grid, ACTION_SPACE

def calculate_probs_and_rewards(grid): 
    # gathering information form the grid
    transition_probs = {}
    rewards = {}
    for (s,a), v in grid.probs.items(): 
        for s2, p in v.items(): 
            transition_probs[(s,a,s2)] = p
            rewards[(s,a,s2)] = grid.rewards.get(s2,0)
    return transition_probs, rewards

def value_iteration(grid, gamma=0.9, threshold=1.0e-3, progress_callback=None):
    transition_probs, rewards = calculate_probs_and_rewards(grid)

    V = {s: 0 for s in grid.all_states()}

    iteration = 0
    while True:
        delta = 0
        for s in grid.all_states():
            if not grid.is_terminal(s):
                old_v = V[s]
                new_v = float("-inf")
                for a in ACTION_SPACE:
                    v = 0
                    for s2 in grid.all_states():
                        r = rewards.get((s, a, s2), 0)
                        t = transition_probs.get((s, a, s2), 0)
                        v += t * (r + gamma * V[s2])
                    new_v = max(new_v, v)
                V[s] = new_v
                delta = max(delta, abs(old_v - V[s]))

        iteration += 1
        if progress_callback:
            progress_callback(iteration)

        if delta < threshold:
            break

    # derive optimal policy
    policy = {}
    for s in grid.actions.keys():
        best_action = None
        best_value = float("-inf")
        for a in ACTION_SPACE:
            v = 0
            for s2 in grid.all_states():
                r = rewards.get((s, a, s2), 0)
                t = transition_probs.get((s, a, s2), 0)
                v += t * (r + gamma * V[s2])
            if v > best_value:
                best_action = a
                best_value = v
        policy[s] = {best_action: 1.0}

    return V, policy
