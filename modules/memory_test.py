import tkinter as tk
import random
from modules.database import save_result
from modules.config import COLORS

class MemoryTest:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.username = app.username
        self.level = 1
        self.max_level = 8
        self.sequence = []
        self.user_sequence = []
        self.score = 0
        # цвета плиток
        self.tile_colors = [
            (COLORS['tile1'], COLORS['glow1']), (COLORS['tile2'], COLORS['glow2']),
            (COLORS['tile3'], COLORS['glow3']), (COLORS['tile4'], COLORS['glow4']),
            (COLORS['tile5'], COLORS['glow5']), (COLORS['tile6'], COLORS['glow6'])
        ]
        self.create_interface()

    def create_interface(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.root.configure(bg=COLORS['bg'])

        header = tk.Frame(self.root, bg=COLORS['bg'], height=130)
        header.pack(fill=tk.X, padx=55, pady=35)
        header.pack_propagate(False)

        tk.Label(header, text="🧠 Тест памяти", font=("Arial", 30, "bold"),
                 bg=COLORS['bg'], fg=COLORS['text']).pack(anchor='w')
        tk.Label(header, text="Запомни последовательность цветов и повтори!",
                 font=("Arial", 15), bg=COLORS['bg'], fg=COLORS['text_dim']).pack(anchor='w', pady=(12, 0))

        center = tk.Frame(self.root, bg=COLORS['bg'])
        center.pack(expand=True, fill=tk.BOTH, padx=55, pady=(0, 35))

        self.level_label = tk.Label(center, text=f"Уровень {self.level}",
                                     font=("Arial", 18, "bold"), bg=COLORS['bg'], fg=COLORS['accent'])
        self.level_label.pack(pady=(0, 30))

        # плитки 3x2
        tiles_frame = tk.Frame(center, bg=COLORS['bg'])
        tiles_frame.pack(pady=(0, 35))
        self.tiles = []

        for i in range(6):
            row, col = i // 3, i % 3
            tile = tk.Button(tiles_frame, bg=self.tile_colors[i][0],
                            activebackground=self.tile_colors[i][1],
                            width=12, height=6, relief=tk.FLAT, cursor="hand2",
                            borderwidth=0, state=tk.DISABLED,
                            command=lambda idx=i: self.on_tile_click(idx))
            tile.grid(row=row, column=col, padx=12, pady=12)
            self.tiles.append(tile)

        self.start_btn = tk.Button(center, text="Начать уровень", command=self.start_level,
                                   font=("Arial", 17, "bold"), bg=COLORS['accent'], fg='white',
                                   relief=tk.FLAT, cursor="hand2", padx=40, pady=15, borderwidth=0)
        self.start_btn.pack(pady=(0, 20))

        back = tk.Button(center, text="← Назад в меню", command=self.back_to_menu,
                        font=("Arial", 14), bg=COLORS['card'], fg=COLORS['text_dim'],
                        relief=tk.FLAT, cursor="hand2", padx=25, pady=14, borderwidth=0)
        back.pack()

    def start_level(self):
        self.start_btn.config(state=tk.DISABLED)
        self.user_sequence = []
        seq_length = 2 + self.level
        options = range(0, 5)
        self.sequence = []

        for _ in range(seq_length):
            choice = random.choice(options)
            while self.sequence and choice == self.sequence[-1]:
                choice = random.choice(options)
            self.sequence.append(choice)

        self.show_sequence()

    def show_sequence(self):
        for tile in self.tiles:
            tile.config(state=tk.DISABLED)

        def flash(index, delay):
            if index < len(self.sequence):
                tile_idx = self.sequence[index]
                tile = self.tiles[tile_idx]
                normal_color = self.tile_colors[tile_idx][0]
                glow_color = self.tile_colors[tile_idx][1]
                tile.config(bg=glow_color)

                def restore():
                    tile.config(bg=normal_color)
                    flash(index + 1, delay)

                self.root.after(400, restore)
            else:
                self.root.after(delay, self.enable_input)

        flash(0, 600)

    def enable_input(self):
        for tile in self.tiles:
            tile.config(state=tk.NORMAL)

    def on_tile_click(self, idx):
        self.user_sequence.append(idx)

        if self.user_sequence[-1] != self.sequence[len(self.user_sequence) - 1]:
            self.game_over()
            return

        if len(self.user_sequence) == len(self.sequence):
            self.score += self.level * 10
            self.level += 1

            if self.level > self.max_level:
                self.show_results()
            else:
                self.level_label.config(text=f"Уровень {self.level}")
                for tile in self.tiles:
                    tile.config(state=tk.DISABLED)
                self.start_btn.config(state=tk.NORMAL, text="Следующий уровень")

    def game_over(self):
        for tile in self.tiles:
            tile.config(state=tk.DISABLED)
        self.show_results()

    def show_results(self):
        save_result(self.username, "Тест памяти", self.score)

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

        tk.Label(inner, text=f"Достигнутый уровень: {self.level - 1}",
                 font=("Arial", 21), bg=COLORS['card'], fg=COLORS['text']).pack(pady=18)
        tk.Label(inner, text=f"Итоговый счёт: {self.score}",
                 font=("Arial", 21), bg=COLORS['card'], fg=COLORS['text']).pack(pady=18)

        rating = "Феноменально! 🧠" if self.level > 6 else "Отлично! 👍" if self.level > 4 else "Хорошо! 💪"
        tk.Label(inner, text=rating, font=("Arial", 25, "bold"),
                 bg=COLORS['card'], fg=COLORS['accent']).pack(pady=22)

        btn = tk.Button(self.root, text="← Вернуться в меню", command=self.back_to_menu,
                       font=("Arial", 15, "bold"), bg=COLORS['accent'], fg='white',
                       relief=tk.FLAT, cursor="hand2", padx=45, pady=17, borderwidth=0)
        btn.pack(pady=35)

    def back_to_menu(self):
        from modules.main_menu import MainMenu
        MainMenu(self.app)
