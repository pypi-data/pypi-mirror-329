import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Listbox
import pyperclip  # Import pyperclip to copy to clipboard

class Coordinates:
    def __init__(self, root):
        self.root = root
        self.root.title("Coordinates Obtainter.")
        messagebox.showwarning("Very important thing to note", "This app is very weird so don't commit a mistake :).")

        # Ask for width and height on launch
        self.width = simpledialog.askinteger("Board Width", "Enter the width of the board:")
        self.height = simpledialog.askinteger("Board Height", "Enter the height of the board:")

        if self.width is None or self.height is None:
            messagebox.showerror("Invalid Input", "Width and Height must be provided!")
            self.root.quit()
            return
        
        # Initialize the board as a 2D list
        self.board = [['' for _ in range(self.width)] for _ in range(self.height)]
        
        # Set up the drawing canvas
        self.canvas = tk.Canvas(self.root, width=self.width * 30, height=self.height * 30)
        self.canvas.pack()

        self.draw_board()

        # Option to draw borders
        self.borderSprite = "X"  # Representing borders with 'X'
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Start button to allow drawing borders
        self.draw_button = tk.Button(self.root, text="Draw Borders", command=self.draw_borders)
        self.draw_button.pack()

        # Add a "Copy Coordinates" button
        self.copy_button = tk.Button(self.root, text="Copy Coordinates", command=self.copy_coordinates)
        self.copy_button.pack()

    def draw_board(self):
        for y in range(self.height):
            for x in range(self.width):
                self.canvas.create_rectangle(x * 30, y * 30, (x + 1) * 30, (y + 1) * 30, outline="black", width=1)

    def on_canvas_click(self, event):
        # Get grid position based on click
        x = event.x // 30
        y = event.y // 30
        if 0 <= x < self.width and 0 <= y < self.height:
            self.board[y][x] = self.borderSprite  # Mark border position
            self.canvas.create_text(x * 30 + 15, y * 30 + 15, text=self.borderSprite, font=("Arial", 12))

    def draw_borders(self):
        # Create the popup window to display the list of coordinates
        popup = Toplevel(self.root)
        popup.title("Borders Coordinates")

        # Create a Listbox to display the coordinates
        listbox = Listbox(popup, width=20, height=10)
        listbox.pack()

        # Collect all coordinates with the 'X' mark
        border_coords = []
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == self.borderSprite:
                    border_coords.append((x, y))

        # Add coordinates to the Listbox
        for coord in border_coords:
            listbox.insert(tk.END, str(coord))

    def copy_coordinates(self):
        # Collect all coordinates with the 'X' mark
        border_coords = []
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == self.borderSprite:
                    border_coords.append((x, y))

        # Prepare the coordinates as a string in the format (x, y), (x, y), ...
        coords_string = ", ".join([f"({x}, {y})" for x, y in border_coords])

        if coords_string:
            # Copy the coordinates to the clipboard
            pyperclip.copy(coords_string)
            messagebox.showinfo("Copied", "Coordinates copied to clipboard!")
        else:
            messagebox.showinfo("No Borders", "No borders to copy!")

def launch():
    root = tk.Tk()
    app = Coordinates(root)
    root.mainloop()