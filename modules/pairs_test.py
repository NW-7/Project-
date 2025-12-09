import tkinter as tk
import random
import time
from modules.database import save_result
from modules.config import COLORS

class PairsTest:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.username = app.username
        self.emojis = ['🍎', '🍌', '🍊', '🍇', '🍓', '🍒', '🥝', '🍑']
        self.cards = []
        self.card_buttons = []
        self.opened = []
        self.matched = []
        self.moves = 0
        self.start_time = None
        self.is_checking = False
        self.create_interface()

    def create_interface(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.root.configure(bg=COLORS['bg'])

        header = tk.Frame(self.root, bg=COLORS['bg'], height=130)
        header.pack(fill=tk.X, padx=55, pady=35)
        header.pack_propagate(False)

        tk.Label(header, text="🎮 Найди пару", font=("Arial", 30, "bold"),
                 bg=COLORS['bg'], fg=COLORS['text']).pack(anchor='w')
        tk.Label(header, text="Открывай карточки и ищи одинаковые пары!",
                 font=("Arial", 15), bg=COLORS['bg'], fg=COLORS['text_dim']).pack(anchor='w', pady=(12, 0))

        center = tk.Frame(self.root, bg=COLORS['bg'])
        center.pack(expand=True, fill=tk.BOTH, padx=55, pady=(0, 35))

        self.moves_label = tk.Label(center, text="Ходов: 0", font=("Arial", 17, "bold"),
                                     bg=COLORS['bg'], fg=COLORS['accent'])
        self.moves_label.pack(pady=(0, 25))

        # сетка 4x4
        grid = tk.Frame(center, bg=COLORS['bg'])
        grid.pack(pady=(0, 25))

        self.cards = self.emojis * 2
        random.shuffle(self.cards)
        self.card_buttons = []

        for i in range(16):
            btn = tk.Button(grid, text="?", font=("Arial", 36, "bold"),
                           bg=COLORS['closed'], fg=COLORS['text'],
                           width=4, height=2, relief=tk.FLAT, cursor="hand2",
                           borderwidth=0, command=lambda idx=i: self.flip_card(idx))
            btn.grid(row=i//4, column=i%4, padx=8, pady=8)
            self.card_buttons.append(btn)

            btn.bind('<Enter>', lambda e, b=btn, idx=i: self.on_hover_enter(b, idx))
            btn.bind('<Leave>', lambda e, b=btn, idx=i: self.on_hover_leave(b, idx))

        back = tk.Button(center, text="← Назад в меню", command=self.back_to_menu,
                        font=("Arial", 14), bg=COLORS['card'], fg=COLORS['text_dim'],
                        relief=tk.FLAT, cursor="hand2", padx=25, pady=14, borderwidth=0)
        back.pack()

        self.start_time = time.time()

    def on_hover_enter(self, btn, idx):
        if idx not in self.matched and idx not in self.opened and not self.is_checking:
            btn.config(bg=COLORS['card_hover'])

    def on_hover_leave(self, btn, idx):
        if idx in self.matched:
            btn.config(bg=COLORS['success'])
        elif idx in self.opened:
            btn.config(bg=COLORS['card'])
        else:
            btn.config(bg=COLORS['closed'])

    def flip_card(self, idx):
        if self.is_checking or idx in self.opened or idx in self.matched or len(self.opened) >= 2:
            return

        self.card_buttons[idx].config(text=self.cards[idx], bg=COLORS['card'])
        self.opened.append(idx)

        if len(self.opened) == 2:
            self.is_checking = True
            self.moves += 1
            self.moves_label.config(text=f"Ходов: {self.moves}")
            self.root.after(500, self.check_match)

    def check_match(self):
        idx1, idx2 = self.opened

        if self.cards[idx1] == self.cards[idx2]:
            self.matched.extend([idx1, idx2])
            self.card_buttons[idx1].config(bg=COLORS['success'], state=tk.DISABLED,
                                          disabledforeground=COLORS['text'])
            self.card_buttons[idx2].config(bg=COLORS['success'], state=tk.DISABLED,
                                          disabledforeground=COLORS['text'])
            self.opened = []
            self.is_checking = False

            if len(self.matched) == 16:
                self.root.after(500, self.show_results)
        else:
            self.root.after(1000, self.close_cards)

    def close_cards(self):
        for idx in self.opened:
            self.card_buttons[idx].config(text="?", bg=COLORS['closed'])
        self.opened = []
        self.is_checking = False

    def show_results(self):
        elapsed = time.time() - self.start_time
        score = max(0, 1000 - self.moves * 10 - int(elapsed))
        save_result(self.username, "Найди пару", score)

        for w in self.root.winfo_children():
            w.destroy()
        self.root.configure(bg=COLORS['bg'])

        tk.Label(self.root, text="✅ Тест завершён!", font=("Arial", 34, "bold"),
                 bg=COLORS['bg'], fg=COLORS['success']).pack(pady=55)

        results = tk.Frame(self.root, bg=COLORS['card'],
                          highlightthickness=2, highlightbackground=COLORS['card'])
        results.pack(padx=110, pady=25, fill=tk.BOTH, expand=True)

        inner = tk.Frame(results, bg=COLORS['card'])
        inner.pack(expand=True, padx=45, pady=45)

        tk.Label(inner, text=f"Ходов: {self.moves}", font=("Arial", 21),
                 bg=COLORS['card'], fg=COLORS['text']).pack(pady=18)
        tk.Label(inner, text=f"Время: {int(elapsed)} сек", font=("Arial", 21),
                 bg=COLORS['card'], fg=COLORS['text']).pack(pady=18)
        tk.Label(inner, text=f"Счёт: {score}", font=("Arial", 21, "bold"),
                 bg=COLORS['card'], fg=COLORS['accent']).pack(pady=18)

        rating = "Феноменально! 🏆" if self.moves <= 12 else "Отлично! 👍" if self.moves <= 18 else "Хорошо! 💪"
        tk.Label(inner, text=rating, font=("Arial", 25, "bold"),
                 bg=COLORS['card'], fg=COLORS['success']).pack(pady=22)

        btn = tk.Button(self.root, text="← Вернуться в меню", command=self.back_to_menu,
                       font=("Arial", 15, "bold"), bg=COLORS['accent'], fg='white',
                       relief=tk.FLAT, cursor="hand2", padx=45, pady=17, borderwidth=0)
        btn.pack(pady=35)

    def back_to_menu(self):
        from modules.main_menu import MainMenu
        MainMenu(self.app)
