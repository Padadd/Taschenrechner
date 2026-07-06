import tkinter as tk
from tkinter import StringVar


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Taschenrechner")
        self.root.geometry("800x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # History list
        self.history = []
        self.history_visible = False
        
        # Main container
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Calculator frame
        calc_frame = tk.Frame(main_frame, bg="#f0f0f0")
        calc_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Display
        self.display_var = StringVar()
        self.display_var.set("0")
        
        display = tk.Entry(
            calc_frame,
            textvar=self.display_var,
            font=("Arial", 28, "bold"),
            justify="right",
            bd=2,
            relief=tk.SUNKEN,
            bg="white",
            fg="#333"
        )
        display.pack(fill=tk.X, pady=(0, 10))
        
        # History toggle button
        self.history_btn = tk.Button(
            calc_frame,
            text="📋 Verlauf",
            font=("Arial", 10, "bold"),
            bg="#2196F3",
            fg="white",
            command=self.toggle_history,
            relief=tk.RAISED,
            bd=1
        )
        self.history_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons frame
        buttons_frame = tk.Frame(calc_frame, bg="#f0f0f0")
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button Layout
        buttons = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("÷", 0, 3),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("×", 1, 3),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("−", 2, 3),
            ("0", 3, 0), (".", 3, 1), ("=", 3, 2), ("+", 3, 3),
            ("C", 4, 0), ("←", 4, 1), ("(", 4, 2), (")", 4, 3),
        ]
        
        # Create buttons
        for (text, row, col) in buttons:
            self.create_button(text, row, col, buttons_frame)
        
        # Grid configuration for buttons
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)
        
        # History panel frame
        self.history_frame = tk.Frame(main_frame, bg="white", width=280)
        self.history_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
        self.history_frame.pack_propagate(False)
        
        # History title
        history_title = tk.Label(
            self.history_frame,
            text="Rechenverlauf",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#333"
        )
        history_title.pack(fill=tk.X, pady=10, padx=10)
        
        # History text widget
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
        
        # Clear history button
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
    
    def create_button(self, text, row, col, parent):
        """Create a button with specific styling"""
        if text == "=":
            btn_color = "#4CAF50"
            fg_color = "white"
        elif text in ["C", "←", "÷", "×", "−", "+"]:
            btn_color = "#f44336"
            fg_color = "white"
        else:
            btn_color = "#e8e8e8"
            fg_color = "#333"
        
        btn = tk.Button(
            parent,
            text=text,
            font=("Arial", 20, "bold"),
            bg=btn_color,
            fg=fg_color,
            activebackground="#ddd",
            activeforeground="#333",
            command=lambda: self.on_button_click(text),
            relief=tk.RAISED,
            bd=1
        )
        btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
    
    def on_button_click(self, char):
        """Handle button clicks"""
        current = self.display_var.get()
        
        if char == "C":
            self.display_var.set("0")
        elif char == "←":
            if len(current) > 1:
                self.display_var.set(current[:-1])
            else:
                self.display_var.set("0")
        elif char == "=":
            self.calculate()
        elif char in "0123456789.()":
            if current == "0" and char != ".":
                self.display_var.set(char)
            else:
                self.display_var.set(current + char)
        elif char in "÷×−+":
            if current and current[-1] not in "÷×−+":
                self.display_var.set(current + char)
    
    def calculate(self):
        """Calculate the result"""
        try:
            expression = self.display_var.get()
            original_expression = expression
            # Replace symbols with Python operators
            expression = expression.replace("÷", "/").replace("×", "*").replace("−", "-")
            result = eval(expression)
            # Format result (remove unnecessary decimal places)
            if isinstance(result, float):
                if result == int(result):
                    result_str = str(int(result))
                else:
                    result_str = str(round(result, 10))
            else:
                result_str = str(result)
            
            # Add to history
            self.history.append(f"{original_expression} = {result_str}")
            self.update_history()
            
            self.display_var.set(result_str)
        except Exception as e:
            self.display_var.set("Fehler")
    
    def toggle_history(self):
        """Toggle history panel visibility"""
        if self.history_visible:
            self.history_frame.pack_forget()
            self.history_btn.config(relief=tk.RAISED)
            self.history_visible = False
        else:
            self.history_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
            self.history_btn.config(relief=tk.SUNKEN)
            self.history_visible = True
    
    def update_history(self):
        """Update history display"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        for entry in self.history:
            self.history_text.insert(tk.END, entry + "\n")
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)
    
    def clear_history(self):
        """Clear all history"""
        self.history = []
        self.update_history()


if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()
