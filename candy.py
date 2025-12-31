import tkinter as tk
from tkinter import messagebox
import random

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
        # each candy is a dict: {"emoji": str, "color": str}
        self.stack = []
        self.temp_offset = 0  # temporary visual offset for animation (positive compresses)

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
        # Spring anchored at the BOTTOM of the container and extends upward.
        # Candies appear on the top side of the spring (above it) and stack upward.
        spring_bottom_y = 400
        # Each candy shortens the spring a bit; temp_offset further compresses it
        spring_length = SPRING_MAX - (len(self.stack) * 20) - self.temp_offset
        spring_length = max(SPRING_MIN, min(SPRING_MAX, spring_length))
        spring_top_y = spring_bottom_y - spring_length

        # Draw a coil-like spring as a zigzag between spring_top_y and spring_bottom_y
        cx = 150
        coil_points = []
        steps = 60
        amp = 24  # horizontal amplitude
        for i in range(steps + 1):
            t = i / steps
            y = spring_top_y + t * (spring_bottom_y - spring_top_y)
            # oscillate horizontally to simulate coils
            x = cx + amp * ((-1) ** i) * (1 - abs(2 * t - 1))
            coil_points.append((x, y))

        # Flatten points for create_line
        flat = []
        for (x, y) in coil_points:
            flat.extend([x, y])

        self.canvas.create_line(flat, fill="gray40", width=3, smooth=True)

        # Draw candies stacked from spring_top_y upward (they sit on top of the spring)
        y = spring_top_y
        for candy in self.stack:
            y -= CANDY_HEIGHT
            # candy rectangle
            self.canvas.create_rectangle(
                100, y, 200, y + CANDY_HEIGHT,
                fill=candy.get("color", "pink"), outline="black"
            )
            # emoji centered
            self.canvas.create_text(
                150, y + CANDY_HEIGHT / 2,
                text=candy.get("emoji", "🍬"), font=("Arial", 14)
            )

        self.info.config(text=f"Candies: {len(self.stack)}/{MAX_CAPACITY}")

    # ------------ STACK METHODS ------------
    def add_candy(self):
        if len(self.stack) == MAX_CAPACITY:
            messagebox.showerror("Full", "Dispenser is FULL")
            return
        # pick a random emoji and color for the candy
        emojis = ['🍬', '🍭', '🍫', '🍪', '🧁', '🍩', '🍡']
        colors = ['pink', 'lightblue', 'lightgreen', 'yellow', 'orange', 'plum', 'salmon']
        candy = {"emoji": random.choice(emojis), "color": random.choice(colors)}
        self.stack.append(candy)
        # temporarily compress the spring visually
        self.temp_anim = 40
        self.animate()
        self.draw()

    def remove_candy(self):
        if not self.stack:
            messagebox.showwarning("Empty", "Dispenser is EMPTY")
            return
        self.stack.pop()
        # temporarily decompress the spring visually
        self.temp_anim = -40
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
        # simple animation that eases temp_anim back to 0
        steps = 10
        start = getattr(self, 'temp_anim', 0)
        for i in range(steps):
            # ease-out interpolation
            t = 1 - (i / steps)
            self.temp_offset = int(start * t)
            self.draw()
            self.root.update()
            self.root.after(30)
        self.temp_offset = 0
        # cleanup temp_anim attribute
        self.temp_anim = 0

# ---------------- RUN ----------------
root = tk.Tk()
app = CandyDispenser(root)
root.mainloop()
