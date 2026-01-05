# core/value_iteration_3d.py

from core.grid_3d import GridWorld3D
from typing import Dict, Tuple

GAMMA = 0.9
THETA = 1e-6

def value_iteration(env: GridWorld3D) -> Tuple[Dict[Tuple, float], Dict[Tuple, str]]:
    V = {s: 0.0 for s in env.get_all_states()}
    policy = {}

    while True:
        delta = 0
        for s in env.get_all_states():
            if env.is_terminal(s):
                V[s] = env.get_reward(s)
                continue

            v_old = V[s]
            action_values = {}
            for a in env.get_actions(s):
                next_s = env.get_next_state(s, a)
                reward = env.get_reward(s)
                action_values[a] = reward + GAMMA * V[next_s]
            if action_values:
                V[s] = max(action_values.values())
                policy[s] = max(action_values, key=action_values.get)
            else:
                V[s] = env.get_reward(s)

            delta = max(delta, abs(v_old - V[s]))

        if delta < THETA:
            break

    return V, policy
