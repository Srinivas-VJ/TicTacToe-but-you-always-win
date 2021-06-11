# terminal based TicTacToe game in python

def gameDrawn(grid):
    '''
    returns true if game has ended in a draw
    '''
    # print(f'number of symbols on board = {getNumver
    if ((getNumberOfSymbols(grid, 'X') + getNumberOfSymbols(grid, 'O')) == 9):
        return True
    return False


def playerHasWon(grid, player):
    '''
    returns true if player has won.
    '''
    symbs = getNumberOfSymbols(grid, player)

    if(symbs < 3):
        return False

    pos = getPositions(grid, player)

    for t in pos:
        if ((t[0] == t[1]) or (t[0] + t[1] == 2)):
            if(diagonalIsFull(grid, t, player)):
                return True
        if (rowIsFull(grid, t, player) or colIsFull(grid, t, player)):
            return True

    return False


def rowIsFull(grid, t, player):
    return (grid[t[0]][0] == player and grid[t[0]][1] == player and grid[t[0]][2] == player)


def colIsFull(grid, t, player):
    return (grid[0][t[1]] == player and grid[1][t[1]] == player and grid[2][t[1]] == player)


def diagonalIsFull(grid, t, player):
    if(t[0] != t[1]):
        return (player == grid[0][2] and player == grid[1][1] and player == grid[2][0])
    return (player == grid[0][0] and player == grid[1][1] and player == grid[2][2])


def getPositions(grid, player):
    '''
    returns positions which are filled in by a player
    '''
    pos = []
    for i in range(3):
        for j in range(3):
            if (grid[i][j] == player):
                pos.append((i, j))
    return pos


def getNumberOfSymbols(grid, player):
    '''
    returns returns total num of symbols in grid
    '''
    count = 0
    for i in range(3):
        for j in range(3):
            if (grid[i][j] == player):
                count += 1
    return count


def printGrid(grid):
    '''
    Prints the grid on the terminal
    '''

    print(chr(27)+'[2j')
    print('\033c')
    print('\x1bc')
    print('\x1b[0;33;40m')
    print("""╔╦╗┬┌─┐╔╦╗┌─┐┌─┐╔╦╗┌─┐┌─┐
 ║ ││   ║ ├─┤│   ║ │ │├┤
 ╩ ┴└─┘ ╩ ┴ ┴└─┘ ╩ └─┘└─┘""")
    print('\x1b[0m')

    for i in range(3):
        print('\t', end="")
        for j in range(3):
            if(grid[i][j] == 'X'):
                s = '❌'
            elif (grid[i][j] == 'O'):
                s = '⭕️'
            else:
                s = '  '
            if(j != 2):
                print(" " + s + " ", end="╏")
            else:
                print(" " + s + " ", end="")

        print()
        print('\t', end="")
        if(i != 2):
            print("──────────────")
    print()
    print()


def game(grid, x_turn):
    '''
    A function thats runs in a loop until the game ends
    Takes user input and processes it.
    '''

    if (x_turn):
        printGrid(grid)
        player = 'X'
        position = int(input(f'Enter position X [ 1 ⇒ 9 ]➤ '))
        i, j = 0, 0
        if (position > 0):
            if (position <= 3):
                i, j = 0, position - 1
            elif (position <= 6):
                i, j = 1, (position % 3) - 1
            elif (position <= 9):
                i, j = 2, (position % 3) - 1
            else:
                print("invalid")
                game(grid, x_turn)
        else:
            print("invalid")
            game(grid, x_turn)
    else:
        player = 'O'
        i, j = getMove(grid)

    if(grid[i][j] == ' '):
        grid[i][j] = player
    else:
        print("invalid")
        game(grid, x_turn)
    if (playerHasWon(grid, player)):
        printGrid(grid)
        print(f"GAME OVER {player} WINS !")
        print('Do you want to play again ? (y/n)')
        inp = input()
        if (inp == 'y' or inp == 'Y'):
            game([[' ', ' ', ' '],
                  [' ', ' ', ' '],
                  [' ', ' ', ' ']], True)

        return

    if (gameDrawn(grid)):
        printGrid(grid)
        print(f'GAME Tied !')
    game(grid, not x_turn)


def getEmptySpots(grid):
    '''
    returns position of all empty spots
    '''
    res = []
    for i in range(3):
        for j in range(3):
            if(grid[i][j] == ' '):
                res.append((i, j))
    return res


def getMove(grid):
    '''
    returns a move to the bot
    '''
    bestScore = -100
    pos = 0, 0
    positions = getEmptySpots(grid)
    for (i, j) in positions:
        grid[i][j] = 'O'
        score = minimax(grid, False)
        grid[i][j] = ' '
        # print(score)
        if score > bestScore:
            bestScore = score
            pos = i, j
            # print(f'best score {bestScore} move {pos}')
    return pos


def minimax(grid, isMaximizer):
    '''
    minimax algorithm
    '''

    if(playerHasWon(grid, 'X')):
        return 1

    if(playerHasWon(grid, 'O')):
        return -1

    if(gameDrawn(grid)):
        return 0

    if (isMaximizer):
        bestScore = -100
        positions = getEmptySpots(grid)
        for (i, j) in positions:
            grid[i][j] = 'O'
            score = minimax(grid, False)
            grid[i][j] = ' '
            bestScore = max(bestScore, score)
        return bestScore

    else:
        bestScore = 100
        positions = getEmptySpots(grid)
        for (i, j) in positions:
            grid[i][j] = 'X'
            score = minimax(grid, True)
            grid[i][j] = ' '
            bestScore = min(bestScore, score)
        return bestScore


if __name__ == '__main__':

    game([[' ', ' ', ' '],
          [' ', ' ', ' '],
          [' ', ' ', ' ']], True)
