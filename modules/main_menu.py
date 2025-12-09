import tkinter as tk
from modules.config import COLORS

class MainMenu:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.username = app.username
        self.create_menu()

    def create_menu(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.root.configure(bg=COLORS['bg'])

        main_container = tk.Frame(self.root, bg=COLORS['bg'])
        main_container.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(main_container, text=f"Привет, {self.username}! 👋",
                 font=("Arial", 32, "bold"), bg=COLORS['bg'], fg=COLORS['text']).pack(pady=(0, 10))
        tk.Label(main_container, text="Выбери тест для проверки своих способностей",
                 font=("Arial", 16), bg=COLORS['bg'], fg=COLORS['text_dim']).pack(pady=(0, 50))

        # карточки 3x2
        cards = tk.Frame(main_container, bg=COLORS['bg'])
        cards.pack(pady=(0, 40))

        tests = [
            {'icon': '⚡', 'name': 'Реакция', 'desc': 'Скорость',
             'color': COLORS['test1'], 'cmd': self.start_reaction},
            {'icon': '👁', 'name': 'Найди букву', 'desc': 'Зрение',
             'color': COLORS['test2'], 'cmd': self.start_vision},
            {'icon': '🔊', 'name': 'Слух', 'desc': 'Тоны',
             'color': COLORS['test3'], 'cmd': self.start_hearing},
            {'icon': '🧠', 'name': 'Память', 'desc': 'Последовательность',
             'color': COLORS['test4'], 'cmd': self.start_memory},
            {'icon': '🎮', 'name': 'Найди пару', 'desc': 'Memory',
             'color': COLORS['test5'], 'cmd': self.start_pairs},
            {'icon': '🌈', 'name': 'Цвета', 'desc': 'Оттенки',
             'color': COLORS['test6'], 'cmd': self.start_color}
        ]

        for i, test in enumerate(tests):
            card = self.create_card(cards, test)
            card.grid(row=i//3, column=i%3, padx=20, pady=20)

        # нижние кнопки
        btns = tk.Frame(main_container, bg=COLORS['bg'])
        btns.pack()

        self.create_btn(btns, "🏆 Лидеры", self.show_leaderboard).pack(side=tk.LEFT, padx=15)
        self.create_btn(btns, "📊 Результаты", self.show_results).pack(side=tk.LEFT, padx=15)

    def create_card(self, parent, test):
        card = tk.Frame(parent, bg=COLORS['card'], cursor='hand2',
                       width=200, height=200, highlightthickness=2,
                       highlightbackground=COLORS['border'])
        card.pack_propagate(False)

        icon = tk.Label(card, text=test['icon'], font=("Arial", 55),
                       bg=COLORS['card'], fg=test['color'])
        icon.pack(pady=(30, 15))

        name = tk.Label(card, text=test['name'], font=("Arial", 18, "bold"),
                       bg=COLORS['card'], fg=COLORS['text'])
        name.pack(pady=(0, 5))

        desc = tk.Label(card, text=test['desc'], font=("Arial", 12),
                       bg=COLORS['card'], fg=COLORS['text_dim'])
        desc.pack()

        # события hover и клик
        for w in [card, icon, name, desc]:
            w.bind('<Button-1>', lambda e, c=test['cmd']: c())
            w.bind('<Enter>', lambda e, ca=card, i=icon, n=name, d=desc: 
                   [x.config(bg=COLORS['card_hover']) for x in [ca, i, n, d]])
            w.bind('<Leave>', lambda e, ca=card, i=icon, n=name, d=desc: 
                   [x.config(bg=COLORS['card']) for x in [ca, i, n, d]])

        return card

    def create_btn(self, parent, text, cmd):
        btn = tk.Button(parent, text=text, command=cmd, font=("Arial", 16, "bold"),
                       bg=COLORS['card'], fg=COLORS['text'], relief=tk.FLAT,
                       cursor="hand2", padx=40, pady=18, borderwidth=0)
        btn.bind('<Enter>', lambda e: btn.config(bg=COLORS['card_hover']))
        btn.bind('<Leave>', lambda e: btn.config(bg=COLORS['card']))
        return btn

    def start_reaction(self):
        from modules.reaction_test import ReactionTest
        ReactionTest(self.app)

    def start_vision(self):
        from modules.vision_test import VisionTest
        VisionTest(self.app)

    def start_hearing(self):
        from modules.hearing_test import HearingTest
        HearingTest(self.app)

    def start_memory(self):
        from modules.memory_test import MemoryTest
        MemoryTest(self.app)

    def start_pairs(self):
        from modules.pairs_test import PairsTest
        PairsTest(self.app)

    def start_color(self):
        from modules.color_test import ColorTest
        ColorTest(self.app)

    def show_leaderboard(self):
        from modules.database import show_leaderboard
        show_leaderboard(self.app)

    def show_results(self):
        from modules.database import show_user_results
        show_user_results(self.app)
