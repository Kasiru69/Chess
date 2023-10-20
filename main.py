import asyncio
import pygame as py
import ChessEngine
import Images
width=height=512
dimension=8
size=height
fps=15
images={}
Flag=False
def loadimages():
    pieces=['black_r','black_n','black_b','black_q','black_k','black_p','white_r','white_n','white_b', 'white_q', 'white_k','white_p']
    for _ in pieces:
        images[_]=py.transform.scale(py.image.load("Images/"+_+".png"),(64,64))
async def main():
    py.init()
    screen=py.display.set_mode((512,512))
    clock=py.time.Clock()
    screen.fill(py.Color('red'))
    gs=ChessEngine.gamestate()
    validmoves=gs.ValidMoves()
    movemade=False
    loadimages()
    flag=True
    select=()
    clicks=[]
    while flag:
        for e in py.event.get():
            if e.type == py.QUIT:
                flag=False
            elif e.type == py.MOUSEBUTTONDOWN:
                cood=py.mouse.get_pos()
                col=cood[0]//64
                row=cood[1]//64
                if select==(row,col):
                    select=()
                    clicks=[]
                else:
                    select=(row,col)
                    clicks.append(select)
                if len(clicks) == 2:
                    print(clicks)
                    move=ChessEngine.Move(clicks[0],clicks[1],gs.board)
                    if move in validmoves:
                        gs.makeMove(move)
                        movemade=True
                        select=()
                        clicks=[]
                    else:
                        clicks=[select]
        if movemade:
            validmoves=gs.ValidMoves()
            if gs.checkmate:
                flag=False
                Flag=True
            movemade=False
        drawGameState(screen,gs,validmoves, select)
        clock.tick(15)
        py.display.flip()
    #draw_text(screen, 'win')
def drawGameState(screen,gs,validmoves,select):
    drawBoard(screen)
    drawPieces(screen,gs.board)
    highlight(screen,gs,validmoves,select)
    if Flag==True:
        draw_text(screen, 'win')
def highlight(screen, gs, validmoves, select):
    if select!=():
        r=select[0]
        c=select[1]
        if gs.board[r][c][0]=='w' or gs.board[r][c][0]=='b':
            s=py.Surface((64,64))
            s.set_alpha(100)
            s.fill(py.Color('blue'))
            k = py.Surface((64, 64))
            k.set_alpha(100)
            k.fill(py.Color('red'))
            screen.blit(s,(c*64,r*64))
            s.fill(py.Color('yellow'))
            for move in validmoves:
                if move.startrow == r and move.startcol == c:
                    if gs.board[move.endrow][move.endcol]!='--':
                        screen.blit(k, (move.endcol * 64, move.endrow * 64))
                    else:
                        screen.blit(s, (move.endcol * 64, move.endrow * 64))

def drawBoard(screen):
    colors=[py.Color('white'),py.Color('gray')]
    for r in range(8):
        for c in range(8):
            color=colors[(r+c)%2]
            py.draw.rect(screen,color,py.Rect(c*64,r*64,512,512))
def drawPieces(screen,board):
    for r in range(8):
        for c in range(8):
            piece=board[r][c];
            if piece!='--':
                print(images[piece])
                screen.blit(images[piece],py.Rect(c*64,r*64,512,512))
def draw_text(screen, text):
    font = py.font.SysFont("Helvitca", 32, True, False)
    text_object = font.render(text.format(15), False, py.Color("Black"))
    text_location = py.Rect(0, 0, 512, 512).move(512 / 2 - text_object.get_width() / 2,
                                                      512 / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)

asyncio.run(main())
