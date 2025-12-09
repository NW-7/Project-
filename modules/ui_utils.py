import tkinter as tk
from modules.config import COLORS

def clear_window(root):
    """очистка всех виджетов"""
    for w in root.winfo_children():
        w.destroy()
    root.configure(bg=COLORS['bg'])

def create_centered_container(root):
    """центрированный контейнер"""
    container = tk.Frame(root, bg=COLORS['bg'])
    container.place(relx=0.5, rely=0.5, anchor='center')
    return container

def create_title(parent, text, subtitle=None):
    """заголовок с подзаголовком"""
    tk.Label(parent, text=text, font=("Arial", 36, "bold"),
             bg=COLORS['bg'], fg=COLORS['text']).pack(pady=(0, 10))
    if subtitle:
        tk.Label(parent, text=subtitle, font=("Arial", 18),
                 bg=COLORS['bg'], fg=COLORS['text_dim']).pack(pady=(0, 30))

def create_back_button(root, command):
    """кнопка возврата в меню"""
    btn = tk.Button(root, text="← Назад в меню", command=command,
                    font=("Arial", 16, "bold"), bg=COLORS['card'],
                    fg=COLORS['text'], width=25, relief=tk.FLAT,
                    cursor="hand2", padx=30, pady=15, borderwidth=0)
    btn.place(relx=0.5, rely=0.95, anchor='center')
    return btn

def add_hover(widget, normal_bg, hover_bg):
    """эффект hover для виджета"""
    widget.bind('<Enter>', lambda e: widget.config(bg=hover_bg))
    widget.bind('<Leave>', lambda e: widget.config(bg=normal_bg))
