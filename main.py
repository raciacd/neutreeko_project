# Import the NeutreekoGame class and the execute_random_move function from the neutreeko.game module
from neutreeko.game import NeutreekoGame, execute_random_move
from ai.min_max import execute_minimax_move


# Define the main function of the program
def main():
    # Create an instance of the NeutreekoGame, passing execute_random_move as the function to control moves for both players
    game = NeutreekoGame(execute_random_move, execute_random_move)
    game.run_game() # Start the game

main()# Call the main function to start the program