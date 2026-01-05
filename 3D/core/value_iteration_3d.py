# core/value_iteration_3d.py - نسخه بهینه‌شده کاربر

from core.grid_3d import GridWorld3D
from typing import Dict, Tuple
import numpy as np

GAMMA = 0.9
THETA = 1e-4  # کمی کاهش داده شده برای سرعت بیشتر

def value_iteration(env: GridWorld3D) -> Tuple[Dict[Tuple, float], Dict[Tuple, str]]:
    # پیش‌تخصیص آرایه‌های numpy برای سرعت بیشتر
    states = env.get_all_states()
    V = {s: 0.0 for s in states}
    policy = {}
    
    iteration = 0
    max_iterations = 1000  # جلوگیری از حلقه بی‌پایان
    
    # بهینه‌سازی: پیش‌محاسبه عملیات‌های مکرر
    terminal_states = {s for s in states if env.is_terminal(s)}
    non_terminal_states = [s for s in states if not env.is_terminal(s)]
    
    while iteration < max_iterations:
        delta = 0
        # پردازش حالت‌های ترمینال به صورت جداگانه
        for s in terminal_states:
            V[s] = env.get_reward(s)
        
        # پردازش حالت‌های غیرترمینال
        for s in non_terminal_states:
            v_old = V[s]
            action_values = []
            
            # بهینه‌سازی: استفاده از لیست و max به جای دیکشنری
            for a in env.get_actions(s):
                next_s = env.get_next_state(s, a)
                reward = env.get_reward(s)
                action_values.append(reward + GAMMA * V[next_s])
            
            if action_values:
                V[s] = max(action_values)
                # پیدا کردن عمل با بیشترین مقدار
                best_action_idx = np.argmax(action_values)
                policy[s] = env.get_actions(s)[best_action_idx]
            else:
                V[s] = env.get_reward(s)
            
            delta = max(delta, abs(v_old - V[s]))
        
        iteration += 1
        if delta < THETA:
            break
    
    return V, policy
