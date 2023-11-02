import copy
import sys
import pygame
import numpy as np 
import random
from const import *
from button import Button

#pygame setup
pygame.init()
screen =pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(bg_color)
pygame.display.set_caption("Menu")

class Board:
    def __init__(self):
        self.square = np.zeros((ROWS,COLS))
        self.emp_sq = self.square
        self.marked_sqr = 0
        #self.mark_sqr(1,1,2)
        #print(self.square)
    def mark_sqr(self,row,col,player):
        self.square[row][col]=player
        self.marked_sqr += 1
        
    def final_state(self,show=False):
        #return 0 is there is no win
        #return 1 if player 1 win 
        # return 2 if player 2 win
        #vartical win
        for col in range(COLS):
            if self.square[0][col] == self.square[1][col] == self.square[2][col] != 0:
                if show:
                    color = wins_color if self.square[0][col] == 2 else cros_color
                    iPos = (col * s_size + s_size // 2, 20)
                    fPos = (col * s_size + s_size // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, line_width)
                return self.square[0][col]

        # horizontal win
        for row in range(ROWS):
            if self.square[row][0] == self.square[row][1] == self.square[row][2] != 0:
                if show:
                    color = wins_color if self.square[row][0] == 2 else cros_color
                    iPos = (20, row * s_size + s_size // 2)
                    fPos = (WIDTH - 20, row * s_size + s_size // 2)
                    pygame.draw.line(screen, color, iPos, fPos, line_width)
                return self.square[row][0]

        # desc diagonal
        if self.square[0][0] == self.square[1][1] == self.square[2][2] != 0:
            if show:
                color = wins_color if self.square[1][1] == 2 else cros_color
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, cross_width)
            return self.square[1][1]

        # asc diagonal
        if self.square[2][0] == self.square[1][1] == self.square[0][2] != 0:
            if show:
                color = wins_color if self.square[1][1] == 2 else cros_color
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, cross_width)
            return self.square[1][1]

        # no win yet
        return 0
    

    def empty_sqr(self,row,col):
        return self.square[row][col] == 0
    
    def get_empty_sqr(self):
        emp_sq=[]
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row,col):
                    emp_sq.append((row,col))
        return emp_sq
    
    def isfull(self):
        return self.mark_sqr == 9
    
    def isempty(self):
        return self.mark_sqr == 0

class AI:
    def __init__(self,level=1,player=2):
        self.level = level
        self.player = player
    def rnd(self,board):
        emp_sq=board.get_empty_sqr()
        idx = random.randrange(0,len(emp_sq))
        return emp_sq[idx]
    def minimax(self, board, maximizing):
        
        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None # eval, move

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            emp_sq = board.get_empty_sqr()

            for (row, col) in emp_sq:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            emp_sq = board.get_empty_sqr()

            for (row, col) in emp_sq:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            return min_eval, best_move

    # --- MAIN EVAL ---

    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board, False)
            
            if move is not None:
                print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')
            return move # row, col

class Game:
    def __init__(self):
        self.board = Board()
        self.player = 1 # 1 == cross and 2 is circle
        self.ai=AI()
        self.gamode = 'ai' #player vs player
        self.running,self.playing = True,False
        self.show_line()
    def make_move(self,row,col):
        self.board.mark_sqr(row,col,self.player)
        self.draw_fig(row,col)
        self.next_turn()
    def show_line(self):
        screen.fill( bg_color )
        #vertical
        pygame.draw.line(screen,line_color,(s_size,0),(s_size,HEIGHT),line_width)
        pygame.draw.line(screen,line_color,(WIDTH-s_size,0),(WIDTH-s_size,HEIGHT),line_width)
        #horizontal
        pygame.draw.line(screen,line_color,(0,s_size),(WIDTH,s_size),line_width)
        pygame.draw.line(screen,line_color,(0,HEIGHT-s_size),(WIDTH,HEIGHT-s_size),line_width)
    def draw_fig(self,row,col):
        if self.player == 1:
            #draw cross
            start_des=(col*s_size + OFFSET, row*s_size + OFFSET)
            end_des=(col*s_size + s_size - OFFSET, row*s_size+s_size-OFFSET)
            pygame.draw.line(screen,cross_color,start_des,end_des,cross_width)
            #assanding line 
            start_asc=(col*s_size + OFFSET, row*s_size +s_size - OFFSET)
            end_asc=(col*s_size + s_size - OFFSET, row*s_size+OFFSET)
            pygame.draw.line(screen,cross_color,start_asc,end_asc,cross_width)
        elif self.player == 2:
            center = [col * s_size + s_size//2, row * s_size + s_size//2]
            pygame.draw.circle(screen,circle_color,center,RADIUS,circle_width)

    def next_turn(self):
        self.player = self.player%2 + 1
    def change_gamemode(self):
        self.gamode == 'ai' if self.gamode == 'pvp' else 'p'
    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()
    def reset(self):
        self.__init__()
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("D:/code for fun/tik tak tao/font.ttf", size)

def game_loop(self):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:

                # g-gamemode
                if event.key == pygame.K_g:
                    self.change_gamemode()

                # r-restart
                if event.key == pygame.K_r:
                    self.reset()
                    board = self.board
                    ai = self.ai

                # 0-random ai
                if event.key == pygame.K_0:
                    ai.level = 0
                
                # 1-random ai
                if event.key == pygame.K_1:
                    ai.level = 1

def play():
    #object 
    game=Game()
    board= game.board
    ai = game.ai
    
    #main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:

                # g-gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # r-restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                # 0-random ai
                if event.key == pygame.K_0:
                    ai.level = 0
                
                # 1-random ai
                if event.key == pygame.K_1:
                    ai.level = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1]//s_size
                col = pos[0]//s_size
                #print(row,col)
                #print(event.pos)
                if board.empty_sqr(row, col):
                    game.make_move(row,col)
                    
                #check the board 
                #game.board.mark_sqr(row,col,1)
                #print(game.board.square)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    game.change_gamemode()
                #0-random ai
                if event.key == pygame.K_0:
                    ai.level=0
                if event.key == pygame.K_1:
                    ai.level=1
        if game.gamode == 'ai' and game.player == ai.player:
            pygame.display.update()
            
            #ai methods
            row,col = ai.eval(board)
            game.make_move(row,col)
            if game.isover():
                game.running = False

        pygame.display.update()

def details():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(45).render("OPTIONS\n screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(250, 260))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(200, 460), 
                            text_input="BACK", font=get_font(50), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

BG = pygame.image.load("D:/code for fun/tik tak tao/Background.png")
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("D:/code for fun/tik tak tao/font.ttf", size)

def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(90).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(50, 150))

        PLAY_BUTTON = Button(image=pygame.image.load("D:/code for fun/tik tak tao/Options Rect.png"), pos=(300, 250), 
                            text_input="PLAY", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("D:/code for fun/tik tak tao/Options Rect.png"), pos=(300, 400), 
                            text_input="OPTIONS", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("D:/code for fun/tik tak tao/Options Rect.png"), pos=(300, 550), 
                            text_input="QUIT", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                    #game_loop()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    details()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()