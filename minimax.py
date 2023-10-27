from math import inf as infinity

class TicTacToe:
    def __init__(self):
        X, O = "X", "O"
        self.first_move = "O"
        self.debug_board = [None,
                            X, O, O,
                            4, O, 6,
                            "", X, 9]
        self.board = [None] + [x for x in range(1, 10)]
        self.WIN_COMBINATIONS = [(1, 2, 3),
                                 (4, 5, 6),
                                 (7, 8, 9),
                                 (1, 4, 7),
                                 (2, 5, 8),
                                 (3, 6, 9),
                                 (1, 5, 9),
                                 (3, 5, 7)]
        self.game_running = True

    def draw_board(self, board = None):
        if board == None: board = self.board
        print("{} | {} | {}".format(board[1], board[2], board[3]))
        print("----------")
        print("{} | {} | {}".format(board[4], board[5], board[6]))
        print("----------")
        print("{} | {} | {}".format(board[7], board[8], board[9]))
        print()

    def get_opponent(self, player):
        if player == "X":
            return "O"
        else:
            return "X"

    def evaluate(self, board):
        if self.check_win(board)[1] == "X":
            return -1
        elif self.check_win(board)[1] == "O":
            return 1
        else:
            return 0

    def check_win(self, board = None):
        if board == None: board = self.board
        for a, b, c in self.WIN_COMBINATIONS:
            if board[a] == board[b] == board[c] == "X":
                return (True, "X")
            elif board[a] == board[b] == board[c] == "O":
                return (True, "O")
        else: return (False, None)

    def check_tie(self):
        empty_cells = 0
        for cell in self.board[1:10]:
            if isinstance(cell, int):
                empty_cells += 1
        if empty_cells == 0:
            return True
        else: return False

    def get_empty_cells(self, board = None):
        if board == None: board = self.board
        empty_cells = []
        for cell in board[1:10]:
            if isinstance(cell, int):
                empty_cells.append(cell)
        return empty_cells

    def player_move(self):
        try:
            selected_cell = int(input("Enter cell index: "))
        except:
            #DEBUG
            if selected_cell == "stop": assert KeyError
            #DEBUG
            print("Invalid cell index.")
            self.player_move()
        if selected_cell in self.get_empty_cells():
            self.board[selected_cell] = "X"
            print("You selected cell {} for X.\n".format(selected_cell))
            self.draw_board()
        else:
            print("Invalid cell index.")
            self.player_move()

    def computer_move(self):
        selected_cell = self.calculate_best_move()[0]
        print(selected_cell)
        self.board[selected_cell] = "O"
        print("Computer selected cell {} for O.\n".format(selected_cell))
        self.draw_board()

    def calculate_best_move(self):
        depth = len(self.get_empty_cells())
        if depth == 9:
            return [1, None]
        return self.minimax(self.board, len(self.get_empty_cells()), "O")

    def minimax(self, board, depth, player):
        if player == "X":
            best = [-1, +infinity]
        else:
            best = [-1, -infinity]

        if depth == 0 or self.check_win()[0] or self.check_tie(): #SA ADAUG SI self.check_tie DACA NU MERGE
            score = self.evaluate(board)
            return [-1, score]

        for cell in self.get_empty_cells(board):
            board[cell] = player
            score = self.minimax(board, depth - 1, self.get_opponent(player))
            board[cell] = cell
            score[0] = cell
            if player == "O":
                if score[1] > best[1]:
                    best = score
            else:
                if score[1] < best[1]:
                    best = score

        return best

    def run(self):
        game.draw_board()
        while self.game_running:
            if self.first_move == "X":
                game.player_move()
                if game.check_win()[0] == True and game.check_win()[1] == "X":
                    print("Player won the game!")
                    break
                if game.check_tie():
                    print("Tie!")
                    break
                game.computer_move()
                if game.check_win()[0] == True and game.check_win()[1] == "O":
                    print("Computer won the game!")
                    break
                if game.check_tie():
                    print("Tie!")
                    break
            if self.first_move == "O":
                game.computer_move()
                if game.check_win()[0] == True and game.check_win()[1] == "O":
                    print("Computer won the game!")
                    break
                if game.check_tie():
                    print("Tie!")
                    break
                game.player_move()
                if game.check_win()[0] == True and game.check_win()[1] == "X":
                    print("Player won the game!")
                    break
                if game.check_tie():
                    print("Tie!")
                    break

game = TicTacToe()
game.run()