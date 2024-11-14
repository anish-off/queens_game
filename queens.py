import tkinter as tk
from tkinter import messagebox

# Set up board size
N = 6  # Grid size (6 x 6)

# Define regions with unique identifiers for irregular shapes
regions = [
    [0, 0, 1, 1, 2, 2],
    [0, 3, 3, 1, 4, 2],
    [5, 3, 1, 4, 4, 6],
    [5, 7, 7, 8, 4, 6],
    [5, 9, 7, 8, 10, 10],
    [9, 9, 7, 8, 10, 10]
]

# Unique colors for each region
region_colors = [
    "#FFCCCB", "#ADD8E6", "#90EE90", "#FFD700", "#FFB6C1",
    "#20B2AA", "#9370DB", "#FF6347", "#4682B4", "#FFE4B5", "#7FFFD4"
]

# GUI setup
root = tk.Tk()
root.title("Interactive Queens Game")

# Board canvas setup
board_size = 400
cell_size = board_size // N
canvas = tk.Canvas(root, width=board_size, height=board_size)
canvas.pack()

# Initialize board
board = [["" for _ in range(N)] for _ in range(N)]
queens = set()

# Drawing the initial board with unique colored regions
def draw_board():
    canvas.delete("all")
    for row in range(N):
        for col in range(N):
            color = region_colors[regions[row][col]]
            canvas.create_rectangle(
                col * cell_size, row * cell_size,
                (col + 1) * cell_size, (row + 1) * cell_size,
                fill=color
            )
            if board[row][col] == "X":
                canvas.create_text(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2, text="X", font=("Arial", 18), fill="black")
            elif board[row][col] == "Q":
                canvas.create_text(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2, text="♕", font=("Arial", 18), fill="red")

# Check placement rules
def is_valid_placement(row, col):
    if any(board[row][c] == "Q" for c in range(N)) or \
       any(board[r][col] == "Q" for r in range(N)) or \
       any(board[r][c] == "Q" for r in range(N) for c in range(N) if regions[r][c] == regions[row][col]) or \
       any((0 <= row + dr < N and 0 <= col + dc < N and board[row + dr][col + dc] == "Q") 
           for dr in [-1, 0, 1] for dc in [-1, 0, 1] if dr != 0 or dc != 0):
        return False
    return True

# Handle cell click
def on_click(event):
    row, col = event.y // cell_size, event.x // cell_size
    if board[row][col] == "":
        if is_valid_placement(row, col):
            board[row][col] = "Q"
            queens.add((row, col))
        else:
            board[row][col] = "X"
    elif board[row][col] == "X":
        board[row][col] = ""
    elif board[row][col] == "Q":
        board[row][col] = ""
        queens.remove((row, col))
    draw_board()

# Check if the solution is correct
def is_solution_correct():
    for i in range(N):
        if sum(1 for j in range(N) if board[i][j] == "Q") != 1:
            return False
        if sum(1 for j in range(N) if board[j][i] == "Q") != 1:
            return False

    unique_regions = set(sum(regions, []))
    for region_id in unique_regions:
        if sum(1 for row in range(N) for col in range(N) if regions[row][col] == region_id and board[row][col] == "Q") != 1:
            return False

    for row in range(N):
        for col in range(N):
            if board[row][col] == "Q":
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < N and 0 <= nc < N and board[nr][nc] == "Q":
                            return False
    return True

# Submit answer
def submit_answer():
    if is_solution_correct():
        messagebox.showinfo("Correct!", "Congratulations, your solution is correct!")
    else:
        messagebox.showerror("Incorrect", "The current solution does not meet the game's requirements.")

# Add Submit button to check answer
submit_button = tk.Button(root, text="Submit Answer", command=submit_answer)
submit_button.pack()

# Draw the initial board and bind click
draw_board()
canvas.bind("<Button-1>", on_click)
root.mainloop()
