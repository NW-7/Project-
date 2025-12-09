import tkinter as tk
from tkinter import messagebox
from modules.config import COLORS

class SensoryTestApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Проверка сенсорных способностей")
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg=COLORS['bg'])
        self.root.bind('<Escape>', lambda e: self.toggle_fullscreen())
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
        self.username = None
        self.show_welcome_screen()

    def toggle_fullscreen(self):
        current = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current)

    def show_welcome_screen(self):
        for w in self.root.winfo_children():
            w.destroy()

        container = tk.Frame(self.root, bg=COLORS['bg'])
        container.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(container, text="🎯", font=("Arial", 80),
                 bg=COLORS['bg'], fg=COLORS['accent']).pack(pady=(0, 30))

        tk.Label(container, text="Добро пожаловать!", font=("Arial", 42, "bold"),
                 bg=COLORS['bg'], fg=COLORS['text']).pack(pady=(0, 15))

        tk.Label(container, text="Тесты сенсорных способностей", font=("Arial", 20),
                 bg=COLORS['bg'], fg=COLORS['text_dim']).pack(pady=(0, 60))

        tk.Label(container, text="Введите ваше имя:", font=("Arial", 18),
                 bg=COLORS['bg'], fg=COLORS['text']).pack(pady=(0, 20))

        entry_frame = tk.Frame(container, bg=COLORS['card'],
                               highlightthickness=2, highlightbackground=COLORS['border'])
        entry_frame.pack(pady=(0, 40))

        self.name_var = tk.StringVar()
        entry = tk.Entry(entry_frame, textvariable=self.name_var, font=("Arial", 20),
                        bg=COLORS['card'], fg=COLORS['text'], 
                        insertbackground=COLORS['accent'], relief=tk.FLAT,
                        width=28, bd=0, justify='center')
        entry.pack(padx=30, pady=20)
        entry.focus()
        entry.bind('<Return>', lambda e: self.start_app())

        btn = tk.Button(container, text="Начать →", command=self.start_app,
                       font=("Arial", 20, "bold"), bg=COLORS['accent'], fg='white',
                       relief=tk.FLAT, cursor="hand2", padx=60, pady=20, borderwidth=0)
        btn.pack()
        btn.bind('<Enter>', lambda e: btn.config(bg=COLORS['accent_hover']))
        btn.bind('<Leave>', lambda e: btn.config(bg=COLORS['accent']))

        tk.Label(container, text="ESC - выход из полноэкранного режима",
                 font=("Arial", 11), bg=COLORS['bg'], fg=COLORS['text_dim']).pack(pady=(40, 0))

    def start_app(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Внимание", "Пожалуйста, введите имя!")
            return
        self.username = name
        from modules.main_menu import MainMenu
        MainMenu(self)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SensoryTestApp()
    app.run()
