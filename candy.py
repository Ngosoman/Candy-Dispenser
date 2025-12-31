import tkinter as tk
from tkinter import messagebox

# ---------------- CONFIG ----------------
MAX_CAPACITY = 10
CANDY_HEIGHT = 30
SPRING_MIN = 50
SPRING_MAX = 300

# ---------------- APP ----------------
class CandyDispenser:
    def __init__(self, root):
        self.root = root
        self.root.title("Candy Dispenser - Stack + Spring")
        self.stack = []

        self.canvas = tk.Canvas(root, width=300, height=450, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=20, pady=20)

        self.controls = tk.Frame(root)
        self.controls.pack(side=tk.RIGHT, padx=20)

        self.info = tk.Label(self.controls, text="Candies: 0", font=("Arial", 14))
        self.info.pack(pady=10)

        tk.Button(self.controls, text=" Add Candy", width=20, command=self.add_candy).pack(pady=5)
        tk.Button(self.controls, text=" Remove Candy", width=20, command=self.remove_candy).pack(pady=5)
        tk.Button(self.controls, text=" Count Candies", width=20, command=self.count_candies).pack(pady=5)
        tk.Button(self.controls, text=" Is Empty", width=20, command=self.is_empty).pack(pady=5)
        tk.Button(self.controls, text=" Exit", width=20, command=root.destroy).pack(pady=20)

        self.draw()

    # ------------ DRAWING ------------
    def draw(self):
        self.canvas.delete("all")

        # Draw container
        self.canvas.create_rectangle(80, 50, 220, 400, outline="black", width=3)

        # Spring logic
        spring_length = SPRING_MAX - (len(self.stack) * 20)
        spring_length = max(SPRING_MIN, spring_length)

        self.canvas.create_line(
            150, 50,
            150, 50 + spring_length,
            width=4
        )

        # Draw candies
        y = 400
        for _ in self.stack:
            y -= CANDY_HEIGHT
            self.canvas.create_rectangle(
                100, y, 200, y + CANDY_HEIGHT,
                fill="pink", outline="black"
            )

        self.info.config(text=f"Candies: {len(self.stack)}/{MAX_CAPACITY}")

    # ------------ STACK METHODS ------------
    def add_candy(self):
        if len(self.stack) == MAX_CAPACITY:
            messagebox.showerror("Full", "Dispenser is FULL")
            return
        self.stack.append("🍬")
        self.animate()
        self.draw()

    def remove_candy(self):
        if not self.stack:
            messagebox.showwarning("Empty", "Dispenser is EMPTY")
            return
        self.stack.pop()
        self.animate()
        self.draw()

    def count_candies(self):
        messagebox.showinfo("Count", f"Total candies: {len(self.stack)}")

    def is_empty(self):
        if not self.stack:
            messagebox.showinfo("Empty", "Dispenser is EMPTY")
        else:
            messagebox.showinfo("Not Empty", "Dispenser is NOT empty")

    # ------------ ANIMATION ------------
    def animate(self):
        for _ in range(5):
            self.draw()
            self.root.update()
            self.root.after(50)

# ---------------- RUN ----------------
root = tk.Tk()
app = CandyDispenser(root)
root.mainloop()
