import json
import sys

# Global variable keeps track of who played the first move of the game
was_first_move = False

# Function checks whether a winning move is possible
def check_for_win(grid, row, col, player):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # horizontal, vertical, diagonal right and left
    for row_dir, col_dir in directions:
        count = 0
        for i in range(-3, 4):  # Checking in both directions
            new_row = row + i * row_dir
            new_col = col + i * col_dir
            # Counting consecutive player pieces within the grid
            if 0 <= new_row < len(grid[0]) and 0 <= new_col < len(grid) and grid[new_col][new_row] == player:
                count += 1
                if count == 4:  # Sequence of 4 is a winning move
                    return True
            else:
                count = 0 # Reset sequence count
    return False

# Function determines the best move of whether to block or win
def best_move_for_player(precept, player):
    grid = precept["grid"]
    valid_columns = valid_moves(precept)
    
    for col in valid_columns:
        for row in range(len(grid[col]) - 1, -1, -1):
            if grid[col][row] == 0:  # If empty space
                grid[col][row] = player # try
                if check_for_win(grid, row, col, player): # Check winning space
                    grid[col][row] = 0
                    return col # Return best move
                grid[col][row] = 0
                break
    return None

# Finds valid columns (not full), to place pieces.
def valid_moves(precept):
    grid = precept["grid"]
    return [i for i, col in enumerate(grid) if col[0] == 0]

# Determines column that connects with player's neighbouring spaces
def neighboring_player_piece(precept, player):
    grid = precept["grid"]
    valid_columns = valid_moves(precept)

    for col in valid_columns:
        for row in range(len(grid[col]) - 1, -1, -1):
            if grid[col][row] == 0:
                # Check neighboring places for player pieces to place next to
                # Check left
                if col > 0 and grid[col - 1][row] == player:
                    return col
                # Check right
                if col < len(grid) - 1 and grid[col + 1][row] == player:
                    return col
                # Check below if there's another row
                if row < len(grid[0]) - 1 and grid[col][row + 1] == player:
                    return col
    return None

# Determines the move to be made
def determine_move(precept):
    global was_first_move
    
    # Checks first move, changes global variable
    if not was_first_move:
        was_first_move = True
        print("Starting new game. Playing first move in the center.", file=sys.stderr)
        return len(precept["grid"]) // 2
    
    player = precept["player"]
    opponent = 3 - player # Calculation to get opponent number (1 or 2)

    valid_moves_list = valid_moves(precept)
    if not valid_moves_list:
        print("Error: No valid moves available.", file=sys.stderr)
        return None
   
    # Check winning move for the player
    best_player_move = best_move_for_player(precept, player)
    if best_player_move is not None:
        print(f"Playing move {best_player_move} as a winning move for the player.", file=sys.stderr)
        return best_player_move
    
    # Check winning move for opponent for player to block
    best_opponent_move = best_move_for_player(precept, opponent)
    if best_opponent_move is not None:
        print(f"Playing move {best_opponent_move} to block opponent's winning path.", file=sys.stderr)
        return best_opponent_move
    
    # Play next to a neighboring player piece if possible
    next_to_player = neighboring_player_piece(precept, player)
    if next_to_player is not None:
        print(f"Playing move {next_to_player} next to a neighboring player piece.", file=sys.stderr)
        return next_to_player
    
    # Play in the center if possible or closest to it.
    center = len(precept["grid"]) // 2
    if center in valid_moves_list:
        print(f"Playing move {center} in the center.", file=sys.stderr)
        return center
    offset = 1
    while offset < len(precept["grid"]):
        # Check left-center
        if center - offset in valid_moves_list:
            print(f"Playing move {center - offset} closest to the center.", file=sys.stderr)
            return center - offset
        # Check right-center
        if center + offset in valid_moves_list:
            print(f"Playing move {center - offset} closest to the center.", file=sys.stderr)
            return center - offset
        offset += 1

# Main function from orginial program
def main():
    print('Connect Four in Python', file=sys.stderr)
    for line in sys.stdin:
        precept = json.loads(line)
        moves = valid_moves(precept)
        print(f"Received game state: {precept}", file=sys.stderr)
        print(f"Valid moves: {moves}", file=sys.stderr)
        move = determine_move(precept) # Determine move made by player
        action = {"move": move}
        action_json = json.dumps(action)
        print(action_json, flush=True)

if __name__ == '__main__':
    main()