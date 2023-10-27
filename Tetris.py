from cmu_graphics import *
import random

def onAppStart(app):
    #Making the board
    app.rows = 15
    app.cols = 10
    app.boardLeft = 95
    app.boardTop = 50
    app.boardWidth = 210
    app.boardHeight = 280
    app.cellBorderWidth = .5
    app.board = [(['black'] * app.cols) for row in range(app.rows)]
    app.beginning = True
    
    #stepping
    app.nextPieceIndex = random.randrange(7)-1
    app.isPaused = False
    app.gameOver = False
    app.onStepCounter = 0
    app.stepsPerSecond = 1
    
    #Loading Pieces
    loadTetrisPieces(app)
    loadNextPiece(app)
    app.resetGame = False
    
    
    #score
    app.score = 0
    app.highestScore = 0
    app.newHigh = False
    
    
    
#canvas functions
def onStep(app):
    app.onStepCounter += 1
    
    if app.isPaused == False and app.beginning == False:
        takeStep(app)
        
    resetGame(app)
        
def redrawAll(app):
    
    drawBoard(app)
    drawPiece(app)
    drawBoardBorder(app)
    
    middleX = (app.boardLeft+app.boardWidth)/2 + app.boardLeft/2
    middleY = (app.boardTop+app.boardHeight)/2 + app.boardTop/2
    
    if app.beginning:
        drawLabel(f'TETRIX', middleX, 30, font = 'robotica', fill = 'black', size=36) 
        drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight, opacity = 75)
        drawLabel(f'Controls:', middleX, middleY - 110, fill = 'white', bold = True, size=16)
        drawLabel(f'W, up arrow - rotate piece clockwise', middleX, middleY - 85, fill = 'white', align = 'center', size=11)
        drawLabel(f'A, left arrow - move piece left', middleX, middleY - 70, fill = 'white', align = 'center', size=11)
        drawLabel(f'S, down arrow - move piece down', middleX, middleY - 55, fill = 'white', align = 'center', size=11)
        drawLabel(f'D, right arrow - move piece right', middleX, middleY - 40, fill = 'white', align = 'center', size=11)
        drawLabel(f'space - Hard Drop', middleX, middleY - 25, fill = 'white', align = 'center', size=11)
        drawLabel(f"Use number keys to change difficulty", middleX, middleY + 15 , fill = 'white', size=12)
        drawLabel(f"Difficulty Level: {app.stepsPerSecond} ", middleX, middleY + 40 , bold = True, fill = 'white', size=16)
        drawLabel(f"Press 'enter' to begin", middleX, middleY+90 , fill = 'white', bold = True, size=18)


    elif app.isPaused:
        drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight, opacity = 50)
        drawLabel("Game Paused", middleX, 30 , fill = 'white', border = 'black', borderWidth = 1, size= 36)
        drawLabel("press 'P' to continue", middleX, middleY, fill = 'black', border = 'white', borderWidth = 1, size=16)
    
    elif app.gameOver:
        drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight, opacity = 50)
        drawLabel('Game Over', middleX, 30 , fill = 'white', border = 'black', borderWidth = 2, size=36)
        drawLabel("press the 'R' key to play again", middleX, (app.boardTop + app.boardHeight) + 10, fill = 'black', borderWidth = 1, size=12)
        if app.newHigh:
            drawLabel(f'New High Score!', middleX, middleY-20, fill = 'black', border = 'white', size=16)
            drawLabel(f'{app.score}', middleX, middleY+20, fill = 'black', border = 'white', size=36)
        else:
            drawLabel(f'Score: {app.score}', middleX, middleY - 15, fill = 'black', border = 'white', size=16)
            drawLabel(f'High Score: {app.highestScore}', middleX, middleY + 15, fill = 'black', border = 'white', size=16)
    else:
        drawLabel(f'Score: {app.score}',middleX, app.boardTop/2 - 10, size=16)
        drawLabel(f'High Score: {app.highestScore}', middleX - app.boardLeft + app.boardLeft/4, app.boardTop/2 + 10, size=12)

def resetGame(app):
    if app.gameOver and app.resetGame:
        #Making the board
        app.rows = 15
        app.cols = 10
        app.boardLeft = 95
        app.boardTop = 50
        app.boardWidth = 210
        app.boardHeight = 280
        app.cellBorderWidth = .5
        app.board = [(['black'] * app.cols) for row in range(app.rows)]
        
        #stepping
        app.nextPieceIndex = random.randrange(7)-1
        app.isPaused = False
        app.gameOver = False
        app.onStepCounter = 0
                
        #Loading Pieces
        loadTetrisPieces(app)
        loadNextPiece(app)
        app.resetGame = False
        
        
        #score
        app.score = 0

def onKeyPress(app,key):
    if key.isdigit() == True and int(key) != 0:
        app.stepsPerSecond = int(key)
    if app.beginning and key == 'enter':
        app.beginning = False
        hardDropPiece(app)
    
    elif key == 'p':
        app.isPaused = True if app.isPaused == False else app.isPaused == False 
    elif key == 'r':
        if app.isPaused or app.gameOver:
            app.resetGame = True if app.resetGame == False else app.resetGame == False 
 
    elif not app.isPaused:
        if key == 'left' or key == 'a': movePiece(app,0,-1)
        elif key == 'right' or key == 'd': movePiece(app,0,1)
        elif key == 'down' or key == 's': movePiece(app,1,0)
        elif key == 'up' or key == 'w': rotatePieceClockwise(app)
        elif key == 'space': hardDropPiece(app)
#Piece funtions
def isFull(app,row):
    if 'black' in app.board[row]:
        return False
    return True
    
def removeFullRows(app): #fixer upper
    i = 0
    while i < len(app.board):
        if isFull(app,i):
            
            app.board.pop(i)
            app.score += 10
        else:
            i += 1
    while len(app.board) < app.rows:
        app.board.insert(0,(['black'] * app.cols))
        
def placePieceOnBoard(app):
    for i in range(len(app.piece)):
        for j in range(len(app.piece[0])):
            if app.piece[i][j] == True:
                app.board[app.pieceTopRow+i][app.pieceLeftCol+j] = app.pieceColor #

def takeStep(app):
    if not movePiece(app, +1, 0):
        # We could not move the piece, so place it on the board:
        placePieceOnBoard(app)
        removeFullRows(app)
        loadNextPiece(app)
        
    
def loadNextPiece(app):
    if app.gameOver:
        return
    loadPiece(app, app.nextPieceIndex)
    app.nextPieceIndex = random.randrange(len(app.tetrisPieces))
    app.gameOver = not pieceIsLegal(app)
    if app.gameOver == True and app.score > app.highestScore:
        app.highestScore = app.score 
        app.newHigh = True
    else:
        app.newHigh = False
    
        
    
def rotatePieceClockwise(app):
    oldPiece = app.piece
    oldTopRow = app.pieceTopRow
    oldLeftCol = app.pieceLeftCol
    
    centerRow = oldTopRow + len(app.piece)//2
    centerCol = oldLeftCol + len(app.piece[0])//2
    
    app.piece = rotate2dListClockwise(app.piece)
    newRows = len(app.piece)
    
    app.pieceTopRow = centerRow - len(app.piece)//2
    app.pieceLeftCol = centerCol - len(app.piece[0])//2
    
    if pieceIsLegal(app):
        return
    else:
        app.piece = oldPiece
        app.pieceTopRow = oldTopRow
        app.pieceLeftCol = oldLeftCol
    
def rotate2dListClockwise(L):
    oldRows = len(L)
    oldCols = len(L[0])
    newRows = oldCols
    newCols = oldRows
    
    M = [ ['black']*newCols for newRow in range(newRows) ]
    
    for oldRow in range(oldRows):
        for oldCol in range(oldCols):
            newRow,newCol = oldCol,oldRow
            M[newRow][newCol] = L[oldRow][oldCol]
    for newRow in range(newRows):
        M[newRow].reverse()
    
    return M
    
def hardDropPiece(app):
    while movePiece(app, +1, 0):
        pass
    
def movePiece(app,drow,dcol):
    app.pieceTopRow += drow
    app.pieceLeftCol += dcol
    if pieceIsLegal(app):
        return True
    else: 
        app.pieceTopRow -= drow
        app.pieceLeftCol -= dcol
        return False
        
def pieceIsLegal(app):
    for i in range(len(app.piece)):
        for j in range(len(app.piece[0])):
            if app.piece[i][j] == True:
                if app.pieceLeftCol < 0 or app.pieceLeftCol + len(app.piece[0]) > app.cols or app.pieceTopRow < 0 or app.pieceTopRow + len(app.piece) > app.rows: 
                    return False
                elif app.board[app.pieceTopRow+i][app.pieceLeftCol+j] != 'black':
                    return False
    return True
            
                
def drawPiece(app):
    for i in range(len(app.piece)):
        for j in range(len(app.piece[0])):
            if app.piece[i][j] == True:
                drawCell(app, app.pieceTopRow+i, app.pieceLeftCol+j, app.pieceColor)
    
def loadPiece(app, pieceIndex):
    app.piece = app.tetrisPieces[pieceIndex]
    app.pieceColor = app.tetrisPieceColors[pieceIndex] if not app.beginning else 'black'
    app.pieceTopRow = 0
    
    pieceCols = len(app.piece[0])
    app.pieceLeftCol = (app.cols - pieceCols)//2 

def loadTetrisPieces(app):
    # Seven "standard" pieces (tetrominoes)
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],
              [  True,  True,  True ]]
    lPiece = [[ False, False,  True ],
              [  True,  True,  True ]]
    oPiece = [[  True,  True ],
              [  True,  True ]]
    sPiece = [[ False,  True,  True ],
              [  True,  True, False ]]
    tPiece = [[ False,  True, False ],
              [  True,  True,  True ]]
    zPiece = [[  True,  True, False ],
              [ False,  True,  True ]] 
    app.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece,
                         sPiece, tPiece, zPiece ]
    app.tetrisPieceColors = [ 'red', 'yellow', 'magenta', 'pink',
                              'cyan', 'green', 'orange' ]


#Board funtions
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col, app.board[row][col])

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='white',
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

#main functions
def main():
    runApp()

main()
