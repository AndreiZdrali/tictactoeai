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

    def test_win_move(self, mark, j, board = None):
        if board == None: board = self.board
        board_copy = [n for n in board]
        board_copy[j] = mark
        return self.check_win(board_copy)[0]

    def test_fork_move(self, mark, i, board = None):
        if board == None: board = self.board
        board_copy = [n for n in self.board]
        board_copy[i] = mark
        winning_moves = 0
        for j in self.get_empty_cells(board_copy):
            if self.test_win_move(mark, i, board_copy):
                winning_moves += 1
        if winning_moves >= 2:
            return i

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
        selected_cell = self.calculate_best_move()
        self.board[selected_cell] = "O"
        print("Computer selected cell {} for O.\n".format(selected_cell))
        self.draw_board()

    def calculate_best_move(self):
        for a, b, c in self.WIN_COMBINATIONS: #CHECK IF THERE IS ANY INSTANT WIN = FIRST MOVE
            if self.board[a] == self.board[b] == "O" and self.board[c] in self.get_empty_cells():
                print("FIRST")
                return c
            elif self.board[a] == self.board[c] == "O" and self.board[b] in self.get_empty_cells():
                print("FIRST")
                return b
            elif self.board[b] == self.board[c] == "O" and self.board[a] in self.get_empty_cells():
                print("FIRST")
                return a

        for a, b, c in self.WIN_COMBINATIONS: #CHECK IF THERE IS ANY INSTANT WIN FOR OPPONENT TO BLOCK = SECOND MOVE
            if self.board[a] == self.board[b] == "X" and self.board[c] in self.get_empty_cells():
                print("SECOND")
                return c
            elif self.board[a] == self.board[c] == "X" and self.board[b] in self.get_empty_cells():
                print("SECOND")
                return b
            elif self.board[b] == self.board[c] == "X" and self.board[a] in self.get_empty_cells():
                print("SECOND")
                return a

        for i in self.get_empty_cells(): #CHECK IF THERE IS ANY FORK FOR AI = THIRD MOVE
            board_copy = [n for n in self.board]
            board_copy[i] = "O"
            winning_moves = 0
            for j in self.get_empty_cells(board_copy):
                if self.test_win_move("O", j, board_copy):
                    print(i, j, "FROM 3")
                    winning_moves += 1
            if winning_moves >= 1: #SWITCHED FROM 2 // MAY BE BETTER WITH 1
                print("THIRD")
                return i #CAN BE IMPROVED // TO IMPLEMENT CONTINUE CHECKING AFTER THE FIRST SOLUTION DECENT WAS FOUND

        player_forks = 0                   #|
        for i in self.get_empty_cells():   #|
            if self.test_fork_move("X", i) is not None:
                player_forks +=1
        if player_forks == 1:
            return i             #|CHECK IF THERE IS ANY FORK FOR OPPONENT = FOURTH MOVE
        elif player_forks == 2:            #|
            for j in [2, 4, 6, 8]:
                if j in self.get_empty_cells():
                    return j

        if len(self.get_empty_cells()) == 9:            #|PLAY IN CORNER IF FIRST, ELSE CENTER IF IT IS EMPTY = FIFTH MOVE
            print("FIFTH - CORNER")
            return 1
        elif self.board[5] in self.get_empty_cells():   #|
            print("FIFTH - CENTER")
            return 5

        for i in [1, 3, 7, 9]: #PLAY IN OPPOSITE CORNER IF OPPONENT PLAYS IN CORNER = SIXTH MOVE
            if i == "X" and i == 1 and 9 in self.get_empty_cells():
                print("SIXTH")
                return 9
            if i == "X" and i == 3 and 7 in self.get_empty_cells():
                print("SIXTH")
                return 7
            if i == "X" and i == 7 and 3 in self.get_empty_cells():
                print("SIXTH")
                return 3
            if i == "X" and i == 9 and 1 in self.get_empty_cells():
                print("SIXTH")
                return 1

        for i in [1, 3, 7, 9]: #PLAY IN EMPTY CORNER = SEVENTH MOVE
            if i in self.get_empty_cells():
                print("SEVENTH")
                return i

        for i in self.get_empty_cells(): #PLAY IN ANY EMPTY CELL = EIGHTH MOVE
            print("EIGHTH")
            return i

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
