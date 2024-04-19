import tkinter as tk
from tkinter import ttk
from pynput.keyboard import Controller, Key, Listener
import time
import threading
from ttkthemes import ThemedTk

class TypingSimulator:
    def __init__(self, master):
        self.master = master
        self.master.title("Human Typing Simulator")
        self.set_theme()  # Set the theme
        
        self.is_typing = False  # Track if typing is in progress
        
        self.label = ttk.Label(master, text="Enter text:")
        self.label.grid(row=0, column=0, padx=10, pady=10)
        
        self.text_entry = tk.Text(master, width=50, height=10)
        self.text_entry.grid(row=0, column=1, padx=10, pady=10)
        
        self.speed_label = ttk.Label(master, text="Speed:")
        self.speed_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.speed_slider = ttk.Scale(master, from_=0.1, to=1.0, length=200, orient="horizontal", command=self.update_speed_label)
        self.speed_slider.set(0.5)  # Default speed
        self.speed_slider.grid(row=1, column=1, padx=10, pady=10)
        
        self.speed_value_label = ttk.Label(master, text=f"Current Speed: {self.speed_slider.get():.2f}")
        self.speed_value_label.grid(row=2, column=1, padx=10, pady=10)
        
        self.start_button = ttk.Button(master, text="Start Typing", command=self.start_typing)
        self.start_button.grid(row=3, column=0, padx=10, pady=10)

        self.pause_resume_button = ttk.Button(master, text="Pause", command=self.toggle_typing)
        self.pause_resume_button.grid(row=3, column=1, padx=10, pady=10)

        self.hotkey_combination = {Key.ctrl_l, Key.alt_l, Key.space}
        self.hotkey_pressed = set()

        self.listener_thread = threading.Thread(target=self.start_listener)
        self.listener_thread.start()

        self.keyboard = Controller()
        self.typing_thread = None

    def set_theme(self):
        self.style = ttk.Style()
        self.style.theme_use("breeze")  # Change the theme here
        
    def update_speed_label(self, value):
        rounded_speed = round(float(value), 2)
        self.speed_value_label.config(text=f"Current Speed: {rounded_speed}")
        
    def toggle_typing(self):
        self.is_typing = not self.is_typing
        if self.is_typing:
            self.typing_thread = threading.Thread(target=self.type_text)
            self.typing_thread.start()
            self.pause_resume_button.config(text="Pause")
        else:
            self.pause_resume_button.config(text="Resume")
            
    def start_typing(self):
        if not self.typing_thread or not self.typing_thread.is_alive():
            self.is_typing = True
            self.typing_thread = threading.Thread(target=self.type_text)
            self.typing_thread.start()
            
    def type_text(self):
        text_to_type = self.text_entry.get("1.0", tk.END)
        for char in text_to_type:
            if not self.is_typing:
                return
            self.keyboard.type(char)
            time.sleep(self.speed_slider.get())
            self.master.update()



            
    def on_press(self, key):
        if key in self.hotkey_combination:
            self.hotkey_pressed.add(key)
            if len(self.hotkey_combination) == len(self.hotkey_pressed):
                self.toggle_typing()

    def on_release(self, key):
        if key in self.hotkey_pressed:
            self.hotkey_pressed.remove(key)

    def start_listener(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

def main():
    root = ThemedTk(theme="adapta")
    root.geometry("520x320")  # Set default window size
    app = TypingSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

