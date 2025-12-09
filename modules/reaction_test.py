import tkinter as tk
import time
import random
from modules.database import save_result
from modules.config import COLORS
from modules.ui_utils import clear_window, create_centered_container, create_back_button

class ReactionTest:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.username = app.username
        self.start_time = None
        self.reaction_times = []
        self.round_number = 0
        self.max_rounds = 5
        self.waiting_for_green = False
        self.create_interface()

    def create_interface(self):
        clear_window(self.root)
        container = create_centered_container(self.root)

        tk.Label(container, text="⚡ Тест реакции", font=("Arial", 36, "bold"),
                 bg=COLORS['bg'], fg=COLORS['text']).pack(pady=(0, 10))
        tk.Label(container, text="Нажми ПРОБЕЛ, когда экран станет зелёным!",
                 font=("Arial", 18), bg=COLORS['bg'], fg=COLORS['text_dim']).pack(pady=(0, 40))

        # цветная область
        self.color_area = tk.Frame(container, bg=COLORS['card'], width=700, height=350,
                                    highlightthickness=3, highlightbackground=COLORS['card'])
        self.color_area.pack(pady=(0, 30))
        self.color_area.pack_propagate(False)

        self.status = tk.Label(self.color_area, text="Нажми START или ПРОБЕЛ",
                               font=("Arial", 28, "bold"), bg=COLORS['card'], fg=COLORS['text'])
        self.status.place(relx=0.5, rely=0.5, anchor='center')

        # кнопка старта
        self.btn = tk.Button(container, text="START", command=self.start_round,
                            font=("Arial", 24, "bold"), bg=COLORS['accent'], fg='white',
                            width=30, height=2, relief=tk.FLAT, cursor="hand2", borderwidth=0)
        self.btn.pack()

        create_back_button(self.root, self.back_to_menu)
        self.root.bind('<space>', self.on_space)

    def on_space(self, event):
        if self.btn['state'] != tk.DISABLED:
            if self.waiting_for_green:
                self.record_time()
            else:
                self.start_round()

    def start_round(self):
        if self.round_number >= self.max_rounds:
            self.show_results()
            return

        self.btn.config(state=tk.DISABLED, bg=COLORS['card'])
        self.color_area.config(bg=COLORS['error'], highlightbackground=COLORS['error'])
        self.status.config(text="Жди...", bg=COLORS['error'], fg='white')
        self.waiting_for_green = False

        delay = random.uniform(1.5, 3.8)
        self.root.after(int(delay * 1000), self.show_green)

    def show_green(self):
        self.color_area.config(bg=COLORS['success'], highlightbackground=COLORS['success'])
        self.status.config(text="НАЖМИ ПРОБЕЛ!", bg=COLORS['success'], fg='white')
        self.start_time = time.time()
        self.waiting_for_green = True
        self.btn.config(state=tk.NORMAL, text="КЛИК!", command=self.record_time,
                        bg=COLORS['success'], fg='white')

    def record_time(self):
        if not self.start_time or not self.waiting_for_green:
            return

        reaction_time = (time.time() - self.start_time) * 1000
        self.reaction_times.append(reaction_time)
        self.round_number += 1
        self.waiting_for_green = False

        self.color_area.config(bg=COLORS['card'], highlightbackground=COLORS['card'])
        self.status.config(text=f"Раунд {self.round_number}: {reaction_time:.0f} мс",
                          bg=COLORS['card'], fg=COLORS['text'])
        self.start_time = None

        btn_text = f"Раунд {self.round_number + 1}/{self.max_rounds}" if self.round_number < self.max_rounds else "Результаты"
        self.btn.config(text=btn_text, command=self.start_round,
                        bg=COLORS['accent'], fg='white')

    def show_results(self):
        avg = sum(self.reaction_times) / len(self.reaction_times)
        best = min(self.reaction_times)
        save_result(self.username, "Тест реакции", avg)

        self.root.unbind('<space>')
        clear_window(self.root)
        container = create_centered_container(self.root)

        tk.Label(container, text="✅ Тест завершён!", font=("Arial", 40, "bold"),
                 bg=COLORS['bg'], fg=COLORS['success']).pack(pady=(0, 40))

        results = tk.Frame(container, bg=COLORS['card'], width=600, height=300)
        results.pack_propagate(False)
        results.pack(pady=20)

        inner = tk.Frame(results, bg=COLORS['card'])
        inner.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(inner, text=f"Средняя реакция: {avg:.0f} мс",
                 font=("Arial", 24), bg=COLORS['card'], fg=COLORS['text']).pack(pady=15)
        tk.Label(inner, text=f"Лучшее время: {best:.0f} мс",
                 font=("Arial", 24), bg=COLORS['card'], fg=COLORS['text']).pack(pady=15)

        rating = "Невероятно! 🏆" if avg < 250 else "Отлично! 👍" if avg < 350 else "Хорошо! 💪"
        tk.Label(inner, text=rating, font=("Arial", 28, "bold"),
                 bg=COLORS['card'], fg=COLORS['success']).pack(pady=20)

        create_back_button(self.root, self.back_to_menu)

    def back_to_menu(self):
        self.root.unbind('<space>')
        from modules.main_menu import MainMenu
        MainMenu(self.app)
