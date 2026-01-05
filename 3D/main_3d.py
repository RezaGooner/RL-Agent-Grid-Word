# main_3d.py

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from grid_3d import GridWorld3D, WALL, REWARD, PENALTY, ACTIONS_3D
from value_iteration_3d import value_iteration

def visualize_3d(env: GridWorld3D, V=None, policy=None):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Draw all cells
    for x in range(env.depth):
        for y in range(env.height):
            for z in range(env.width):
                if (x, y, z) in env.walls:
                    ax.scatter(x, y, z, color='black', s=200, alpha=0.8, marker='s')
                elif (x, y, z) in env.rewards:
                    val = env.rewards[(x, y, z)]
                    color = 'red' if val > 0 else 'blue'
                    ax.scatter(x, y, z, color=color, s=200, alpha=0.9, marker='o')
                else:
                    if V and (x, y, z) in V:
                        val = V[(x, y, z)]
                        vmin, vmax = min(V.values()), max(V.values())
                        norm_val = (val - vmin) / (vmax - vmin + 1e-8)
                        color = plt.cm.viridis(norm_val)
                        ax.scatter(x, y, z, color=color, s=100, alpha=0.6)

    # Draw policy arrows (optional)
    if policy:
        for (x, y, z), action in policy.items():
            if (x, y, z) in env.walls or env.is_terminal((x, y, z)):
                continue
            dx, dy, dz = ACTIONS_3D[action]
            ax.quiver(x, y, z, dx*0.4, dy*0.4, dz*0.4, color='green', arrow_length_ratio=0.3)

    ax.set_xlabel('X (Depth)')
    ax.set_ylabel('Y (Height)')
    ax.set_zlabel('Z (Width)')
    ax.set_title('3D GridWorld with Value Iteration')
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    env = GridWorld3D(depth=4, height=4, width=4)
    
    # Add terminal states
    env.set_cell(3, 3, 3, REWARD)   # goal
    env.set_cell(1, 1, 1, PENALTY)  # pit
    env.set_cell(2, 2, 2, WALL)     # wall
    env.set_start(0, 0, 0)

    print("Running Value Iteration...")
    V, policy = value_iteration(env)

    print("Optimal policy at start:", policy.get(env.start_pos, "Terminal"))
    visualize_3d(env, V, policy)
