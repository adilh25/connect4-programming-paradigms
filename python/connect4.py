
import random

# Connect 4 Game
# Language - Python
# Paradigm - Procedural

board = [
    ["_"] * 7,
    ["_"] * 7,
    ["_"] * 7,
    ["_"] * 7,
    ["_"] * 7,
    ["_"] * 7
]

# Each player has one bomb
bombs = {"X": True, "O": True}


# Display the board
def display_board():
    print("0 1 2 3 4 5 6")
    for row in board:
        print(" ".join(row))
    print()


# Drop a piece into a column
def drop_piece(column, player):
    for row in range(5, -1, -1):
        if board[row][column] == "_":
            board[row][column] = player
            return row
    return -1


# Remove the top piece from a column
def bomb_piece(column):
    for row in range(6):
        if board[row][column] != "_":
            board[row][column] = "_"
            return True
    return False


# Check if a player has won
def winner(player):

    # Horizontal
    for row in range(6):
        for col in range(4):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                return True

    # Vertical
    for row in range(3):
        for col in range(7):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Diagonal down-right
    for row in range(3):
        for col in range(4):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Diagonal down-left
    for row in range(3):
        for col in range(3, 7):
            if board[row][col] == player and board[row + 1][col - 1] == player and board[row + 2][col - 2] == player and board[row + 3][col - 3] == player:
                return True

    return False


# Find columns that are not full
def valid_columns():
    columns = []

    for col in range(7):
        if board[0][col] == "_":
            columns.append(col)

    return columns


# Check if a move would win
def would_win(column, player):
    row = drop_piece(column, player)

    if row == -1:
        return False

    result = winner(player)

    # Undo the test move
    board[row][column] = "_"

    return result


# Human player's turn
def take_turn(player):
    while True:
        print("Player " + player + "'s turn")

        if bombs[player]:
            choice = input("Choose column (0-6) or B for bomb: ")
        else:
            choice = input("Choose column (0-6): ")

        # Use a bomb
        if choice.lower() == "b" and bombs[player]:
            choice = input("Column to bomb (0-6): ")

            if choice.isdigit() and int(choice) in range(7):
                if bomb_piece(int(choice)):
                    bombs[player] = False
                    return

            print("Invalid bomb column")

        # Drop a piece
        elif choice.isdigit() and int(choice) in range(7):
            if drop_piece(int(choice), player) != -1:
                return

            print("Column is full")

        else:
            print("Invalid choice")


# AI opponent
def ai_turn():
    print("AI's turn")
    columns = valid_columns()

    # Try to win
    for col in columns:
        if would_win(col, "O"):
            drop_piece(col, "O")
            print("AI chose column", col)
            return

    # Block player X
    for col in columns:
        if would_win(col, "X"):
            drop_piece(col, "O")
            print("AI chose column", col)
            return

    # Use bomb if the centre is full and X is on top
    if bombs["O"] and 3 not in columns and board[0][3] == "X":
        bomb_piece(3)
        bombs["O"] = False
        print("AI bombed column 3")
        return

    # Prefer the centre column
    if 3 in columns:
        col = 3
    else:
        col = random.choice(columns)

    drop_piece(col, "O")
    print("AI chose column", col)


# Main game loop
def game_loop():
    player = "X"

    while True:
        display_board()

        if not valid_columns():
            print("It's a draw")
            break

        if player == "X":
            take_turn("X")
        else:
            ai_turn()

        if winner(player):
            display_board()
            print("Player " + player + " wins")
            break

        # Change player
        if player == "X":
            player = "O"
        else:
            player = "X"


def main():
    game_loop()


if __name__ == "__main__":
    main()
