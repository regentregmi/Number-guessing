import random
import tkinter as tk
from tkinter import messagebox
import json
import os

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("400x500")
        
        # Game variables
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        self.max_attempts = 10
        self.high_score = self.load_high_score()
        
        # GUI elements
        self.label_instruction = tk.Label(root, text="Guess a number between 1 and 100:", font=("Arial", 14))
        self.label_instruction.pack(pady=20)
        
        self.entry_guess = tk.Entry(root, font=("Arial", 12))
        self.entry_guess.pack(pady=10)
        
        self.button_guess = tk.Button(root, text="Submit Guess", command=self.check_guess, font=("Arial", 12))
        self.button_guess.pack(pady=10)
        
        self.label_feedback = tk.Label(root, text="", font=("Arial", 12), wraplength=350)
        self.label_feedback.pack(pady=10)
        
        self.label_attempts = tk.Label(root, text=f"Attempts left: {self.max_attempts}", font=("Arial", 12))
        self.label_attempts.pack(pady=10)
        
        self.label_high_score = tk.Label(root, text=f"Best score: {self.high_score if self.high_score else 'None'}", font=("Arial", 12))
        self.label_high_score.pack(pady=10)
        
        self.button_play_again = tk.Button(root, text="Play Again", command=self.reset_game, font=("Arial", 12), state=tk.DISABLED)
        self.button_play_again.pack(pady=10)
        
        # Bind Enter key to submit guess
        self.root.bind('<Return>', lambda event: self.check_guess())

    def load_high_score(self):
        try:
            if os.path.exists("high_score.json"):
                with open("high_score.json", "r") as file:
                    data = json.load(file)
                    return data.get("high_score", None)
        except:
            return None
        return None

    def save_high_score(self, score):
        with open("high_score.json", "w") as file:
            json.dump({"high_score": score}, file)

    def check_guess(self):
        try:
            guess = int(self.entry_guess.get())
            if guess < 1 or guess > 100:
                self.label_feedback.config(text="Please enter a number between 1 and 100!", fg="red")
                return
        except ValueError:
            self.label_feedback.config(text="Please enter a valid number!", fg="red")
            return

        self.attempts += 1
        attempts_left = self.max_attempts - self.attempts
        self.label_attempts.config(text=f"Attempts left: {attempts_left}")

        if guess == self.target_number:
            self.label_feedback.config(text=f"Congratulations! You guessed it in {self.attempts} attempts!", fg="green")
            self.button_guess.config(state=tk.DISABLED)
            self.button_play_again.config(state=tk.NORMAL)
            # Update high score (lower is better)
            if self.high_score is None or self.attempts < self.high_score:
                self.high_score = self.attempts
                self.save_high_score(self.attempts)
                self.label_high_score.config(text=f"Best score: {self.high_score}")
            messagebox.showinfo("Winner!", f"You guessed the number in {self.attempts} attempts!")
        elif self.attempts >= self.max_attempts:
            self.label_feedback.config(text=f"Game Over! The number was {self.target_number}.", fg="red")
            self.button_guess.config(state=tk.DISABLED)
            self.button_play_again.config(state=tk.NORMAL)
            messagebox.showinfo("Game Over", f"You ran out of attempts! The number was {self.target_number}.")
        elif guess < self.target_number:
            self.label_feedback.config(text="Too low! Try a higher number.", fg="blue")
        else:
            self.label_feedback.config(text="Too high! Try a lower number.", fg="blue")

        self.entry_guess.delete(0, tk.END)

    def reset_game(self):
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        self.label_attempts.config(text=f"Attempts left: {self.max_attempts}")
        self.label_feedback.config(text="")
        self.button_guess.config(state=tk.NORMAL)
        self.button_play_again.config(state=tk.DISABLED)
        self.entry_guess.delete(0, tk.END)
        self.entry_guess.focus()

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGuessingGame(root)
    root.mainloop()