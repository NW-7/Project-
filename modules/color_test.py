import tkinter as tk
import random
from modules.database import save_result
from modules.config import COLORS

class ColorTest:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.username = app.username
        self.correct_answers = 0
        self.total_questions = 8
        self.question_number = 0
        self.grid_size = 3
        self.create_interface()

    def create_interface(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.root.configure(bg=COLORS['bg'])

        tk.Label(self.root, text="🌈 Тест цветовосприятия", font=("Arial", 24, "bold"),
                 bg=COLORS['bg'], fg=COLORS['text']).pack(pady=30)
        tk.Label(self.root, text="Найди квадрат отличающегося оттенка!",
                 font=("Arial", 12), bg=COLORS['bg'], fg=COLORS['text_dim']).pack(pady=10)

        self.question_label = tk.Label(self.root, text=f"Вопрос: 0/{self.total_questions}",
                                       font=("Arial", 11), bg=COLORS['bg'], fg=COLORS['text_dim'])
        self.question_label.pack(pady=5)

        self.grid_frame = tk.Frame(self.root, bg=COLORS['bg'])
        self.grid_frame.pack(pady=40)

        btn_back = tk.Button(self.root, text="← Назад в меню", command=self.back_to_menu,
                            font=("Arial", 11), bg=COLORS['card'], fg=COLORS['text_dim'],
                            relief=tk.FLAT, cursor="hand2", padx=15, pady=8)
        btn_back.pack(pady=20)

        self.show_question()

    def show_question(self):
        self.question_number += 1

        if self.question_number > self.total_questions:
            self.show_results()
            return

        self.question_label.config(text=f"Вопрос: {self.question_number}/{self.total_questions}")

        for w in self.grid_frame.winfo_children():
            w.destroy()

        # увеличиваем сложность
        if self.question_number > 4:
            self.grid_size = 4
        if self.question_number > 6:
            self.grid_size = 5

        # генерация цветов
        base_r, base_g, base_b = random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)
        diff = max(15, 40 - (self.question_number * 3))

        diff_r = min(255, max(0, base_r + random.choice([-diff, diff])))
        diff_g = min(255, max(0, base_g + random.choice([-diff, diff])))
        diff_b = min(255, max(0, base_b + random.choice([-diff, diff])))

        base_color = f'#{base_r:02x}{base_g:02x}{base_b:02x}'
        diff_color = f'#{diff_r:02x}{diff_g:02x}{diff_b:02x}'

        different_pos = random.randint(0, self.grid_size * self.grid_size - 1)
        self.correct_answer = different_pos

        for i in range(self.grid_size * self.grid_size):
            color = diff_color if i == different_pos else base_color
            btn = tk.Button(self.grid_frame, bg=color, width=8, height=4,
                           relief=tk.FLAT, cursor="hand2",
                           command=lambda idx=i: self.check_answer(idx))
            btn.grid(row=i//self.grid_size, column=i%self.grid_size, padx=2, pady=2)

    def check_answer(self, selected):
        if selected == self.correct_answer:
            self.correct_answers += 1
        self.show_question()

    def show_results(self):
        accuracy = (self.correct_answers / self.total_questions) * 100
        save_result(self.username, "Тест цветов", accuracy)

        for w in self.root.winfo_children():
            w.destroy()
        self.root.configure(bg=COLORS['bg'])

        tk.Label(self.root, text="✅ Тест завершён!", font=("Arial", 24, "bold"),
                 bg=COLORS['bg'], fg=COLORS['success']).pack(pady=40)

        results_frame = tk.Frame(self.root, bg=COLORS['card'], relief=tk.FLAT)
        results_frame.pack(pady=20, padx=80, fill=tk.BOTH, expand=True)

        tk.Label(results_frame, text=f"Правильных ответов: {self.correct_answers}/{self.total_questions}",
                 font=("Arial", 16), bg=COLORS['card'], fg=COLORS['text']).pack(pady=15)
        tk.Label(results_frame, text=f"Точность: {accuracy:.0f}%",
                 font=("Arial", 16), bg=COLORS['card'], fg=COLORS['text']).pack(pady=15)

        rating = "Превосходное зрение! 🌈" if accuracy >= 90 else "Отличное восприятие! 👍" if accuracy >= 70 else "Хорошая попытка! 💪"
        tk.Label(results_frame, text=rating, font=("Arial", 18, "bold"),
                 bg=COLORS['card'], fg=COLORS['test6']).pack(pady=15)

        tk.Button(self.root, text="← Вернуться в меню", command=self.back_to_menu,
                 width=25, height=2, font=("Arial", 12, "bold"),
                 bg=COLORS['accent'], fg=COLORS['text'], relief=tk.FLAT, cursor="hand2").pack(pady=30)

    def back_to_menu(self):
        from modules.main_menu import MainMenu
        MainMenu(self.app)
