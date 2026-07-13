import random
import tkinter as tk
from tkinter import StringVar
import os

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Taschenrechner")
        self.root.geometry("800x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#fafafa")

        # Status: wurde gerade ein Ergebnis berechnet?
        self.just_calculated = False

        # History – aus Datei laden, falls vorhanden
        self.history_file = "history.txt"
        self.history = self.load_history()
        self.history_visible = False

        # Haupt-Frames
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True)

        calc_frame = tk.Frame(main_frame, bg="#f0f0f0")
        calc_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Display
        self.display_var = StringVar()
        self.display_var.set("0")

        display = tk.Entry(
            calc_frame,
            textvar=self.display_var,
            font=("Segoe UI", 28, "bold"),
            justify="right",
            bd=0,
            relief=tk.FLAT,
            bg="white",
            fg="#222",
            insertbackground="#222",
            highlightthickness=0
        )
        display.pack(fill=tk.X, pady=(0, 10))
        display.focus_set()  # Fokus für Tastatureingaben

        # History toggle button
        self.history_btn = tk.Button(
            calc_frame,
            text="📋 Verlauf",
            font=("Segoe UI", 10, "bold"),
            bg="#1976D2",
            fg="white",
            command=self.toggle_history,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0
        )
        self.history_btn.pack(fill=tk.X, pady=(0, 10))

        # Buttons frame
        buttons_frame = tk.Frame(calc_frame, bg="#fafafa")
        buttons_frame.pack(fill=tk.BOTH, expand=True)

        # Button-Layout
        buttons = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("÷", 0, 3),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("×", 1, 3),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("−", 2, 3),
            ("0", 3, 0), (".", 3, 1), ("=", 3, 2), ("+", 3, 3),
            ("C", 4, 0), ("←", 4, 1), ("(", 4, 2), (")", 4, 3),
        ]

        for (text, row, col) in buttons:
            self.create_button(text, row, col, buttons_frame)

        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)

        # History panel
        self.history_frame = tk.Frame(main_frame, bg="white", width=280)
        self.history_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
        self.history_frame.pack_propagate(False)

        history_title = tk.Label(
            self.history_frame,
            text="Rechenverlauf",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#333"
        )
        history_title.pack(fill=tk.X, pady=10, padx=10)

        history_scroll = tk.Scrollbar(self.history_frame)
        history_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_text = tk.Text(
            self.history_frame,
            font=("Arial", 10),
            bg="white",
            fg="#333",
            yscrollcommand=history_scroll.set,
            relief=tk.SUNKEN,
            bd=1,
            wrap=tk.WORD
        )
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.history_text.config(state=tk.DISABLED)
        history_scroll.config(command=self.history_text.yview)

        clear_history_btn = tk.Button(
            self.history_frame,
            text="Löschen",
            font=("Arial", 9),
            bg="#f44336",
            fg="white",
            command=self.clear_history,
            relief=tk.RAISED,
            bd=1
        )
        clear_history_btn.pack(fill=tk.X, padx=5, pady=5)

        # Initially hide history
        self.history_frame.pack_forget()

        # Footer
        footer_frame = tk.Frame(root, bg="#fafafa", height=48)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.game_button = tk.Button(
            footer_frame,
            text="Schere, Stein, Papier",
            font=("Segoe UI", 10, "bold"),
            bg="#5c6bc0",
            fg="white",
            command=self.open_game_window,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            padx=10,
            pady=6
        )
        self.game_button.pack(side=tk.LEFT, padx=12, pady=6)
        self.game_window = None

        credit_label = tk.Label(
            footer_frame,
            text="Created by Patrick Weidel",
            font=("Segoe UI", 8),
            bg="#fafafa",
            fg="#666"
        )
        credit_label.pack(side=tk.RIGHT, padx=12)

        # Tastaturbindungen
        self.root.bind('<Key>', self.on_key_press)
        self.root.bind('<Return>', lambda e: self.handle_equal())
        self.root.bind('<BackSpace>', lambda e: self.handle_backspace())
        self.root.bind('<Escape>', lambda e: self.handle_clear())

        # History beim Start anzeigen (falls vorhanden)
        self.update_history()

    def create_button(self, text, row, col, parent):
        if text == "=":
            btn_color = "#43a047"
            fg_color = "white"
            active_bg = "#36913a"
        elif text in ["C", "←"]:
            btn_color = "#ef5350"
            fg_color = "white"
            active_bg = "#d64a45"
        elif text in ["÷", "×", "−", "+"]:
            btn_color = "#ff8a65"
            fg_color = "white"
            active_bg = "#ff7043"
        else:
            btn_color = "#ffffff"
            fg_color = "#222"
            active_bg = "#f5f5f5"

        btn = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 16, "bold"),
            bg=btn_color,
            fg=fg_color,
            activebackground=active_bg,
            activeforeground=fg_color,
            command=lambda: self.on_button_click(text),
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0
        )
        btn.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)
        btn.bind("<Enter>", lambda e, b=btn, c=active_bg: b.configure(bg=c))
        btn.bind("<Leave>", lambda e, b=btn, c=btn_color: b.configure(bg=c))

    # ---------- Tastatur- und Button-Ereignisse ----------
    def on_key_press(self, event):
        char = event.char
        if char in "0123456789.":
            self.handle_digit(char)
        elif char in "+-*/":
            # * und / werden intern in × und ÷ umgewandelt
            if char == '*':
                self.handle_operator('×')
            elif char == '/':
                self.handle_operator('÷')
            else:
                self.handle_operator(char)
        elif char == '(' or char == ')':
            self.handle_digit(char)  # Klammern wie Ziffern behandeln
        elif char == '=' or char == '\r':
            self.handle_equal()
        elif char == '\x08':  # Backspace
            self.handle_backspace()
        elif char == '\x1b':  # Escape
            self.handle_clear()

    def on_button_click(self, char):
        if char == "C":
            self.handle_clear()
        elif char == "←":
            self.handle_backspace()
        elif char == "=":
            self.handle_equal()
        elif char in "0123456789.()":
            self.handle_digit(char)
        elif char in "÷×−+":
            self.handle_operator(char)

    # ---------- Einzelne Aktionen ----------
    def handle_digit(self, char):
        current = self.display_var.get()
        if self.just_calculated:
            # Nach einem Ergebnis wird bei neuer Ziffer die Anzeige zurückgesetzt
            self.display_var.set(char)
            self.just_calculated = False
        else:
            if current == "0" and char != ".":
                self.display_var.set(char)
            else:
                self.display_var.set(current + char)

    def handle_operator(self, op):
        current = self.display_var.get()
        if current and current[-1] not in "÷×−+":
            self.display_var.set(current + op)
            self.just_calculated = False

    def handle_clear(self):
        self.display_var.set("0")
        self.just_calculated = False

    def handle_backspace(self):
        current = self.display_var.get()
        if len(current) > 1:
            self.display_var.set(current[:-1])
        else:
            self.display_var.set("0")
        self.just_calculated = False

    def handle_equal(self):
        try:
            expression = self.display_var.get()
            original_expression = expression

            # Erlaubte Zeichen prüfen (nur Ziffern, Punkt, Klammern, Grundrechenarten)
            allowed = set("0123456789.()+-*/ ")
            if not all(c in allowed for c in expression.replace('÷', '/').replace('×', '*').replace('−', '-')):
                self.display_var.set("Ungültige Zeichen")
                return

            # Ersetzen für Python
            python_expr = expression.replace("÷", "/").replace("×", "*").replace("−", "-")

            # Sicheres eval mit leerem globals
            result = eval(python_expr, {})
            # Formatierung
            if isinstance(result, float):
                if result == int(result):
                    result_str = str(int(result))
                else:
                    result_str = str(round(result, 10))
            else:
                result_str = str(result)

            # In History aufnehmen
            self.history.append(f"{original_expression} = {result_str}")
            self.update_history()
            self.save_history()

            self.display_var.set(result_str)
            self.just_calculated = True
        except ZeroDivisionError:
            self.display_var.set("Division durch Null")
            self.just_calculated = False
        except SyntaxError:
            self.display_var.set("Syntaxfehler")
            self.just_calculated = False
        except Exception:
            self.display_var.set("Fehler")
            self.just_calculated = False

    # ---------- History ----------
    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        return []

    def save_history(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            f.write("\n".join(self.history))

    def toggle_history(self):
        if self.history_visible:
            self.history_frame.pack_forget()
            self.history_btn.config(relief=tk.RAISED)
            self.history_visible = False
        else:
            self.history_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
            self.history_btn.config(relief=tk.SUNKEN)
            self.history_visible = True

    def update_history(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        for entry in self.history:
            self.history_text.insert(tk.END, entry + "\n")
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)

    def clear_history(self):
        self.history = []
        self.update_history()
        self.save_history()

    # ---------- Schere-Stein-Papier ----------
    def open_game_window(self):
        if self.game_window is not None and tk.Toplevel.winfo_exists(self.game_window):
            self.game_window.lift()
            return

        self.game_window = tk.Toplevel(self.root)
        self.game_window.title("Schere, Stein, Papier")
        self.game_window.geometry("320x260")
        self.game_window.resizable(False, False)
        self.game_window.transient(self.root)
        self.game_window.grab_set()

        instruction = tk.Label(
            self.game_window,
            text="Wähle Schere, Stein oder Papier:",
            font=("Segoe UI", 11, "bold"),
            bg="#fafafa",
            fg="#222"
        )
        instruction.pack(pady=(15, 10), padx=10)

        button_frame = tk.Frame(self.game_window, bg="#fafafa")
        button_frame.pack(pady=5, padx=10, fill=tk.X)

        for choice in ["Schere", "Stein", "Papier"]:
            btn = tk.Button(
                button_frame,
                text=choice,
                font=("Segoe UI", 12, "bold"),
                bg="#ffffff",
                fg="#222",
                relief=tk.RAISED,
                bd=1,
                command=lambda c=choice: self.play_rps(c)
            )
            btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.result_label = tk.Label(
            self.game_window,
            text="",
            font=("Segoe UI", 11),
            bg="#fafafa",
            fg="#333",
            wraplength=280,
            justify=tk.LEFT
        )
        self.result_label.pack(pady=(15, 5), padx=10)

        close_btn = tk.Button(
            self.game_window,
            text="Schließen",
            font=("Segoe UI", 10),
            bg="#1976D2",
            fg="white",
            command=self.close_game_window,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            padx=8,
            pady=6
        )
        close_btn.pack(pady=(10, 10))

        self.game_window.protocol("WM_DELETE_WINDOW", self.close_game_window)

    def close_game_window(self):
        if self.game_window is not None:
            self.game_window.destroy()
            self.game_window = None

    def play_rps(self, player_choice):
        if self.game_window is None or not tk.Toplevel.winfo_exists(self.game_window):
            return
        self.result_label.config(text="Der Gegner denkt nach...")
        self.root.after(800, lambda: self.show_rps_result(player_choice))

    def show_rps_result(self, player_choice):
        if self.game_window is None or not tk.Toplevel.winfo_exists(self.game_window):
            return
        options = ["Schere", "Stein", "Papier"]
        cpu_choice = random.choice(options)
        result = self.get_rps_result(player_choice, cpu_choice)
        self.result_label.config(
            text=f"Du: {player_choice}\nGegner: {cpu_choice}\nErgebnis: {result}"
        )

    @staticmethod
    def get_rps_result(player, cpu):
        if player == cpu:
            return "Unentschieden"
        if (player == "Schere" and cpu == "Papier") or \
           (player == "Stein" and cpu == "Schere") or \
           (player == "Papier" and cpu == "Stein"):
            return "Du gewinnst!"
        return "Der Gegner gewinnt."


if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()