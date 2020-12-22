"""
blah blah blah
I made a user vs computer battleship game!
Shubhradeep Majumdar
"""
__AUTHOR__ = "Shubhradeep Majumdar"

import random


# Function to ask the user for their board position
def generateShips(row, column):
    """
    returns the row number and column number based on the CR input (B5, C2, etc.)
    :param row: row number
    :param column: column index (A, B)
    :return: class `tuple` of row, column
    """

    return int(row) - 1, ord(column.upper()) - 65


def printBoard(board, numcols):
    """
    prints a stylized battleship board
    :param board: the board list to print
    :param numcols: number of columns the board is initialized with
    :return: None
    """
    # Shows the board, one row at a time, labelled
    print("   {0}".format(' '.join([chr(65 + i) for i in range(numcols)])))
    print("  {0}+".format('+-' * numcols))
    rowNumber = 1
    for row in board:
        print("%02d|%s|" % (rowNumber, "|".join(row)))
        print("  {0}+".format('+-' * numcols))
        rowNumber = rowNumber + 1

    return None


def generateComputerChoicePool(numcols):
    """
    generates the choices available to computer at the beginning
    :param numcols: number of columns
    :return: :class: `list` of available choice
    """

    columns = [chr(k) for k in range(65, 65 + numcols)]
    rows = [k + 1 for k in range(numcols)]

    return rows, columns, [(k.upper() + str(l)) for k in columns for l in rows]


def computerChoicesAvailable(choiceList, choiceMade):
    """
    keep reducing the choice list after every choice made
    :param choiceList: List of available choices
    :param choiceMade: the choice made recently
    :return: class `list` of remaining choices
    """

    return list(filter(lambda k: k != choiceMade.upper(), choiceList))


def makeBoard(numcols):
    """
    Put ships in coordinates
    :param numcols: number of columns the game boards are to be initialized with
    :return:
    """

    computerBoard, playerBoard, guessesBoard = \
        [[' ' for i in range(numcols)] for j in range(numcols)],\
        [[' ' for i in range(numcols)] for j in range(numcols)],\
        [[' ' for i in range(numcols)] for j in range(numcols)]

    # computer will generate play board but not reveal
    rows, columns, compChoicePool = generateComputerChoicePool(numcols)
    i = 0
    while i < min(5, numcols):
        compChoice = random.choice(compChoicePool)
        rowNumberComp, columnNumberComp = generateShips(compChoice[1], compChoice[0])
        computerBoard[rowNumberComp][columnNumberComp] = 'X'
        compChoicePool = computerChoicesAvailable(compChoicePool, compChoice)
        i = i + 1

    # set up player board and print
    print("Player, set up your ships . . .")
    printBoard(playerBoard, numcols)
    coordinatesIn = \
        input("Enter {0} board coordinates (comma delimited) to place ships\n".format(str(min(5, numcols))) +
              "columns available: {0}\n".format(', '.join(["'" + k + "'" for k in columns])) +
              "rows available: {0}\n".format(', '.join(str(k) for k in rows)) +
              "e.g. {0}\n".format(', '.join([(k.upper() + str(l)) for k in columns for l in rows][:min(5, numcols)]))
              ). \
        upper(). \
        replace(', ', ',')

    assert coordinatesIn.find(',') != -1, "Coordinates must be comma delimited"

    coordinates = coordinatesIn.split(sep=',')

    assert len(coordinates) == min(5, numcols), "{0} coordinates required".format(str(min(5, numcols)))

    for k in coordinates:
        rowNumber, columnNumber = generateShips(k[1], k[0])
        playerBoard[rowNumber][columnNumber] = 'X'

    print('Player board below')
    printBoard(playerBoard, numcols)
    print("\n")

    return computerBoard, playerBoard, guessesBoard


def runGame(numcols, computerBoard, playerBoard, guessesBoard):
    """
    the actual game logic
    :param numcols: number of columns the game boards are initialized with
    :param computerBoard: the computer's board list
    :param playerBoard: the player's board list
    :param guessesBoard: the guessing board list
    :return:
    """

    # initialize computer decisions
    rowls, columnls, compChoicePool = generateComputerChoicePool(numcols)

    # Initialize guess counts
    computerGuess, playerGuess = 0, 0

    # run game
    while True:
        # player plays
        print("Player, guess a battleship location")
        print("Enter the opponent's board coordinate to launch missile\n" +
              "columns available: {0}\n".format(', '.join(["'"+k+"'" for k in columnls])) +
              "rows available: {0}\n".format(', '.join(str(k) for k in rowls)) +
              "e.g. A1 or B4\n"
              )
        printBoard(guessesBoard, numcols)
        inputCoordinate = input().upper().replace(' ', '')
        rowIn = int(inputCoordinate[1])
        columnIn = inputCoordinate[0]
        rowNumber, columnNumber = generateShips(rowIn, columnIn)

        if computerBoard[rowNumber][columnNumber] == ' ':
            guessesBoard[rowNumber][columnNumber] = '.'
            computerBoard[rowNumber][columnNumber] = '.'
            print('\nPlayer played: You Missed!\n')
        elif computerBoard[rowNumber][columnNumber] == 'X':
            guessesBoard[rowNumber][columnNumber] = 'O'
            computerBoard[rowNumber][columnNumber] = 'O'
            playerGuess = playerGuess + 1
            print("\nPlayer played: That's a HIT! Computer has {0} battleships left.\n".format(numcols - playerGuess))
        elif computerBoard[rowNumber][columnNumber] in ('.', 'O'):
            print("\nPlayer played: You have already launched a missile here.\n")

        if playerGuess == min(5, numcols):
            print("You Win!")
            break

        # Computer Plays
        compChoice = random.choice(compChoicePool)
        rowNumberComp, columnNumberComp = generateShips(compChoice[1], compChoice[0])

        # reset its choice pool
        compChoicePool = computerChoicesAvailable(compChoicePool, compChoice)

        if playerBoard[rowNumberComp][columnNumberComp] == ' ':
            playerBoard[rowNumberComp][columnNumberComp] = '.'
            print('Computer played: It Missed!')
        elif playerBoard[rowNumberComp][columnNumberComp] == 'X':
            playerBoard[rowNumberComp][columnNumberComp] = 'O'
            computerGuess = computerGuess + 1
            print("Computer played: You LOST a battleship! {0} left.".format(numcols - computerGuess))

        print("\nplayer board")
        printBoard(playerBoard, numcols)
        print("\n")

        if computerGuess == min(5, numcols):
            print("You Lose!")
            break

    return computerBoard, playerBoard


if __name__ == '__main__':
    # ask for board dimension
    numcols = int(input('Enter the number of columns for the square board (at least 5 recommended): '))
    print("The game will be played with {0} ships.".format(min(5, numcols)))

    # Initialize boards
    computerBoard, playerBoard, guessesBoard = makeBoard(numcols=numcols)

    # Run game
    computerBoard, playerBoard = \
        runGame(numcols=numcols,
                computerBoard=computerBoard,
                playerBoard=playerBoard,
                guessesBoard=guessesBoard
                )

    print("\nplayer board")
    printBoard(playerBoard, numcols)
    print("\ncomputer board")
    printBoard(computerBoard, numcols)
    print("\n")

