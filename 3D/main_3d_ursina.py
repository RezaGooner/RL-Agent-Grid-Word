# main_3d_ursina.py
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from grid_3d import GridWorld3D, WALL, REWARD, PENALTY
from value_iteration_3d import value_iteration

# تنظیمات محیط
app = Ursina()
window.title = '3D GridWorld RL'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False

# پارامترهای شبیه‌سازی
depth, height, width = 5, 5, 5
env = GridWorld3D(depth=depth, height=height, width=width)

# تنظیم محیط نمونه
env.set_cell(4, 4, 4, REWARD)
env.set_cell(2, 2, 2, PENALTY)
env.set_cell(1, 1, 1, WALL)
env.set_cell(3, 3, 3, WALL)
env.set_start(0, 0, 0)

# اجرای Value Iteration
print("Running Value Iteration...")
V, policy = value_iteration(env)
print(f"Optimal policy at start: {policy.get(env.start_pos, 'Terminal')}")

# ذخیره سیاست برای نمایش مسیر
agent_path = []
pos = env.start_pos
while pos in policy and not env.is_terminal(pos):
    agent_path.append(pos)
    pos = env.get_next_state(pos, policy[pos])
agent_path.append(pos)  # ترمینال

# رنگ‌ها
COLOR_EMPTY = color.gray
COLOR_WALL = color.black
COLOR_REWARD = color.green
COLOR_PENALTY = color.red
COLOR_AGENT = color.blue
COLOR_PATH = color.yellow

# ساخت مکعب‌ها
entities = []

for x in range(depth):
    for y in range(height):
        for z in range(width):
            pos_3d = (x, y, z)
            if pos_3d in env.walls:
                c = COLOR_WALL
            elif pos_3d in env.rewards:
                c = COLOR_REWARD if env.rewards[pos_3d] > 0 else COLOR_PENALTY
            else:
                c = COLOR_EMPTY

            # ایجاد مکعب (scale=0.9 برای فاصله بین مکعب‌ها)
            cube = Entity(
                model='cube',
                color=c,
                position=pos_3d,
                scale=0.9,
                collider='box'
            )
            entities.append(cube)

# نمایش مسیر
for p in agent_path:
    if p != env.start_pos and not env.is_terminal(p):
        Entity(
            model='cube',
            color=COLOR_PATH,
            position=p,
            scale=0.7
        )

# مکان عامل
agent_entity = Entity(
    model='cube',
    color=COLOR_AGENT,
    position=env.start_pos,
    scale=0.6
)

# دوربین آزاد (مثل بازی‌های سه‌بعدی)
player = FirstPersonController(
    position=(depth//2, height + 2, width//2 - 2),
    rotation=(0, 0, 0),
    speed=4
)
player.gravity = 0  # غیرفعال کردن گرانش برای حرکت آزاد

# نور
PointLight(parent=camera, position=(0, 10, -10))
AmbientLight(color=color.white * 0.7)

# توضیحات کنترل
Text(
    text="WASD: حرکت | ماوس: چرخش | Espace: بالا | Shift: پایین",
    origin=(0, 0),
    y=0.45,
    background=True
)

# اجرا
app.run()