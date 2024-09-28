from connect4 import Connect4  # Import the Connect4 class from the connect4.py
import os  # Import the os module for system-related functionalities

def play_multiplayer():
    """
    Start a multiplayer Connect4 game.
    """
    game = Connect4(multiplayer=True)  # Create a Connect4 object for multiplayer game
    game.start_game()  # Start the game

def play_with_ai(difficulty, pruning=True):
    """
    Start a Connect4 game against an AI player.
    
    Parameters:
        difficulty (str): The difficulty level of the AI player ('Easy', 'Medium', or 'Hard').
        pruning (bool): A flag indicating whether alpha-beta pruning should be enabled (default is True).
    """
    game = Connect4(aiplayer2_difficulty=difficulty, pruning=pruning)  # Create a Connect4 object for AI game
    game.start_game()  # Start the game

def simulate_ai_game(aiplayer1_difficulty, aiplayer2_difficulty, depth=5, pruning=True):
    """
    Simulate a Connect4 game between two AI players.
    
    Parameters:
        aiplayer1_difficulty (str): The difficulty level of AI player 1 ('Easy', 'Medium', or 'Hard').
        aiplayer2_difficulty (str): The difficulty level of AI player 2 ('Easy', 'Medium', or 'Hard').
        depth (int): The depth of the minimax algorithm (default is 5).
        pruning (bool): A flag indicating whether alpha-beta pruning should be enabled (default is True).
    
    Returns:
        tuple: A tuple containing the statistics of the game.
    """
    game = Connect4(aiplayer1_difficulty=aiplayer1_difficulty, aiplayer2_difficulty=aiplayer2_difficulty, 
                    depth=depth, pruning=pruning, simulate=True)  # Create a Connect4 object for simulation
    game.start_game()  # Start the game
    return game.get_stats()  # Return the game statistics

def benchmark(aiplayer1_difficulty, aiplayer2_difficulty, depth):
    """
    Benchmark the performance of AI players in a simulated Connect4 game.
    
    Parameters:
        aiplayer1_difficulty (str): The difficulty level of AI player 1 ('Easy', 'Medium', or 'Hard').
        aiplayer2_difficulty (str): The difficulty level of AI player 2 ('Easy', 'Medium', or 'Hard').
        depth (int): The depth of the minimax algorithm.
    """
    os.system('cls')  # Clear the console screen
    # Simulate a game without pruning
    output_without_pruning = simulate_ai_game(aiplayer1_difficulty=aiplayer1_difficulty, 
                                               aiplayer2_difficulty=aiplayer2_difficulty, 
                                               pruning=False, depth=depth)
    print("Stats Without Pruning")
    # Print statistics
    print(f"Player 1's Average Evaluated Nodes Per Move: {round(sum(output_without_pruning[0])/len(output_without_pruning[0]),2)} nodes")
    print(f"Player 1's Average Evaluation Time Per Move: {round(sum(output_without_pruning[1])/len(output_without_pruning[1]),2)} seconds")
    print(f"Player 2's Average Evaluated Nodes Per Move: {round(sum(output_without_pruning[2])/len(output_without_pruning[2]),2)} nodes")
    print(f"Player 2's Average Evaluation Time Per Move: {round(sum(output_without_pruning[3])/len(output_without_pruning[3]),2)} seconds")
    print(f"Player {output_without_pruning[4]} wins the game !")
    print('----------------------------------------------')
   
    # Simulate a game with pruning
    output_with_pruning = simulate_ai_game(aiplayer1_difficulty=aiplayer1_difficulty, 
                                           aiplayer2_difficulty=aiplayer2_difficulty, 
                                           pruning=True, depth=depth)
    print("Stats With Pruning")
    # Print statistics
    print(f"Player 1's Average Evaluated Nodes Per Move: {round(sum(output_with_pruning[0])/len(output_with_pruning[0]),2)} nodes")
    print(f"Player 1's Average Evaluation Time Per Move: {round(sum(output_with_pruning[1])/len(output_with_pruning[1]),2)} seconds")
    print(f"Player 2's Average Evaluated Nodes Per Move: {round(sum(output_with_pruning[2])/len(output_with_pruning[2]),2)} nodes")
    print(f"Player 2's Average Evaluation Time Per Move: {round(sum(output_with_pruning[3])/len(output_with_pruning[3]),2)} seconds")
    print(f"Player {output_with_pruning[4]} wins the game !")

# Benchmark the performance of AI players
benchmark("Hard", "Medium", 3)
# You can experiment with different AI players and depth values to see how the performance changes. Also, you can use play_multiplayer() and play_with_ai() to play a game with a human player or an AI, respectively.
