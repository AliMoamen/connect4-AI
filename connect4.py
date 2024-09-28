import pygame
import time
import copy
import sys
import random
from collections import deque

class Connect4:
    """Class representing the Connect 4 game."""

    def __init__(self, row_count=6, col_count=7,multiplayer = False,pruning = True, simulate = False, aiplayer1_difficulty = 'Medium',aiplayer2_difficulty = 'Hard', depth = 5):
        """Initialize the Connect4 game."""
        self.row_count = row_count # Number of rows in the game board
        self.col_count = col_count # Number of columns in the game board
        self.multiplayer = multiplayer # Flag to indicate if the game is multiplayer
        self.aiplayer1_difficulty = aiplayer1_difficulty # Difficulty of the AI Player 1 if simulate mode is on
        self.aiplayer2_difficulty = aiplayer2_difficulty # Difficulty of the AI
        self.depth = depth # Depth of the minimax tree
        self.pruning = pruning # Flag to indicate if pruning is used
        self.nodes_count_aiplayer1 = []  # Initialize the list of nodes count for AI player 1
        self.execution_times_aiplayer1 = []  # Initialize the list of execution times for AI player 1
        self.nodes_count_aiplayer2 = []  # Initialize the list of nodes count for AI player 2
        self.execution_times_aiplayer2 = []  # Initialize the list of execution times for AI player 2
        self.winner = None # Winner of the game
        self.simulate = simulate # Flag to indicate if the game is being simulated
        self.player1_piece = 1 # Piece of player 1
        self.player2_piece = 2 # Piece of player 2
        self.squaresize = 100  # Size of each square on the game board
        self.radius = self.squaresize / 2 - 5  # Radius of each game piece
        self.board = [[0 for _ in range(col_count)] for _ in range(row_count)]  # Initialize the game board
        self.width = self.col_count * self.squaresize  # Width of the game window
        self.height = (self.row_count + 1) * self.squaresize  # Height of the game window
        pygame.init()  # Initialize pygame
        self.screen = pygame.display.set_mode((self.width, self.height))  # Create game window
        self.font = pygame.font.SysFont("calbri", 75)  # Font for displaying text
        # Define colors
        self.grey = (150, 150, 150)
        self.black = (100, 100, 100)
        self.red = (237, 22, 0)
        self.yellow = (255, 240, 0)
        # Initialize game variables
        self.turn = 0  # Player turn: 0 for player 1, 1 for player 2
        self.game_over = False  # Flag to indicate if the game is over

    def __str__(self):
        """Return a string representation of the board."""
        output = ""
        for row in self.board:
            output += '\n' + str(row)
        return output

    def drop_piece(self, col):
        """Drop a piece into the specified column."""
        if self.board[0][col] == 0:  # Check if the top row of the column is empty
            # Iterate through rows from bottom to top
            for row in range(len(self.board) - 1, -1, -1):
                if self.board[row][col] == 0:  # Find the first empty row in the column
                    self.turn += 1  # Increment turn counter
                    self.board[row][col] += self.turn  # Place player's piece in the board
                    self.turn %= 2  # Alternate player turn
                    return row  # Return the row where the piece was dropped

    def check_connection(self, piece, stack):
        """Check for a win condition based on the current piece and stack."""
        if piece == 0:
            stack = []  # If the current piece is empty, reset the stack
        elif stack and stack[-1] == piece:
            stack.append(piece)  # Add the piece to the stack
            if len(stack) >= 4:  # If there are four or more consecutive pieces
                return True, stack[-1]  # Return True for win and the winning piece
        else:
            stack = [piece]  # Start a new stack with the current piece
        return stack, None  # Return the updated stack and no winner

    def find_starting_diagonal(self, col_num, row_num, sign):
        """Find the starting point of a diagonal based on its direction."""
        if sign == 'positive':  # For positive diagonal
            jump = min(col_num, (self.row_count - 1) - row_num)  # Calculate jump distance
            point = [col_num - jump, row_num + jump]  # Calculate starting point
        elif sign == 'negative':  # For negative diagonal
            jump = min(col_num, row_num)  # Calculate jump distance
            point = [col_num - jump, row_num - jump]  # Calculate starting point
        return point  # Return the starting point
    
    def check_win(self, board, col_num, row_num):
        """Check for a win condition on the board."""
        if col_num == None and row_num == None:  # If the board is empty
            return False, None  # Return False for no win and no winner
        stack = []  # Initialize a stack to keep track of consecutive pieces

        # Check for horizontal win
        for piece in board[row_num]:  # Iterate through pieces in the current row
            stack, winner = self.check_connection(piece, stack)  # Check for consecutive pieces
            if stack == True:  # If there are four or more consecutive pieces
                return True, winner  # Return True for win and the winner's piece value

        # Check for vertical win
        stack = []  # Reset the stack for vertical check
        for row in range(len(board)):  # Iterate through rows in the board
            piece = board[row][col_num]  # Get the piece in the current column
            stack, winner = self.check_connection(piece, stack)  # Check for consecutive pieces
            if stack == True:  # If there are four or more consecutive pieces
                return True, winner  # Return True for win and the winner's piece value

        # Check for positive diagonal win
        positive_diagonal = self.find_starting_diagonal(col_num, row_num, 'positive')  # Find starting point for positive diagonal
        stack = []  # Reset the stack for diagonal check
        for row in range(positive_diagonal[1], -1, -1):  # Iterate through rows in the positive diagonal direction
            if positive_diagonal[0] == self.col_count or row == self.row_count:  # If out of bounds
                break
            piece = board[row][positive_diagonal[0]]  # Get the piece in the diagonal
            positive_diagonal[0] += 1  # Move to the next column in diagonal
            stack, winner = self.check_connection(piece, stack)  # Check for consecutive pieces
            if stack == True:  # If there are four or more consecutive pieces
                return True, winner  # Return True for win and the winner's piece value

        # Check for negative diagonal win
        negative_diagonal = self.find_starting_diagonal(col_num, row_num, 'negative')  # Find starting point for negative diagonal
        stack = []  # Reset the stack for diagonal check
        for row in range(negative_diagonal[1], self.row_count):  # Iterate through rows in the negative diagonal direction
            if negative_diagonal[0] == self.col_count or row == self.row_count:  # If out of bounds
                break
            piece = board[row][negative_diagonal[0]]  # Get the piece in the diagonal
            stack, winner = self.check_connection(piece, stack)  # Check for consecutive pieces
            if stack == True:  # If there are four or more consecutive pieces
                return True, winner  # Return True for win and the winner's piece value
            negative_diagonal[0] += 1  # Move to the next column in diagonal

        return False, None  # Return False for no win, and no winner's piece value

    def check_draw(self):
        """Check if the game has ended in a draw."""
        return self.board[0].count(0) == 0
    
    def draw_board(self):
        
        """Draw the game board."""
        # Draw background rectangle for the board
        pygame.draw.rect(self.screen, self.black, (0, 0, self.width, self.squaresize))
        # Loop through each column and row to draw the grid and pieces
        for col in range(self.col_count):
            for row in range(self.row_count):
                # Draw the grid squares
                pygame.draw.rect(self.screen, self.grey, (col * self.squaresize, row * self.squaresize + self.squaresize, self.squaresize, self.squaresize))
                # Draw the pieces based on their values in the board matrix
                if self.board[row][col] == 0:
                    pygame.draw.circle(self.screen, self.black, (int(col * self.squaresize + self.squaresize / 2), int(row * self.squaresize + self.squaresize + self.squaresize / 2)), self.radius)
                elif self.board[row][col] == 1:
                    pygame.draw.circle(self.screen, self.red, (int(col * self.squaresize + self.squaresize / 2), int(row * self.squaresize + self.squaresize + self.squaresize / 2)), self.radius)
                else:
                    pygame.draw.circle(self.screen, self.yellow, (int(col * self.squaresize + self.squaresize / 2), int(row * self.squaresize + self.squaresize + self.squaresize / 2)), self.radius)
        pygame.display.update()  # Update the display to show changes
    
    def select_piece(self, col_num):
        """
        Select a piece to display on hover.
        """
        pygame.draw.rect(self.screen, self.black, (0, 0, self.width, self.squaresize))
        if self.turn == 0:  # If it's player 1's turn
            # Draw a circle with red color representing player 1's piece
            pygame.draw.circle(self.screen, self.red, (int(col_num * self.squaresize + self.squaresize / 2), int(self.squaresize / 2)), self.radius)
        else:  # If it's player 2's turn
            # Draw a circle with yellow color representing player 2's piece
            pygame.draw.circle(self.screen, self.yellow, (int(col_num * self.squaresize + self.squaresize / 2), int(self.squaresize / 2)), self.radius)
        pygame.display.update()  # Update the display to show changes

    def get_stats(self):
        return self.nodes_count_aiplayer1,self.execution_times_aiplayer1,self.nodes_count_aiplayer2,self.execution_times_aiplayer2,self.winner
    
    def start_game(self):
        """Start the Connect4 game."""
        self.draw_board()  # Draw the initial game board
        aiplayer1 = AIPlayer(self.row_count, self.col_count,self.player1_piece,self.aiplayer1_difficulty, self.pruning, self.depth)  # Initialize AI player 1
        aiplayer2 = AIPlayer(self.row_count, self.col_count,self.player2_piece,self.aiplayer2_difficulty, self.pruning, self.depth)  # Initialize AI player 2
        col_num, row_num = None, None  # Initialize variables for column and row
        while not self.game_over:
            played = False  # Flag to indicate if a move has been made
            for event in pygame.event.get():  # Check for events
                if event.type == pygame.QUIT:  # If user quits the game
                    sys.exit(0)  # Exit the program
                
                if not self.simulate and event.type == pygame.MOUSEMOTION:  # If mouse is moved
                    col_num = event.pos[0] // self.squaresize  # Calculate column number
                    self.select_piece(col_num)  # Highlight the selected column
                
                if not self.simulate and (self.turn == 0 or self.turn == 1) and event.type == pygame.MOUSEBUTTONDOWN:  # If it's player's turn and mouse button is clicked
                    col_num = event.pos[0] // self.squaresize  # Calculate column number
                    played = True  # Mark that a move has been played

                if self.simulate and self.turn == 0:  # If it's AI player1's turn if simulation mode is on s
                    output = aiplayer1.select_move(self.board, col_num, row_num) # AI player selects a move
                    col_num = output[0]
                    self.nodes_count_aiplayer1 += output[1]
                    self.execution_times_aiplayer1 += output[2]
                    played = True  # Mark that a move has been played

                elif not self.multiplayer and self.turn == 1:  # If it's AI player2's turn
                    output = aiplayer2.select_move(self.board, col_num, row_num) # AI player selects a move
                    col_num = output[0]
                    self.nodes_count_aiplayer2 += output[1]
                    self.execution_times_aiplayer2 += output[2]
                    played = True # Mark that a move has been played
                if played and col_num != None:  # If a move has been played
                    row_num = self.drop_piece(int(col_num))  # Drop the piece into the selected column
                    self.draw_board()  # Redraw the game board
                    if self.multiplayer:
                        self.select_piece(col_num)
                    if row_num is not None:  # If a piece is successfully dropped
                        win, winner = self.check_win(self.board, int(col_num), row_num)  # Check for win
                        self.winner = winner
                        if win:  # If there is a winner
                            label = self.font.render(f"Player 1 Wins!", 1, self.red) if self.turn == 1 else self.font.render(f"Player 2 Wins!", 1, self.yellow)
                            pygame.draw.rect(self.screen, self.black, (0, 0, self.width, self.squaresize))
                            self.screen.blit(label, (self.width / 4, self.squaresize / 4))  # Display winner message
                            pygame.display.update()  # Update the display
                            self.game_over = True  # Mark game as over
                            pygame.time.wait(3000)  # Wait for 3 seconds

                        elif self.check_draw():  # If it's a draw
                            print(f'Draw!')
                            label = self.font.render(f"Draw!", 1, self.grey)
                            pygame.draw.rect(self.screen, self.black, (0, 0, self.width, self.squaresize))
                            self.screen.blit(label, (self.width / 2.5, self.squaresize / 4))  # Display draw message
                            pygame.display.update()  # Update the display
                            self.game_over = True  # Mark game as over
                            pygame.time.wait(3000)  # Wait for 3 seconds

                    if self.simulate:
                        pygame.time.wait(500)

class AIPlayer(Connect4):
    """Class representing the AI player."""

    def __init__(self, row_count, col_count, ai_piece, difficulty, pruning, depth):
        """Initialize the AIPlayer."""
        self.row_count = row_count  # Set the number of rows in the game board
        self.col_count = col_count  # Set the number of columns in the game board
        self.ai_piece = ai_piece  # Set the piece of the AI
        self.opponent_piece = 1 if ai_piece == 2 else 2  # Set the piece of the opponent
        self.difficulty = difficulty # Set the Diffculty of the AI
        self.pruning = pruning  # Set the Pruning of the AI
        self.depth = depth #Set the depth of Minimax
        self.total_nodes_evaluated = 0  # Initialize the count of nodes evaluated
        self.nodes_count = []  # Initialize the list of nodes count
        self.execution_times = []  # Initialize the list of execution times

    def give_score(self, pieces):
        """Calculate the score based on the pieces."""
        score = 0  # Initialize score
        ai_pieces_count = pieces.count(self.ai_piece)
        empty_spaces = pieces.count(0)  # Count the number of empty spaces in the list of pieces
        if ai_pieces_count == 3 and empty_spaces == 1:  # If AI has three consecutive pieces and one empty space
            score += 10  # Add a high score
        elif ai_pieces_count == 2 and empty_spaces == 2:  # If AI has two consecutive pieces and two empty spaces
            score += 5  # Add a medium score
        return score  # Return the calculated score

    def evaluate_state(self, board):
        """Evaluate the current state of the board."""
        score = 0  # Initialize score
        center_pieces = [board[row][self.col_count // 2] for row in range(self.row_count)]  # Get pieces in the center column
        score += center_pieces.count(self.ai_piece) * 4  # Increase score based on AI's pieces in the center

        for row in board:  # Loop through rows in the board
            horizontal_row = deque()  # Initialize deque to track consecutive pieces in a row
            for piece in row:  # Loop through pieces in the row
                horizontal_row.append(piece)  # Add piece to deque
                if len(horizontal_row) > 4:  # If deque exceeds size limit
                    horizontal_row.popleft()  # Remove the leftmost piece
                score += self.give_score(horizontal_row)  # Calculate score based on consecutive pieces

        for col in range(self.col_count):  # Loop through columns in the board
            vertical_column = deque()  # Initialize deque to track consecutive pieces in a column
            for row in range(self.row_count):  # Loop through rows in the column
                piece = board[row][col]  # Get piece in the column
                vertical_column.append(piece)  # Add piece to deque
                if len(vertical_column) > 4:  # If deque exceeds size limit
                    vertical_column.popleft()  # Remove the topmost piece
                score += self.give_score(vertical_column)  # Calculate score based on consecutive pieces

        positive_diagonal_starting_points = [[0, row] for row in range(self.row_count)]  # Starting points for positive diagonals
        positive_diagonal_starting_points += [[col, self.row_count - 1] for col in range(1, self.col_count)]  # Additional starting points
        for positive_diagonal in positive_diagonal_starting_points:  # Loop through starting points
            positive_diagonal_pieces = deque()  # Initialize deque to track consecutive pieces in a diagonal
            for row in range(positive_diagonal[1], -1, -1):  # Iterate through rows in the positive diagonal direction
                if positive_diagonal[0] == self.col_count or row == self.row_count:  # If out of bounds
                    break
                piece = board[row][positive_diagonal[0]]  # Get piece in the diagonal
                positive_diagonal_pieces.append(piece)  # Add piece to deque
                if len(positive_diagonal_pieces) > 4:  # If deque exceeds size limit
                    positive_diagonal_pieces.popleft()  # Remove the leftmost piece
                score += self.give_score(positive_diagonal_pieces)  # Calculate score based on consecutive pieces
                positive_diagonal[0] += 1  # Move to the next column in diagonal

        negative_diagonal_starting_points = [[col, 0] for col in range(self.col_count - 1, -1, -1)]  # Starting points for negative diagonals
        negative_diagonal_starting_points += [[0, row] for row in range(1, self.row_count)]  # Additional starting points
        for negative_diagonal in negative_diagonal_starting_points:  # Loop through starting points
            negative_diagonal_pieces = deque()  # Initialize deque to track consecutive pieces in a diagonal
            for row in range(negative_diagonal[1], self.row_count):  # Iterate through rows in the negative diagonal direction
                if negative_diagonal[0] == self.col_count or row == self.row_count:  # If out of bounds
                    break
                piece = board[row][negative_diagonal[0]]  # Get piece in the diagonal
                negative_diagonal_pieces.append(piece)  # Add piece to deque
                if len(negative_diagonal_pieces) > 4:  # If deque exceeds size limit
                    negative_diagonal_pieces.popleft()  # Remove the leftmost piece
                score += self.give_score(negative_diagonal_pieces)  # Calculate score based on consecutive pieces
                negative_diagonal[0] += 1  # Move to the next column in diagonal

        return score  # Return the evaluated score

    def valid_moves(self, board):
        """Return a list of valid moves."""
        valid = []  # Initialize list of valid moves
        for col in range(self.col_count):  # Loop through columns in the board
            if board[0][col] == 0:  # If the column is not full
                valid.append(col)  # Add column to list of valid moves
        return valid  # Return the list of valid moves

    def is_terminal_node(self, board, col_num, row_num):
        """Check if the current node is terminal."""
        if col_num != None:
          win, _ = self.check_win(board, col_num, row_num)  # Check for win
          return win or len(self.valid_moves(board)) == 0  # Return True if win or no valid moves left
        return len(self.valid_moves(board)) == 0

    def generate_successor(self, board, col, player_piece):
        """Generate the successor state after a move."""
        state = copy.deepcopy(board)  # Create a deep copy of the current board state
        for row in range(self.row_count - 1, -1, -1):  # Iterate through rows in the column
            if state[row][col] == 0:  # If the cell is empty
                expected_row = row  # Assign the row where the piece will be placed
                break
        state[expected_row][col] = player_piece  # Place the piece in the expected row
        return state, expected_row  # Return the successor state and the row where the piece was placed

    def minimax(self, board, depth, alpha, beta, maximizingPlayer, col_num, row_num):
        """Implementation of the minimax algorithm."""
        self.total_nodes_evaluated += 1  # Increment the count of nodes evaluated
        valid_moves = self.valid_moves(board)  # Get valid moves
        is_terminal = self.is_terminal_node(board, col_num, row_num)  # Check if terminal node reached

        if depth == 0 or is_terminal:  # If maximum depth reached or terminal node
            if is_terminal:  # If terminal node
                _, winner = self.check_win(board, col_num, row_num)  # Check for winner
                if winner ==  self.ai_piece:  # If AI wins
                    return float('inf'), None  # Return positive infinity score
                elif winner == self.opponent_piece:  # If other player wins
                    return float('-inf'), None  # Return negative infinity score
                else:  # If draw
                    return 0, None  # Return a neutral score
            else:  # If maximum depth reached
                return self.evaluate_state(board), None  # Evaluate the state and return the score

        if maximizingPlayer:  # If AI's turn
            max_score = float('-inf')  # Initialize max score
            best_move = random.choice(valid_moves)  # Randomly choose a move initially
            for col in valid_moves:  # Loop through valid moves
                state, expected_row = self.generate_successor(board, col, self.ai_piece)  # Generate successor state
                score = self.minimax(state, depth - 1, alpha, beta, False, col, expected_row)[0]  # Recursively call minimax for the next state
                if score > max_score:  # If higher score found
                    max_score = score  # Update max score
                    best_move = col  # Update best move
                alpha = max(alpha, max_score)  # Update alpha value
                if self.pruning: #If alpha-beta pruning is enabled
                  if alpha >= beta:  # If alpha cutoff occurs
                      break  # Break the loop
            return max_score, best_move  # Return max score and best move
        else:  # If other player's turn
            min_score = float('inf')  # Initialize min score
            best_move = random.choice(valid_moves)  # Randomly choose a move initially
            for col in valid_moves:  # Loop through valid moves
                state, expected_row = self.generate_successor(board, col,self.opponent_piece)  # Generate successor state
                score = self.minimax(state, depth - 1, alpha, beta, True, col, expected_row)[0]  # Recursively call minimax for the next state
                if score < min_score:  # If lower score found
                    min_score = score  # Update min score
                    best_move = col  # Update best move
                if self.pruning: #If alpha-beta pruning is enabled
                  beta = min(beta, min_score)  # Update beta value
                  if alpha >= beta:  # If beta cutoff occurs
                      break  # Break the loop
            return min_score, best_move  # Return min score and best move

    def select_move(self, board, col_num, row_num):
        """Select the best move using the minimax algorithm."""
        difficulty_probabilities = {'Easy':0.4,'Medium':0.8,'Hard': 1} #Probabilites of Choosing Optimal Move
        probability = random.uniform(0,1)
        if probability > difficulty_probabilities[self.difficulty]:
            return random.choice(self.valid_moves(board)),[],[]
        else:
          start_time = time.time()  # Record the start time
          result = self.minimax(board, self.depth, float('-inf'), float('inf'), True, col_num, row_num)  # Call minimax to select the best move
          end_time = time.time()  # Record the end time
          execution_time = end_time - start_time  # Calculate the execution time
          self.execution_times.append(execution_time)

        # Print metrics
        self.nodes_count.append(self.total_nodes_evaluated)
        self.total_nodes_evaluated = 0

        return result[1],[self.nodes_count[-1]],[execution_time] # Return the selected move


if __name__ == "__main__":
    game = Connect4(aiplayer2_difficulty='Hard') #Sample Game with Hard AI Opponent 
    game.start_game()