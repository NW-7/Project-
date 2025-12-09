import tkinter as tk
import random
import numpy as np
import pygame
import wave
import tempfile
import os
from modules.database import save_result
from modules.config import COLORS

class HearingTest:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.username = app.username
        self.round = 1
        self.max_rounds = 4
        self.correct_answers = 0
        self.frequencies = []
        self.target_index = None
        self.is_playing = False
        self.temp_files = []
        self.frequency_diffs = [150, 100, 60, 30]

        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
        except Exception as e:
            print(f"ошибка pygame: {e}")

        self.build_ui()

    def build_ui(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.root.configure(bg=COLORS['bg'])

        self.container = tk.Frame(self.root, bg=COLORS['bg'])
        self.container.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(self.container, text="🔊 Тест слуха", font=("Arial", 36, "bold"),
                 bg=COLORS['bg'], fg=COLORS['text']).pack(pady=(0, 10))
        tk.Label(self.container, text="Послушай два тона и выбери, какой выше",
                 font=("Arial", 18), bg=COLORS['bg'], fg=COLORS['text_dim']).pack(pady=(0, 30))

        self.level_label = tk.Label(self.container, text=f"Раунд {self.round}/{self.max_rounds}",
                                     font=("Arial", 20, "bold"), bg=COLORS['bg'], fg=COLORS['accent'])
        self.level_label.pack(pady=(0, 20))

        diff = self.frequency_diffs[self.round - 1]
        difficulty = "Легко" if diff > 100 else "Средне" if diff > 50 else "Сложно"
        difficulty_color = COLORS['success'] if diff > 100 else COLORS['text'] if diff > 50 else COLORS['error']

        self.difficulty_label = tk.Label(self.container, text=f"Сложность: {difficulty} (разница ~{diff} Hz)",
                                         font=("Arial", 14), bg=COLORS['bg'], fg=difficulty_color)
        self.difficulty_label.pack(pady=(0, 25))

        self.status_label = tk.Label(self.container, text='Нажми «Играть», чтобы услышать два тона',
                                      font=("Arial", 16), bg=COLORS['bg'], fg=COLORS['text'])
        self.status_label.pack(pady=(0, 30))

        # кнопки выбора
        self.buttons_frame = tk.Frame(self.container, bg=COLORS['bg'])
        self.buttons_frame.pack(pady=(0, 30))
        self.choice_buttons = []

        for i, label in enumerate(["Первый тон", "Второй тон"]):
            btn = tk.Button(self.buttons_frame, text=label, font=("Arial", 22, "bold"),
                           bg=COLORS['card'], fg=COLORS['text'], width=14, height=3,
                           relief=tk.FLAT, cursor="hand2", command=lambda idx=i: self.on_choice(idx))
            btn.grid(row=0, column=i, padx=20, pady=10)
            self.choice_buttons.append(btn)

        # кнопка воспроизведения
        self.play_btn = tk.Button(self.container, text="▶ Играть", font=("Arial", 20, "bold"),
                                  bg=COLORS['success'], fg="white", width=20, height=2,
                                  relief=tk.FLAT, cursor="hand2", command=self.on_play)
        self.play_btn.pack(pady=(0, 20))

        back = tk.Button(self.root, text="← Назад в меню", font=("Arial", 14, "bold"),
                        bg=COLORS['card'], fg=COLORS['text'], width=22, relief=tk.FLAT,
                        cursor="hand2", command=self.back_to_menu)
        back.place(relx=0.5, rely=0.95, anchor='center')

        self.set_choices_enabled(False)

    def set_choices_enabled(self, enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        for b in self.choice_buttons:
            b.config(state=state)

    def on_play(self):
        if self.is_playing:
            return

        self.is_playing = True
        self.play_btn.config(state=tk.DISABLED, text="▶ Воспроизведение...")
        self.set_choices_enabled(False)
        self.status_label.config(text="🎵 Слушай внимательно...", fg=COLORS['accent'])

        self.generate_frequencies()
        self.play_sequence(index=0)

    def generate_frequencies(self):
        base_freq = 500 + random.randint(-50, 50)
        diff = self.frequency_diffs[self.round - 1]
        actual_diff = diff + random.randint(-10, 10)

        low_freq = base_freq
        high_freq = base_freq + actual_diff

        if random.random() > 0.5:
            self.frequencies = [low_freq, high_freq]
            self.target_index = 1
        else:
            self.frequencies = [high_freq, low_freq]
            self.target_index = 0

    def play_sequence(self, index):
        if index >= 2:
            self.is_playing = False
            self.play_btn.config(state=tk.NORMAL, text="▶ Играть ещё раз")
            self.set_choices_enabled(True)
            self.status_label.config(text="Какой тон был выше? Выбери один из двух.", fg=COLORS['text'])
            return

        freq = self.frequencies[index]
        tone_label = "Первый" if index == 0 else "Второй"
        self.status_label.config(text=f"🎵 {tone_label} тон...", fg=COLORS['accent'])

        self.play_tone(freq, duration=0.8)
        self.root.after(1200, lambda: self.play_sequence(index + 1))

    def play_tone(self, freq, duration=0.8):
        try:
            sample_rate = 44100
            t = np.linspace(0, duration, int(sample_rate * duration), False)

            # плавное нарастание и затухание
            envelope = np.ones_like(t)
            fade_samples = int(sample_rate * 0.05)
            envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
            envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)

            wave_data = 0.4 * np.sin(2 * np.pi * freq * t) * envelope
            audio = (wave_data * 32767).astype(np.int16)

            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_file.close()
            self.temp_files.append(temp_file.name)

            with wave.open(temp_file.name, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio.tobytes())

            sound = pygame.mixer.Sound(temp_file.name)
            sound.play()
        except Exception as e:
            print(f"ошибка звука: {e}")
            self.status_label.config(text=f"❌ Ошибка: {str(e)[:50]}", fg=COLORS['error'])

    def on_choice(self, idx):
        self.set_choices_enabled(False)
        self.play_btn.config(state=tk.DISABLED)

        if idx == self.target_index:
            self.correct_answers += 1
            self.status_label.config(text="✅ Правильно!", fg=COLORS['success'])
        else:
            correct_label = "Первый" if self.target_index == 0 else "Второй"
            self.status_label.config(text=f"❌ Неправильно. {correct_label} тон был выше.", fg=COLORS['error'])

        self.root.after(2000, self.next_round)

    def next_round(self):
        self.round += 1

        if self.round > self.max_rounds:
            self.show_results()
            return

        diff = self.frequency_diffs[self.round - 1]
        difficulty = "Легко" if diff > 100 else "Средне" if diff > 50 else "Сложно"
        difficulty_color = COLORS['success'] if diff > 100 else COLORS['text'] if diff > 50 else COLORS['error']

        self.level_label.config(text=f"Раунд {self.round}/{self.max_rounds}")
        self.difficulty_label.config(text=f"Сложность: {difficulty} (разница ~{diff} Hz)", fg=difficulty_color)
        self.status_label.config(text='Нажми «Играть», чтобы услышать два тона', fg=COLORS['text'])
        self.play_btn.config(state=tk.NORMAL, text="▶ Играть")

    def show_results(self):
        accuracy = (self.correct_answers / self.max_rounds) * 100
        save_result(self.username, "Тест слуха", accuracy)

        for w in self.root.winfo_children():
            w.destroy()
        self.root.configure(bg=COLORS['bg'])

        container = tk.Frame(self.root, bg=COLORS['bg'])
        container.place(relx=0.5, rely=0.5, anchor='center')

        emoji = "🏆" if accuracy == 100 else "🎉" if accuracy >= 75 else "👍" if accuracy >= 50 else "💪"
        tk.Label(container, text=f"{emoji} Тест завершён!", font=("Arial", 38, "bold"),
                 bg=COLORS['bg'], fg=COLORS['success']).pack(pady=(0, 30))

        tk.Label(container, text=f"Правильных ответов: {self.correct_answers}/{self.max_rounds}",
                 font=("Arial", 20), bg=COLORS['bg'], fg=COLORS['text']).pack(pady=12)
        tk.Label(container, text=f"Точность: {accuracy:.0f}%", font=("Arial", 28, "bold"),
                 bg=COLORS['bg'], fg=COLORS['accent']).pack(pady=12)

        if accuracy == 100:
            comment = "Идеальный слух! 🎵"
        elif accuracy >= 75:
            comment = "Отличный результат! 🎧"
        elif accuracy >= 50:
            comment = "Хороший слух! 🔊"
        else:
            comment = "Продолжай тренироваться! 💪"

        tk.Label(container, text=comment, font=("Arial", 18),
                 bg=COLORS['bg'], fg=COLORS['text_dim']).pack(pady=(15, 0))

        back = tk.Button(self.root, text="← Вернуться в меню", font=("Arial", 16, "bold"),
                        bg=COLORS['accent'], fg="white", width=22, height=2,
                        relief=tk.FLAT, cursor="hand2", command=self.back_to_menu)
        back.place(relx=0.5, rely=0.92, anchor='center')

    def cleanup_temp_files(self):
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception as e:
                print(f"не удалось удалить {temp_file}: {e}")
        self.temp_files.clear()

    def back_to_menu(self):
        try:
            pygame.mixer.quit()
        except:
            pass
        self.cleanup_temp_files()
        from modules.main_menu import MainMenu
        MainMenu(self.app)
