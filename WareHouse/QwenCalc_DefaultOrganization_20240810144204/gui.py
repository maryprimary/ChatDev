import tkinter as tk
from calculator import Calculator
class GUI:
    '''
    A Graphical User Interface (GUI) class for the calculator application.
    '''
    def __init__(self, master):
        self.master = master
        self.calculator = Calculator()
        self.current_value = 0
        self.create_widgets()
    def create_widgets(self):
        self.display = tk.Entry(self.master, width=35, borderwidth=5)
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('*', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('/', 4, 3),
            ('C', 5, 0),  # Clear button
        ]
        for (text, row, col) in buttons:
            button = tk.Button(self.master, text=text, padx=40, pady=20,
                              command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col)
    def on_button_click(self, text):
        if text == '=':
            try:
                result = eval(self.display.get())
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        elif text == 'C':
            self.display.delete(0, tk.END)
            self.current_value = 0
        else:
            self.display.insert(tk.END, text)