import json
import os
from datetime import datetime
import tkinter as tk
from modules.config import COLORS, DATA_FILE

def save_result(username, test_name, score):
    os.makedirs("data", exist_ok=True)
    results = load_results()
    results.append({
        "username": username,
        "test": test_name,
        "score": round(score, 2),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

def load_results():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def get_user_stats(username):
    results = load_results()
    user_results = [r for r in results if r['username'] == username]
    if not user_results:
        return None

    stats = {'total_tests': len(user_results), 'best_scores': {}}
    for r in user_results:
        test, score = r['test'], r['score']
        if test not in stats['best_scores'] or score > stats['best_scores'][test]:
            stats['best_scores'][test] = score
    return stats

def get_leaderboard():
    results, users = load_results(), {}
    for r in results:
        u = r['username']
        if u not in users:
            users[u] = {'total_tests': 0, 'total_score': 0}
        users[u]['total_tests'] += 1
        users[u]['total_score'] += r['score']

    board = [{'username': u, 'total_tests': d['total_tests'],
              'avg_score': d['total_score'] / d['total_tests']}
             for u, d in users.items()]
    board.sort(key=lambda x: x['avg_score'], reverse=True)
    return board

def create_header(root, title, subtitle):
    """создание стандартного заголовка"""
    header = tk.Frame(root, bg=COLORS['bg'], height=130)
    header.pack(fill=tk.X, padx=55, pady=35)
    header.pack_propagate(False)
    tk.Label(header, text=title, font=("Arial", 30, "bold"),
             bg=COLORS['bg'], fg=COLORS['text']).pack(anchor='w')
    tk.Label(header, text=subtitle, font=("Arial", 15),
             bg=COLORS['bg'], fg=COLORS['text_dim']).pack(anchor='w', pady=(12, 0))
    return header

def show_user_results(app):
    for w in app.root.winfo_children():
        w.destroy()
    app.root.configure(bg=COLORS['bg'])

    create_header(app.root, "📊 Мои результаты", f"Пользователь: {app.username}")
    stats = get_user_stats(app.username)

    center = tk.Frame(app.root, bg=COLORS['bg'])
    center.pack(expand=True, fill=tk.BOTH, padx=55, pady=(0, 35))

    if not stats:
        tk.Label(center, text="Пока нет результатов!\n\nПройди тесты!",
                 font=("Arial", 17), bg=COLORS['bg'], fg=COLORS['text_dim'],
                 justify=tk.CENTER).pack(expand=True)
    else:
        tk.Label(center, text=f"Всего тестов: {stats['total_tests']}",
                 font=("Arial", 19, "bold"), bg=COLORS['bg'], fg=COLORS['text']).pack(pady=22)

        tk.Label(center, text="🏆 Лучшие результаты:", font=("Arial", 21, "bold"),
                 bg=COLORS['bg'], fg=COLORS['warning']).pack(pady=(22, 22))

        for test, score in stats['best_scores'].items():
            card = tk.Frame(center, bg=COLORS['card'],
                           highlightthickness=1, highlightbackground=COLORS['border'])
            card.pack(fill=tk.X, pady=9)
            inner = tk.Frame(card, bg=COLORS['card'])
            inner.pack(fill=tk.X, padx=32, pady=22)

            tk.Label(inner, text=test, font=("Arial", 17, "bold"),
                     bg=COLORS['card'], fg=COLORS['text']).pack(side=tk.LEFT)

            score_text = f"{score:.0f} мс" if test == "Тест реакции" else f"{score:.0f}"
            tk.Label(inner, text=score_text, font=("Arial", 17, "bold"),
                     bg=COLORS['card'], fg=COLORS['success']).pack(side=tk.RIGHT)

    btn = tk.Button(app.root, text="← Вернуться в меню", command=lambda: back_to_menu(app),
                    font=("Arial", 15, "bold"), bg=COLORS['accent'], fg='white',
                    relief=tk.FLAT, cursor="hand2", padx=45, pady=17, borderwidth=0)
    btn.pack(pady=35)

def show_leaderboard(app):
    for w in app.root.winfo_children():
        w.destroy()
    app.root.configure(bg=COLORS['bg'])

    create_header(app.root, "🏆 Таблица лидеров", "Топ игроков")
    board = get_leaderboard()

    center = tk.Frame(app.root, bg=COLORS['bg'])
    center.pack(expand=True, fill=tk.BOTH, padx=55, pady=(0, 35))

    if not board:
        tk.Label(center, text="Таблица пуста!\n\nСтань первым!",
                 font=("Arial", 17), bg=COLORS['bg'], fg=COLORS['text_dim'],
                 justify=tk.CENTER).pack(expand=True)
    else:
        # заголовок таблицы
        hdr = tk.Frame(center, bg=COLORS['card'], height=55)
        hdr.pack(fill=tk.X, pady=(0, 12))
        hdr.pack_propagate(False)

        for text, width in [("Место", 10), ("Имя", 25), ("Тестов", 10), ("Средний балл", 15)]:
            tk.Label(hdr, text=text, font=("Arial", 15, "bold"),
                     bg=COLORS['card'], fg=COLORS['text_dim'], width=width,
                     anchor='w' if text == "Имя" else 'center').pack(side=tk.LEFT, padx=12 if text != "Место" else 22)

        # строки лидеров
        medals = {1: "🥇", 2: "🥈", 3: "🥉"}
        for i, p in enumerate(board[:10], 1):
            bg = COLORS['card'] if i % 2 == 0 else COLORS['card_hover']
            row = tk.Frame(center, bg=bg, height=65)
            row.pack(fill=tk.X, pady=2)
            row.pack_propagate(False)

            place = medals.get(i, str(i))
            name_col = COLORS['warning'] if p['username'] == app.username else COLORS['text']

            tk.Label(row, text=place, font=("Arial", 17, "bold"),
                     bg=bg, fg=COLORS['text'], width=10).pack(side=tk.LEFT, padx=22)
            tk.Label(row, text=p['username'], font=("Arial", 15, "bold"),
                     bg=bg, fg=name_col, width=25, anchor='w').pack(side=tk.LEFT, padx=12)
            tk.Label(row, text=str(p['total_tests']), font=("Arial", 15),
                     bg=bg, fg=COLORS['text'], width=10).pack(side=tk.LEFT, padx=12)
            tk.Label(row, text=f"{p['avg_score']:.1f}", font=("Arial", 15, "bold"),
                     bg=bg, fg=COLORS['success'], width=15).pack(side=tk.LEFT, padx=12)

    btn = tk.Button(app.root, text="← Вернуться в меню", command=lambda: back_to_menu(app),
                    font=("Arial", 15, "bold"), bg=COLORS['accent'], fg='white',
                    relief=tk.FLAT, cursor="hand2", padx=45, pady=17, borderwidth=0)
    btn.pack(pady=35)

def back_to_menu(app):
    from modules.main_menu import MainMenu
    MainMenu(app)
