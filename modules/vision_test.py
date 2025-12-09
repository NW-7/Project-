import tkinter as tk
import random
from modules.database import save_result
from modules.config import COLORS
from modules.ui_utils import clear_window, create_centered_container, create_back_button

class VisionTest:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.username = app.username
        self.level = 1
        self.max_level = 6
        self.correct_answers = 0
        self.pixel = tk.PhotoImage(width=1, height=1)  # хак для квадратных кнопок
        self.letter_pairs = [('O', 'X'), ('O', 'Q'), ('O', 'D'),
                            ('B', '8'), ('I', 'l'), ('0', 'O')]
        self.create_interface()

    def create_interface(self):
        clear_window(self.root)
        self.container = create_centered_container(self.root)

        tk.Label(self.container, text="👁 Найди букву", font=("Arial", 36, "bold"),
                 bg=COLORS['bg'], fg=COLORS['text']).pack(pady=(0, 10))
        tk.Label(self.container, text="Найди отличающийся символ!",
                 font=("Arial", 18), bg=COLORS['bg'], fg=COLORS['text_dim']).pack(pady=(0, 15))

        self.level_label = tk.Label(self.container, text=f"Уровень {self.level}/{self.max_level}",
                                     font=("Arial", 20, "bold"), bg=COLORS['bg'], fg=COLORS['accent'])
        self.level_label.pack(pady=(0, 10))

        # контейнер сетки 600x600
        self.GRID_SIZE = 600
        self.grid_frame = tk.Frame(self.container, bg=COLORS['bg'],
                                    width=self.GRID_SIZE, height=self.GRID_SIZE)
        self.grid_frame.pack(pady=(0, 20))
        self.grid_frame.pack_propagate(False)

        create_back_button(self.root, self.back_to_menu)
        self.show_level()

    def show_level(self):
        if self.level > self.max_level:
            self.show_results()
            return

        for w in self.grid_frame.winfo_children():
            w.destroy()

        grid_dim = 4 + self.level
        self.level_label.config(text=f"Уровень {self.level}/{self.max_level}")
        main, diff = self.letter_pairs[self.level - 1]

        # расчет размеров кнопок
        gap = 4
        total_gaps = gap * (grid_dim - 1)
        btn_size = int((self.GRID_SIZE - total_gaps) / grid_dim)
        if (btn_size * grid_dim + total_gaps) > self.GRID_SIZE:
            btn_size -= 1

        font_size = int(btn_size * 0.5)
        total = grid_dim * grid_dim
        self.correct_pos = random.randint(0, total - 1)

        for i in range(total):
            row, col = i // grid_dim, i % grid_dim
            x_pos, y_pos = col * (btn_size + gap), row * (btn_size + gap)
            letter = diff if i == self.correct_pos else main

            btn = tk.Button(self.grid_frame, text=letter, image=self.pixel,
                           compound="center", width=btn_size, height=btn_size,
                           font=("Courier New", font_size, "bold"),
                           bg=COLORS['card'], fg=COLORS['text'],
                           relief=tk.FLAT, cursor="hand2", borderwidth=0,
                           command=lambda p=i: self.check(p))
            btn.place(x=x_pos, y=y_pos, width=btn_size, height=btn_size)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=COLORS['card_hover']))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg=COLORS['card']))

    def check(self, pos):
        if pos == self.correct_pos:
            self.correct_answers += 1
        self.level += 1
        self.show_level()

    def show_results(self):
        accuracy = (self.correct_answers / self.max_level) * 100
        save_result(self.username, "Найди букву", accuracy)

        clear_window(self.root)
        container = create_centered_container(self.root)

        tk.Label(container, text="✅ Тест завершён!", font=("Arial", 40, "bold"),
                 bg=COLORS['bg'], fg=COLORS['success']).pack(pady=(0, 40))

        results = tk.Frame(container, bg=COLORS['card'], width=600, height=300)
        results.pack_propagate(False)
        results.pack()

        inner = tk.Frame(results, bg=COLORS['card'])
        inner.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(inner, text=f"Точность: {accuracy:.0f}%",
                 font=("Arial", 24, "bold"), bg=COLORS['card'], fg=COLORS['accent']).pack(pady=15)

        create_back_button(self.root, self.back_to_menu)

    def back_to_menu(self):
        from modules.main_menu import MainMenu
        MainMenu(self.app)
