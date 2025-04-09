import pygame as pg 
import time 
import random
import psycopg2
from connect import connect
from config import load_config
''''''''''''''''''''''''''''''''''''''''''''''''
pg.init()
FPS = pg.time.Clock()
FPS.tick(60)
cell = 10
GRID_WIDTH = 500 // cell
GRID_HEIGHT = 500 // cell
state = 'RIGHT'
Black = pg.Color(0, 0, 0)         
White = pg.Color(255, 255, 255)  
Grey = pg.Color(128, 128, 128)   
Red = pg.Color(255, 0, 0) 
Green = pg.Color(57,255,20)
Blue = pg.Color(0,0,255)
Biruce = pg.Color(63,161,119)
Brown = pg.Color(139,69,19)
run = True 
screen = pg.display.set_mode((500,500))
snake_body = []
colour = Green

w = True
N = True
M = True
SCORE = 0
speed = 10
scr = 0
LVL = 1
paused = False 
lennn = 2
colorr = Red

print('Please insert Your name')
name = input()
sqlIN = 'INSERT INTO scores(name,score,level,len) values(%s,%s,%s,%s) returning *'
sqlUPDATE = 'UPDATE scores SET score = %s, level = %s, len= %s WHERE name = %s'
sqlCHECK = 'SELECT * FROM scores WHERE name = %s'

conn = connect(load_config())
cur = conn.cursor()

cur.execute(sqlCHECK,(name,))
result = cur.fetchone()
if result:
    ID,name,SCORE,LVL,lennn = result
    scr = SCORE

else:
    cur.execute(sqlIN,(name,0,1,0))
    conn.commit()

for i in range((lennn)):
    snake_body.append([140-10*i,150])
snake_head = snake_body[0]
time.sleep(2)
''''''''''''''''''''''''''''''''''''''''''''''''
def move(snake_head,state,w,speed):
    if w:
        if state == 'RIGHT':
            new_headx = snake_head[0]+speed
            new_heady = snake_head[1]
        elif state == 'LEFT':
            new_headx= snake_head[0]-speed
            new_heady = snake_head[1]
        elif state == 'DOWN':
            new_heady = snake_head[1]+speed
            new_headx = snake_head[0]
        elif state == 'UP':
            new_heady = snake_head[1]-speed
            new_headx = snake_head[0]
        return [new_headx,new_heady]
'''ADDing timer FUnction '''
def timer(a):
    b = max(4-(pg.time.get_ticks() - a.spawn_time)//1000,0)
    t_font = pg.font.SysFont('Times New Roman',20)
    t_sur = t_font.render(f'{b}',True,White)
    t_rect = t_sur.get_rect(topleft = (a.fx+5,a.fy-1))
    screen.blit(t_sur,t_rect.topleft) 

def LVeL():
    scorepad_font = pg.font.SysFont('comic_sans_ms',20)
    scorepad_sur = scorepad_font.render(f"LVL: {LVL}",True,Grey)
    scorepad_rect = scorepad_sur.get_rect(topleft = (0,40))
    screen.blit(scorepad_sur,scorepad_rect.topleft)
    pg.display.update()
def scorepad():
    scorepad_font = pg.font.SysFont('Times New Roman',25)
    scorepad_sur = scorepad_font.render(f"score: {SCORE}",True,Grey)
    scorepad_rect = scorepad_sur.get_rect(topleft = (0,0))
    screen.blit(scorepad_sur,scorepad_rect.topleft)
    pg.display.update()
def game_over(font):
    screen = pg.display.set_mode((600,600))
    screen.fill(White)
    game_over_font = pg.font.SysFont(font,40)
    game_over_surface = game_over_font.render(f"Game Over, your score is: {SCORE}",True,Red)
    game_over_rect = game_over_surface.get_rect(center = (300,300))
    screen.blit(game_over_surface,game_over_rect.topleft)
    pg.display.update()
    time.sleep(3)
class fruit(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.fx = 0
        self.fy = 0
        self.heigth = 10
        self.width = 10 
        self.borders = [1,1]
    def spawn(self,barr):
        spawned = False
        while not spawned:
            self.fx = random.randint(self.borders[0],GRID_WIDTH-self.borders[1])*cell
            self.fy = random.randint(self.borders[0],GRID_HEIGHT-self.borders[1])*cell
            self.spawn_time = pg.time.get_ticks()
            if [self.fx,self.fy] not in snake_body and (self.fx,self.fy) not in barr:
                spawned = True
    def draw(self, screen,colorr):
        pg.draw.rect(screen, colorr, (self.fx, self.fy, self.heigth, self.width)) 
    def big(self):
        self.heigth = 20
        self.width = 20
        self.borders = [5,5]
    def res(self,barr):
        if pg.time.get_ticks() - self.spawn_time > 4000:  
             self.spawn(barr)
''''''''''''''''''''''''''''''''''''''''''''''''    
apple = fruit()
big_apple = fruit()
big_apple.big()

while run:
    if not paused:
        snake_head = snake_body[0]
        head_rect = pg.Rect(snake_body[0][0], snake_body[0][1], cell, cell)
        if LVL == 1:
            screen.fill(Black)
            barr = [(999,99)]
        elif LVL == 2:
            screen.fill(White)
            colour = Red
            colorr = Blue
            pg.draw.rect(screen,Biruce,(20,70,200,10))
            pg.draw.rect(screen,Biruce,(20,70,10,70))
            pg.draw.rect(screen,Biruce,(490,250,10,100))
            pg.draw.rect(screen,Biruce,(250,250,10,70))
            pg.draw.rect(screen,Biruce,(400,20,100,10))
            barr = [(20,70),(20,70),(490,250),(250,250),(400,20)]
            barrcollide = [pg.Rect(20,70,200,10),pg.Rect(20,70,10,70),pg.Rect(490,250,10,100),pg.Rect(250,250,10,70),pg.Rect(400,20,100,10)]
            for i in barrcollide:
                if head_rect.colliderect(i):
                        time.sleep(1)
                        w = False
                        screen.fill(Red)
                        pg.display.update()
                        cur.execute(sqlUPDATE,(0,1,2,name))
                        conn.commit()
                        time.sleep(1)
                        game_over('comic_sans_ms')
                        run = False
                
        elif LVL >= 3:
            screen.fill(Green)
            pg.draw.rect(screen,Brown,(20,70,200,10))
            pg.draw.rect(screen,Brown,(20,70,10,70))
            pg.draw.rect(screen,Brown,(490,250,10,100))
            pg.draw.rect(screen,Brown,(250,250,10,70))
            pg.draw.rect(screen,Brown,(400,20,100,10))

            pg.draw.rect(screen,Brown,(100,100,105,10))
            pg.draw.rect(screen,Brown,(40,200,20,10))
            pg.draw.rect(screen,Brown,(60,200,50,10))
            pg.draw.rect(screen,Brown,(150,50,10,60))
            barr = [(20,70),(20,70),(490,250),(250,250),(400,20),(100,100),(40,200),(60,200),(150,50)]
            barrcollide = [pg.Rect(20,70,200,10),pg.Rect(20,70,10,70),pg.Rect(490,250,10,100),pg.Rect(250,250,10,70),pg.Rect(400,20,100,10),pg.Rect(100,100,105,10),pg.Rect(40,200,20,10),pg.Rect(60,200,50,10),pg.Rect(150,50,10,60)]
            colour = Blue
            colorr = Red
            for i in barrcollide:
                if head_rect.colliderect(i):
                        time.sleep(1)
                        w = False
                        screen.fill(Red)
                        pg.display.update()
                        cur.execute(sqlUPDATE,(0,1,2,name))
                        conn.commit()
                        time.sleep(1)
                        game_over('comic_sans_ms')
                        run = False
        for e in pg.event.get():
            if e.type == pg.QUIT:
                cur.execute(sqlUPDATE,(SCORE,LVL,lennn,name))
                conn.commit()
                run = False
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_DOWN and state != 'UP':
                    state = 'DOWN'
                elif e.key == pg.K_UP and state != 'DOWN':
                    state = 'UP'
                elif e.key == pg.K_LEFT and state != 'RIGHT':
                    state = 'LEFT'
                elif e.key == pg.K_RIGHT and state != 'LEFT':
                    state = 'RIGHT'
                elif e.key == pg.K_SPACE:
                    paused = True
        
        #Moving 

        for block in snake_body:
            pg.draw.rect(screen,colour,(block[0],block[1],10,10))
        s = move(snake_head,state,w,speed)
        
        '''COllision with borders'''
        if snake_head[1] >= 500 or snake_head[1]+10 <= 0 or snake_head[0] >= 500 or snake_head[0]+10 <= 0 or s in snake_body:
            time.sleep(1)
            w = False
            screen.fill(Red)
            pg.display.update()
            cur.execute(sqlUPDATE,(0,1,2,name))
            conn.commit()
            time.sleep(1)
            game_over('comic_sans_ms')
            run = False
        snake_body.insert(0,s)
        '''COLLISION ApPLeS'''
        head_rect = pg.Rect(snake_body[0][0], snake_body[0][1], cell, cell)
        fruit_rect = pg.Rect(apple.fx, apple.fy, cell, cell)
        big_apple_rect = pg.Rect(big_apple.fx, big_apple.fy, 20, 20)
        if head_rect.colliderect(fruit_rect):
            lennn +=1
            N = True
            SCORE+=1
            scr += 1
            if scr>=8:
                LVL+=1
                speed+=0.5
                scr = 0
        else:
            snake_body.pop()
        
        if head_rect.colliderect(big_apple_rect):
            M = True
            SCORE+=3
            scr += 3
            if scr>=8:
                LVL+=1
                speed+=0.5
                scr = 0

        
        if M:
            big_apple.spawn(barr)  
        big_apple.draw(screen,Red)
        timer(big_apple)
        M = False
        big_apple.res(barr)
        if N:
            apple.spawn(barr)
        apple.draw(screen,colorr)
        N = False


        scorepad()
        LVeL()
    else:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                cur.execute(sqlUPDATE,(SCORE,LVL,lennn,name))
                conn.commit()
                run = False
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_SPACE:
                    paused = False
        font = pg.font.SysFont('Arial', 40)
        text = font.render('PAUSED', True, (255, 255, 255))
        screen.blit(text, (180, 230))
        pg.display.flip()
    pg.time.delay(60)
    pg.display.update()