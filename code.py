# rps_gui.py
import tkinter as tk
from tkinter import messagebox
import random
import os

# --- Game data & helpers ---
CHOICES = ["Rock", "Paper", "Scissors"]

def decide_winner(user_idx, comp_idx):
    """Return 'User', 'Computer' or 'Draw' and the winning choice name."""
    if user_idx == comp_idx:
        return "Draw", None
    # rock(0) beats scissors(2); paper(1) beats rock(0); scissors(2) beats paper(1)
    if (user_idx == 0 and comp_idx == 2) or (user_idx == 1 and comp_idx == 0) or (user_idx == 2 and comp_idx == 1):
        return "User", CHOICES[user_idx]
    else:
        return "Computer", CHOICES[comp_idx]

# --- GUI App ---
class RPSApp:
    def __init__(self, root):
        self.root = root
        root.title("Rock Paper Scissors")
        root.geometry("420x420")
        root.resizable(False, False)
        self.bg = "#f0f8ff"
        root.configure(bg=self.bg)

        # Scoreboard
        self.wins = 0
        self.losses = 0
        self.ties = 0

        # Top title
        title = tk.Label(root, text="Rock • Paper • Scissors", font=("Helvetica", 18, "bold"), bg=self.bg)
        title.pack(pady=(18, 8))

        # Info / instruction
        inst = tk.Label(root, text="Choose your move:", font=("Arial", 12), bg=self.bg)
        inst.pack()

        # Button frame
        btn_frame = tk.Frame(root, bg=self.bg)
        btn_frame.pack(pady=8)

        # Try to load images from assets/ (optional). If not present, use emoji labels.
        self.images = {}
        asset_dir = os.path.join(os.path.dirname(__file__), "assets")
        for name in ("rock", "paper", "scissors"):
            path = os.path.join(asset_dir, f"{name}.png")
            if os.path.exists(path):
                try:
                    self.images[name] = tk.PhotoImage(file=path)
                except Exception:
                    self.images[name] = None
            else:
                self.images[name] = None

        # Buttons
        rock_btn = tk.Button(btn_frame, text="🪨 Rock", width=12, height=2,
                             command=lambda: self.play(0))
        paper_btn = tk.Button(btn_frame, text="📄 Paper", width=12, height=2,
                              command=lambda: self.play(1))
        scissor_btn = tk.Button(btn_frame, text="✂️ Scissors", width=12, height=2,
                                command=lambda: self.play(2))

        # If images exist, put images on buttons instead of emojis
        if self.images["rock"]:
            rock_btn.config(image=self.images["rock"], compound="top", text="")
        if self.images["paper"]:
            paper_btn.config(image=self.images["paper"], compound="top", text="")
        if self.images["scissors"]:
            scissor_btn.config(image=self.images["scissors"], compound="top", text="")

        # Layout buttons
        rock_btn.grid(row=0, column=0, padx=8)
        paper_btn.grid(row=0, column=1, padx=8)
        scissor_btn.grid(row=0, column=2, padx=8)
        btn_frame.pack()

        # Result display area
        self.result_label = tk.Label(root, text="", font=("Arial", 13), bg=self.bg, justify="center")
        self.result_label.pack(pady=18)

        # Scoreboard display
        self.score_label = tk.Label(root, text=self.score_text(), font=("Arial", 12), bg=self.bg)
        self.score_label.pack(pady=(0, 12))

        # Bottom controls
        ctrl_frame = tk.Frame(root, bg=self.bg)
        ctrl_frame.pack(pady=6)

        restart_btn = tk.Button(ctrl_frame, text="Restart Score", command=self.reset_scores, width=12)
        quit_btn = tk.Button(ctrl_frame, text="Quit", command=self.confirm_quit, width=12)
        restart_btn.grid(row=0, column=0, padx=6)
        quit_btn.grid(row=0, column=1, padx=6)

    def score_text(self):
        return f"Wins: {self.wins}   Losses: {self.losses}   Ties: {self.ties}"

    def play(self, user_choice_idx):
        comp_choice_idx = random.randint(0, 2)
        user_choice = CHOICES[user_choice_idx]
        comp_choice = CHOICES[comp_choice_idx]

        winner, winning_choice = decide_winner(user_choice_idx, comp_choice_idx)
        if winner == "Draw":
            self.ties += 1
            result_text = f"You chose {user_choice}  •  Computer chose {comp_choice}\n\nIt's a tie!"
        elif winner == "User":
            self.wins += 1
            result_text = f"You chose {user_choice}  •  Computer chose {comp_choice}\n\nYou win! ({winning_choice} wins)"
        else:
            self.losses += 1
            result_text = f"You chose {user_choice}  •  Computer chose {comp_choice}\n\nComputer wins! ({winning_choice} wins)"

        self.result_label.config(text=result_text)
        self.score_label.config(text=self.score_text())

    def reset_scores(self):
        self.wins = self.losses = self.ties = 0
        self.score_label.config(text=self.score_text())
        self.result_label.config(text="Scores reset. Play again!")

    def confirm_quit(self):
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.root.destroy()

def main():
    root = tk.Tk()
    app = RPSApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
