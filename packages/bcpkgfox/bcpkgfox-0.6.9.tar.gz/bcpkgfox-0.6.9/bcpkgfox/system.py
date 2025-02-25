import tkinter as tk
from typing import Optional

class System:
    def __init__(self):
        self.button = None

    def message_of_choices(self,
        message: str,
        choice_1: str,
        choice_2: str,
        title: Optional[str] = None
    ) -> int:
        def on_button1():
            self.button = 1
            window.destroy()

        def on_button2():
            self.button = 2
            window.destroy()

        root = tk.Tk()
        root.withdraw()
        window = tk.Toplevel(root)
        window.title(title if title else "Atenção!")

        # Message label
        message = tk.Label(window, text=message)
        message.pack(padx=20, pady=20)

        # Frame to hold buttons
        button_frame = tk.Frame(window)
        button_frame.pack(pady=10)

        # Two buttons with custom text
        btn1 = tk.Button(button_frame, text=choice_1, command=on_button1)
        btn1.pack(side="left", padx=10)

        btn2 = tk.Button(button_frame, text=choice_2, command=on_button2)
        btn2.pack(side="left", padx=10)

        window.mainloop()
        return self.button

    def message_of_input(self,
        question: str,
        title: Optional[str] = None
    ) -> str:
        def on_submit():
            self.user_input = entry.get()
            window.destroy()
        root = tk.Tk()
        root.withdraw()
        window = tk.Toplevel(root)
        window.title(title if title else "Atenção!")
        window.geometry("300x150")

        # Message label
        message = tk.Label(window, text=question, wraplength=280)
        message.pack(padx=20, pady=5)

        # Input field
        entry = tk.Entry(window, width=30)
        entry.pack(pady=5)
        entry.focus()  # Auto-focus input field

        # Submit button
        btn_submit = tk.Button(window, text="Próximo", command=on_submit)
        btn_submit.pack(pady=10)

        window.mainloop()
        return self.user_input  # Returns the entered text