import customtkinter as ctk
import tkinter.messagebox as messagebox
import math

# Constants
HUMAN = 'O'
AI = 'X'
EMPTY = ' '

# Initialize the board
board = [[EMPTY for _ in range(3)] for _ in range(3)]

def is_winner(board, player):
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

def is_board_full(board):
    return all([cell != EMPTY for row in board for cell in row])

def get_available_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == EMPTY]

def minimax(board, depth, is_maximizing, alpha, beta):
    if is_winner(board, AI):
        return 10 - depth
    if is_winner(board, HUMAN):
        return depth - 10
    if is_board_full(board):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for (r, c) in get_available_moves(board):
            board[r][c] = AI
            eval = minimax(board, depth + 1, False, alpha, beta)
            board[r][c] = EMPTY
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for (r, c) in get_available_moves(board):
            board[r][c] = HUMAN
            eval = minimax(board, depth + 1, True, alpha, beta)
            board[r][c] = EMPTY
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def best_move(board):
    best_val = -math.inf
    move = None
    for (r, c) in get_available_moves(board):
        board[r][c] = AI
        move_val = minimax(board, 0, False, -math.inf, math.inf)
        board[r][c] = EMPTY
        if move_val > best_val:
            best_val = move_val
            move = (r, c)
    return move

def on_button_click(row, col):
    if board[row][col] != EMPTY:
        return
    board[row][col] = HUMAN
    buttons[row][col].configure(text=HUMAN)
    if is_winner(board, HUMAN):
        messagebox.showinfo("Tic-Tac-Toe", "You win!")
        reset_board()
        return
    if is_board_full(board):
        messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
        reset_board()
        return
    ai_move = best_move(board)
    board[ai_move[0]][ai_move[1]] = AI
    buttons[ai_move[0]][ai_move[1]].configure(text=AI)
    if is_winner(board, AI):
        messagebox.showinfo("Tic-Tac-Toe", "AI wins!")
        reset_board()
        return
    if is_board_full(board):
        messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
        reset_board()

def reset_board():
    global board
    board = [[EMPTY for _ in range(3)] for _ in range(3)]
    for row in range(3):
        for col in range(3):
            buttons[row][col].configure(text=EMPTY)

app = ctk.CTk()
app.title("Tic-Tac-Toe")

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=20)

buttons = [[None for _ in range(3)] for _ in range(3)]

for row in range(3):
    for col in range(3):
        buttons[row][col] = ctk.CTkButton(master=frame, text=EMPTY, width=100, height=100, font=("Arial", 32), command=lambda r=row, c=col: on_button_click(r, c))
        buttons[row][col].grid(row=row, column=col, padx=5, pady=5)

reset_button = ctk.CTkButton(master=app, text="Reset", font=("Arial", 20), command=reset_board)
reset_button.pack(pady=10)

app.mainloop()
