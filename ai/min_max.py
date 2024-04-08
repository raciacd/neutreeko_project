
def execute_minimax_move(evaluate_func, depth):
    def execute_minimax_move_aux(game):
        # updates the game state to the best possible move (uses minimax to determine it)
        # your code here
        #--------------------------------------------------#
        best_move = None
        best_eval = float('-inf')
        for move in game.board.available_moves:
            new_state = game.board.move(move)
            # maximizing = False because we are checking for the best moves for the opponent after this move
            new_state_eval = minimax(new_state, depth - 1, float('-inf'), float('+inf'), False, game.board.current_player, evaluate_func)

            if new_state_eval > best_eval:
                best_move = new_state
                best_eval = new_state_eval
        game.board = best_move
        
    return execute_minimax_move_aux

def minimax(state, depth, alpha, beta, maximizing, player, evaluate_func): #state - new state (estado atual do tabuleiro)
    if depth == 0 or state.winner != -1:
        return evaluate_func(state) * (1 if player == 1 else -1)
    
    if maximizing:
        max_eval = float('-inf')
        for move in state.available_moves:
            new_state = state.move(move)
            eval = minimax(new_state, depth - 1, alpha, beta, False, player, evaluate_func)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in state.available_moves:
            new_state = state.move(move)
            eval = minimax(new_state, depth - 1, alpha, beta, True, player, evaluate_func)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
    
# Heuristic functions
def evaluate_f1(board): #Contagem de Alinhamentos Potenciais
    pieces = board.pieces[board.current_player]
    if (pieces[0][0], pieces[0][1]) == pieces[1]:
        print()
