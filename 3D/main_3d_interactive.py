from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

try:
    from core.grid_3d import GridWorld3D, WALL, REWARD, PENALTY
    from core.value_iteration_3d import value_iteration
except ImportError:
    print("Error: core modules not found. Ensure grid_3d.py and value_iteration_3d.py are in 'core' folder.")

app = Ursina(title="3D RL Editor - Value on Floor")
window.borderless = False
window.size = (1100, 700)

env = GridWorld3D(depth=4, height=1, width=4)
V = {}
entities = []
text_labels = []
agent_model = None
edit_mode = 'wall'
show_values = False
reward_val = 1.0
penalty_val = -1.0
ASSETS_DIR = 'assets/'

player = FirstPersonController(position=(2, 3, -5), speed=5)
player.gravity = 0
mouse.locked = True

is_right_mouse_held = False
mouse_sensitivity = 100

def toggle_mouse_lock():
    mouse.locked = not mouse.locked
    player.enabled = mouse.locked

def refresh_grid():
    global entities, text_labels, agent_model
    
    for e in entities: destroy(e)
    for t in text_labels: destroy(t)
    if agent_model: destroy(agent_model)
    
    entities.clear()
    text_labels.clear()
    
    for x in range(env.depth):
        for y in range(env.height):
            for z in range(env.width):
                pos_3d = (x, y, z)
                
                base_color = color.gray
                if pos_3d == env.start_pos:
                    base_color = color.azure.tint(0.3)
                
                floor = Button(parent=scene, model='cube', color=base_color, position=pos_3d,
                               scale=(0.95, 0.11, 0.95), collider='box')
                floor.on_click = Func(handle_click, pos_3d)
                entities.append(floor)
                
                if pos_3d in env.walls:
                    wall = Entity(model='cube', color=color.red, position=pos_3d,
                                  scale=(1.0, 0.4, 1.0))
                    entities.append(wall)
                
                elif pos_3d in env.rewards:
                    val = env.rewards[pos_3d]
                    try:
                        if val > 0:  
                            asset = Entity(model=ASSETS_DIR+'12212_Bird_v1_l2.obj',
                                           texture=ASSETS_DIR+'12212_Bird_diffuse.jpg',
                                           position=pos_3d + (0, 0.35, 0), scale=0.08,
                                           rotation=(-90, 0, 0))
                        else:  
                            asset = Entity(model=ASSETS_DIR+'13466_Canaan_Dog_v1_L3.obj',
                                           texture=ASSETS_DIR+'13466_Canaan_Dog_diff.jpg',
                                           position=pos_3d + (0, 0.15, 0), scale=0.03,
                                           rotation=(-90, 0, 90))
                        entities.append(asset)
                    except Exception as e:
                        print(f"Asset load error: {e}")
                        entities.append(Entity(model='sphere', color=color.orange, position=pos_3d + (0, 0.4, 0), scale=0.4))
                
                if show_values and pos_3d not in env.walls:
                    value = V.get(pos_3d, 0.0)
                    value_text = f"{value:.2f}"
                    
                    if value > 0.01:
                        txt_color = color.lime
                    elif value < -0.01:
                        txt_color = color.red
                    else:
                        txt_color = color.white
                    
                    value_label = Text(
                        text=value_text,
                        parent=floor,
                        position=(0, 0.06, 0),
                        origin=(0, 0),
                        scale=4.0,
                        billboard=True,
                        color=txt_color,
                        background=False
                    )
                    text_labels.append(value_label)
    
    try:
        agent_model = Entity(model=ASSETS_DIR+'12221_Cat_v1_l3.obj',
                             texture=ASSETS_DIR+'Cat_diffuse.jpg',
                             position=env.start_pos,
                             scale=0.02, rotation=(-90, 0, 0))
    except:
        agent_model = Entity(model='sphere', color=color.cyan, position=env.start_pos + (0, 0.4, 0), scale=0.4)

def handle_click(pos):
    if edit_mode == 'wall':
        env.set_cell(*pos, WALL)
    elif edit_mode == 'reward':
        env.rewards[pos] = reward_val
    elif edit_mode == 'penalty':
        env.rewards[pos] = penalty_val
    elif edit_mode == 'start':
        env.set_start(*pos)
    elif edit_mode == 'delete':
        env.walls.discard(pos)
        env.rewards.pop(pos, None)
    refresh_grid()

def open_value_settings():
    r_in = InputField(default_value=str(reward_val))
    p_in = InputField(default_value=str(penalty_val))
    win = WindowPanel(title='Value Settings', content=(Text('Reward:'), r_in, Text('Penalty:'), p_in))
    def apply():
        global reward_val, penalty_val
        reward_val = float(r_in.text)
        penalty_val = float(p_in.text)
        for p in list(env.rewards):
            if env.rewards[p] > 0: env.rewards[p] = reward_val
            else: env.rewards[p] = penalty_val
        destroy(win)
        refresh_grid()
    Button(parent=win, text='Apply', y=-0.2, on_click=apply)

def open_dim_settings():
    d_in = InputField(default_value=str(env.depth))
    h_in = InputField(default_value=str(env.height))
    w_in = InputField(default_value=str(env.width))
    win = WindowPanel(title='Grid Size', content=(Text('Depth:'), d_in, Text('Height:'), h_in, Text('Width:'), w_in))
    def apply():
        global env, V
        env = GridWorld3D(int(d_in.text), int(h_in.text), int(w_in.text))
        V = {}
        destroy(win)
        refresh_grid()
    Button(parent=win, text='Update', y=-0.25, on_click=apply)

def input(key):
    global edit_mode, show_values, is_right_mouse_held
    
    if key == 'right mouse down':
        is_right_mouse_held = True
        mouse.visible = False
        player.enabled = False
    if key == 'right mouse up':
        is_right_mouse_held = False
        mouse.visible = True
        player.enabled = True
    
    if is_right_mouse_held:
        dx = mouse.velocity.x * time.dt * mouse_sensitivity
        dy = mouse.velocity.y * time.dt * mouse_sensitivity
        camera.rotation_x = clamp(camera.rotation_x - dy, -89, 89)
        camera.rotation_y += dx
        return
    
    if key in '12345':
        edit_mode = ['wall', 'reward', 'penalty', 'start', 'delete'][int(key)-1]
    elif key == 'z': open_value_settings()
    elif key == 'x': open_dim_settings()
    elif key == 'v':
        show_values = not show_values
        refresh_grid()
    elif key == 'enter':
        print("Running Value Iteration...")
        global V
        V, _ = value_iteration(env)
        refresh_grid()
    elif key == 'e': toggle_mouse_lock()
    elif key == 'scroll up': camera.fov = max(20, camera.fov - 10)
    elif key == 'scroll down': camera.fov = min(120, camera.fov + 10)

DirectionalLight(y=8, rotation=(60, -45, 45))
AmbientLight(color=color.rgba(100, 100, 120, 255))

Text(text="1:Wall  2:Reward  3:Penalty  4:Start  5:Delete   |   Z:Values  X:Size  V:Show Values  Enter:Run VI  E:Mouse Lock",
     position=(-0.85, 0.46), scale=1.5, background=True, color=color.yellow)

refresh_grid()
app.run()
