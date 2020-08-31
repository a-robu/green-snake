import os.path
import pygame, sys
from random import randint
from files.levels import *
from pygame.transform import rotate
from pygame.image import load
from pygame.locals import FULLSCREEN
pygame.init()

class Board:
    def __init__(self):
        self.SIZE = (20, 15)
        self.P = []
        self.FREE = ' '
        self.SNAKE = '%'
        self.HEAD = '@'
        self.TAIL = '~'
        self.FOOD = '+'
        self.WALL = '#'
        self.SPAWN = '$'
        self.KILLER = ('%','@','#')
        self.sSize = 30
        self.snakeAnimationFrames = 10
        self.backRandomFrames = 5      

    def LoadImages(self):
        self.backs = []
        self.walls = []
        self.heads = []
        for i in range(self.snakeAnimationFrames):
            frame = load(os.path.join('files', 'head%d.png' % (i))).convert_alpha()
            self.heads.append(frame)
        for i in range(self.backRandomFrames):
            back  = load(os.path.join('files', 'back%d.png' % (i))).convert_alpha()
            self.backs.append(back)
        for i in range(14):
            wall  = load(os.path.join('files', 'wall%d.png' % (i))).convert_alpha()
            self.walls.append(wall)
        self.bodycn     = load(os.path.join('files', 'bodycn.png')).convert_alpha()
        self.bodyst     = load(os.path.join('files', 'bodyst.png')).convert_alpha()
        self.foodSprite = load(os.path.join('files', 'food.png')).convert_alpha()
        self.tailSprite = load(os.path.join('files', 'tail.png')).convert_alpha()
        self.foodSprite = load(os.path.join('files', 'food.png')).convert_alpha()
        G.background    = load(os.path.join('files', 'background.png')).convert_alpha()
        G.frontend      = load(os.path.join('files', 'frontend.jpg'))
        G.newline       = load(os.path.join('files', 'newline.png')).convert_alpha()
        G.setline       = load(os.path.join('files', 'setline.png')).convert_alpha()
        G.quitline      = load(os.path.join('files', 'quitline.png')).convert_alpha()
        G.select        = load(os.path.join('files', 'selectlevel.png')).convert_alpha()

    def RenderBackground(self):
        self.backSurf = pygame.Surface((len(self.P)*self.sSize,len(self.P[0])*self.sSize))
        for x in range(len(self.P)):
            for y in range(len(self.P[0])):
               self.backSurf.blit(self.backs[randint(0,self.backRandomFrames-1)], (x*self.sSize,y*self.sSize))

    def RenderWalls(self):
        self.wallSurf = pygame.Surface((((len(self.P)-1)*self.sSize+self.sSize, (len(self.P[0])-1)*self.sSize+self.sSize)), 65536).convert_alpha()
        for x in range(len(self.P)):
            for y in range(len(self.P[0])):
                cur = [x*self.sSize,y*self.sSize]
                if self.P[x][y] == self.WALL:                    
                    tl = False
                    top = False
                    tr = False
                    right = False
                    br = False
                    bottom = False
                    bl = False
                    left = False                    
                    if y == 0:
                        tl = True
                        top = True
                        tr = True
                    if x == len(Pos.P)-1:
                        tr = True
                        right = True
                        br = True
                    if y == len(Pos.P[0])-1:
                        br = True
                        bottom = True
                        bl = True
                    if x == 0:
                        bl = True
                        left = True
                        tl = True
                    if not top:
                        if self.P[x][y-1] == self.WALL:
                            top = True                    
                    if not tr:
                        if self.P[x+1][y-1] == self.WALL:
                            tr = True
                    if not right:
                        if self.P[x+1][y] == self.WALL:
                            right = True
                    if not br:
                        if self.P[x+1][y+1] == self.WALL:
                            br = True
                    if not bottom:
                        if self.P[x][y+1] == self.WALL:
                            bottom = True
                    if not bl:
                        if self.P[x-1][y+1] == self.WALL:
                            bl = True
                    if not left:
                        if self.P[x-1][y] == self.WALL:
                            left = True
                    if not tl:
                        if self.P[x-1][y-1] == self.WALL:
                            tl = True
                    # No neibourghs.
                    if not top and not right and not bottom and not left:
                        self.wallSurf.blit(self.walls[0], cur)
                    # 1 neibourghs.
                    elif top and not right and not bottom and not left:
                        self.wallSurf.blit(self.walls[1], cur) #top
                    elif not top and right and not bottom and not left :
                        self.wallSurf.blit(rotate(self.walls[1], 270), cur) #right
                    elif not top and not right and bottom and not left :
                        self.wallSurf.blit(rotate(self.walls[1], 180), cur) #bottom
                    elif not top and not right and not bottom and left:
                        self.wallSurf.blit(rotate(self.walls[1], 90), cur) #left
                    # 2 neibourghs.
                    elif top and not tr and right and not left and not bottom:
                        self.wallSurf.blit(self.walls[2], cur) #top right
                    elif top and left and not tl and not right and not bottom:
                        self.wallSurf.blit(rotate(self.walls[2], 90), cur) #top left
                    elif bottom and not bl and left and not right and not top:
                        self.wallSurf.blit(rotate(self.walls[2], 180), cur) #left bottom
                    elif right and not br and bottom and not left and not top:
                        self.wallSurf.blit(rotate(self.walls[2], 270), cur) #right bottom
                    elif not top and right and not bottom and left:
                        self.wallSurf.blit(rotate(self.walls[3], 90), cur) #left right
                    elif top and not right and bottom and not left:
                        self.wallSurf.blit(self.walls[3], cur) #top bottom
                    # 3 neibourghs.
                    elif left and top and right and not bottom and not tl and not tr:
                        self.wallSurf.blit(rotate(self.walls[5], 90), cur) #left top right
                    elif top and tr and right and not bottom and not left:
                        self.wallSurf.blit(self.walls[4], cur) #top tr right
                    elif top and not tr and right and not br and bottom and not left:
                        self.wallSurf.blit(self.walls[5], cur) #top right bottom
                    elif not top and right and br and bottom and not left:
                        self.wallSurf.blit(rotate(self.walls[4], 270), cur) #right br bottom
                    elif not top and right and not br and bottom and not bl and left :
                        self.wallSurf.blit(rotate(self.walls[5], 270), cur) #right bottom left
                    elif not top and not right and bottom and bl and left:
                        self.wallSurf.blit(rotate(self.walls[4], 180), cur) #left bl bottom
                    elif top and not right and bottom and not bl and left and not tl:
                        self.wallSurf.blit(rotate(self.walls[5], 180), cur) #top left bottom
                    elif top and not right and not bottom and left and tl:
                        self.wallSurf.blit(rotate(self.walls[4], 90), cur) #left tl top
                    # 4 walls
                    elif top and not tr and right and not br and bottom and not bl and left and not tl:
                        self.wallSurf.blit(self.walls[8], cur)
                    elif not left and top and not tr and br and right and bottom:
                        self.wallSurf.blit(flip(self.walls[6], False, True), cur)
                    elif not left and top and tr and not br and right and bottom:
                        self.wallSurf.blit(self.walls[6], cur)
                    elif left and not top and not bl and br and right and bottom:
                        self.wallSurf.blit(rotate(self.walls[6], 270), cur)
                    elif left and not top and bl and not br and right and bottom:
                        self.wallSurf.blit(rotate(flip(self.walls[6], False, True), 270), cur)
                    elif top and not right and bottom and left and not tl and bl:
                        self.wallSurf.blit(rotate(self.walls[6], 180), cur)
                    elif top and not right and bottom and left and tl and not bl:
                        self.wallSurf.blit(flip(self.walls[6], True, False), cur)
                    elif top and not tr and right and not bottom and left and tl:
                        self.wallSurf.blit(rotate(self.walls[6], 90), cur)
                    elif top and tr and right and not bottom and left and not tl:
                        self.wallSurf.blit(rotate(flip(self.walls[6], False, True), 90), cur)
                    # 5 walls            cross plus a corner        
                    elif top and right and tr and not bottom and tl and left:
                        self.wallSurf.blit(rotate(self.walls[7], 90), cur) #besides bottoms
                    elif top and tr and right and br and bottom and not left:
                        self.wallSurf.blit(self.walls[7], cur) #besides lefts
                    elif not top and right and br and bottom and bl and left:
                        self.wallSurf.blit(rotate(self.walls[7], 270), cur) #besides tops
                    elif bottom and bl and left and tl and top and not right:
                        self.wallSurf.blit(rotate(self.walls[7], 180), cur) #besides rights
                    elif top and tr and right and not br and bottom and not bl and left and not tl:
                        self.wallSurf.blit(self.walls[12], cur)
                    elif top and not tr and right and not br and bottom and not bl and left and tl:
                        self.wallSurf.blit(rotate(self.walls[12], 90), cur)
                    elif top and not tr and right and not br and bottom and bl and left and not tl:
                        self.wallSurf.blit(rotate(self.walls[12], 180), cur)
                    elif top and not tr and right and bottom and not bl and left and not tl:
                        self.wallSurf.blit(rotate(self.walls[12], 270), cur)
                    # 6 walls
                    elif top and not tr and right and br and bottom and bl and left and not tl:
                        self.wallSurf.blit(rotate(self.walls[10], 180), cur) # top corners
                    elif top and not tr and right and not br and bottom and bl and left and tl:
                        self.wallSurf.blit(rotate(self.walls[10], 90), cur) # right corners
                    elif top and tr and right and not br and bottom and not bl and left and tl:
                        self.wallSurf.blit(self.walls[10], cur) # bottom corners
                    elif top and tr and right and br and bottom and not bl and left and not tl:
                        self.wallSurf.blit(rotate(self.walls[10], 270), cur) # left corners
                    elif top and tr and right and not br and bottom and bl and left and not tl:
                        self.wallSurf.blit(self.walls[11], cur)
                    elif top and not tr and right and br and bottom and not bl and left and tl:
                        self.wallSurf.blit(rotate(self.walls[11], 90), cur)               
                    # 7 walls                    
                    elif top and not tr and right and br and bottom and bl and left and tl:
                        self.wallSurf.blit(rotate(self.walls[9], 90), cur)
                    elif top and tr and right and not br and bottom and bl and left and tl:
                        self.wallSurf.blit(self.walls[9], cur)
                    elif top and tr and right and br and bottom and not bl and left and tl:
                        self.wallSurf.blit(rotate(self.walls[9], 270), cur)
                    elif top and tr and right and br and  bottom and bl and left and not tl:
                        self.wallSurf.blit(rotate(self.walls[9], 180), cur)
                    # 8 walls
                    elif top and tr and right and br and bottom and bl and left and tl:
                        self.wallSurf.blit(self.walls[13], cur)
        
    def RenderBoard(self):
        pees = [int(Cam.cen[0]-G.frameSize[0])/self.sSize+10, int(Cam.cen[1]-G.frameSize[1])/self.sSize+10, #left, top, right, down
              int(Cam.cen[0]+G.frameSize[0])/self.sSize, int(Cam.cen[1]+G.frameSize[1])/self.sSize]
        if pees[0] < 0: pees[0] = 0
        if pees[1] < 0: pees[1] = 0
        if pees[2] > len(self.P)-1: pees[2] = len(self.P)-1
        if pees[3] > len(self.P[0])-1: pees[3] = len(self.P[0])-1
        for x in range(pees[0],pees[2]+1):
            for y in range(pees[1],pees[3]+1):
                cur = [x*self.sSize-Cam.cen[0],y*self.sSize-Cam.cen[1]]
                if   self.P[x][y] == self.FREE: pass
                elif self.P[x][y] == self.SNAKE:
                    index = Snake.body.index([x,y])
                    up   = True if (Snake.body[index+1] == [x,y-1] or Snake.body[index-1] == [x,y-1]) else False
                    down = True if (Snake.body[index+1] == [x,y+1] or Snake.body[index-1] == [x,y+1]) else False
                    left = True if (Snake.body[index+1] == [x-1,y] or Snake.body[index-1] == [x-1,y]) else False
                    right= True if (Snake.body[index+1] == [x+1,y] or Snake.body[index-1] == [x+1,y]) else False
                    if   down and right:G.window.blit(self.bodycn, cur)
                    elif up   and down: G.window.blit(self.bodyst, cur)
                    elif up   and right:G.window.blit(rotate(self.bodycn, 90),  cur)
                    elif down and left: G.window.blit(rotate(self.bodycn, 270), cur)
                    elif up   and left: G.window.blit(rotate(self.bodycn, 180), cur)
                    elif left and right:G.window.blit(rotate(self.bodyst, 90),  cur)
                elif self.P[x][y] == self.WALL: pass
                elif self.P[x][y] == self.HEAD:
                    frame = int(float(Snake.ST)/Snake.MST*self.snakeAnimationFrames)
                    if frame > self.snakeAnimationFrames-1: frame = self.snakeAnimationFrames-1
                    if len(Snake.body) > 1:
                        if   Snake.body[-2] == [x-1,y]: G.window.blit(self.heads[frame], cur)
                        elif Snake.body[-2] == [x,y-1]: G.window.blit(rotate(self.heads[frame], 270), cur)
                        elif Snake.body[-2] == [x+1,y]: G.window.blit(rotate(self.heads[frame], 180), cur)
                        elif Snake.body[-2] == [x,y+1]: G.window.blit(rotate(self.heads[frame], 90), cur)
                    else:
                        if   Snake.heading == 275:     G.window.blit(self.heads[frame], cur)
                        elif Snake.heading == 274:     G.window.blit(rotate(self.heads[frame], 270), cur)
                        elif Snake.heading == 276:     G.window.blit(rotate(self.heads[frame], 180), cur)
                        elif Snake.heading == 273:     G.window.blit(rotate(self.heads[frame], 90), cur)

                elif self.P[x][y] == self.TAIL:
                    if   Snake.body[1] == [x+1,y]: G.window.blit(self.tailSprite, cur)
                    elif Snake.body[1] == [x,y+1]: G.window.blit(rotate(self.tailSprite, 270), cur)
                    elif Snake.body[1] == [x-1,y]: G.window.blit(rotate(self.tailSprite, 180), cur)
                    elif Snake.body[1] == [x,y-1]: G.window.blit(rotate(self.tailSprite, 90), cur)
                elif self.P[x][y] == self.FOOD:    G.window.blit(self.foodSprite, cur)

    def GenerateBoard(self, make_wall_on_the_sides=True):
        self.P = []        
        for i in range(self.SIZE[0]):
            self.P.append([])
            for o in range(self.SIZE[1]):
                self.P[i].append(self.FREE)
        if make_wall_on_the_sides:
            for i in range(1,self.SIZE[0]-1):
                self.P[i][0]=self.WALL
            for i in range(1,self.SIZE[1]-1):
                self.P[self.SIZE[0]-1][i]=self.WALL
            for i in range(1,self.SIZE[0]-1):
                self.P[i][self.SIZE[1]-1]=self.WALL
            for i in range(1,self.SIZE[1]-1):
                self.P[0][i]=self.WALL
            self.P[0][0] = self.WALL
            self.P[len(self.P)-1][0] = self.WALL
            self.P[len(self.P)-1][len(self.P[0])-1] = self.WALL
            self.P[0][len(self.P[0])-1] = self.WALL
        Snake.spawnPoint = [self.SIZE[0]//2 , self.SIZE[1]//2]
        Snake.next = [self.SIZE[0]//2+1, self.SIZE[1]//2]

    def RandFree(self):
        rands = []
        while True:
            for i in range(self.SIZE[0]):
                for o in range(self.SIZE[1]):
                    if self.Check((i,o)):
                        rands.append((i,o))
            return rands[randint(0,len(rands)-1)]

    def GenFood(self):
        rand = self.RandFree()
        Pos.P[rand[0]][rand[1]]=self.FOOD

    def Check(self, next, what=' '):
        if what == self.KILLER:
            if self.P[next[0]][next[1]] in self.KILLER:
                return True
        if what == self.P[next[0]][next[1]]:
            return True


class Snakes:
    def __init__(self):
        self.body = []
        self.fat = 4
        self.heading = 275
        self.next = [0, 0]
        self.nextDir = None
        self.MST=9
        self.ST=0

    def Death(self):
        Pos.__init__()
        Pos.GenerateBoard()
        Snake.__init__()
        if self.lives > 0:
            self.lives -= 1
            self.Spawn()
            Pos.GenFood()
            self.fat -= 1
            G.score = 0
            Cam.SnapTo([self.spawnPoint[0]*Pos.sSize,self.spawnPoint[1]*Pos.sSize])
        else:
            self.lives -= 1
            self.Spawn()
            self.fat -= 1
            G.score = 0
            G.gameOn = False

    def Spawn(self):
        self.body.append(self.spawnPoint[:])
        Pos.P[self.spawnPoint[0]][self.spawnPoint[1]] = Pos.HEAD

    def Move(self):
        boo = bool(not self.heading == 275 and not self.heading == 276)
        cho = False
        for i in range(1,len(G.keys)+1):
            if   G.keys[-i] == 273 and not boo: self.next = [self.body[-1][0], self.body[-1][1] - 1];self.heading = G.keys[-i];cho = True;break
            elif G.keys[-i] == 274 and not boo: self.next = [self.body[-1][0], self.body[-1][1] + 1];self.heading = G.keys[-i];cho = True;break
            elif G.keys[-i] == 276 and     boo: self.next = [self.body[-1][0] - 1, self.body[-1][1]];self.heading = G.keys[-i];cho = True;break
            elif G.keys[-i] == 275 and     boo: self.next = [self.body[-1][0] + 1, self.body[-1][1]];self.heading = G.keys[-i];cho = True;break
        else:
            for i in range(1,len(G.flashKeys)+1):
                if   G.flashKeys[-i] == 273 and not boo: self.next = [self.body[-1][0], self.body[-1][1] - 1];self.heading = G.flashKeys[-i];cho = True;break
                elif G.flashKeys[-i] == 274 and not boo: self.next = [self.body[-1][0], self.body[-1][1] + 1];self.heading = G.flashKeys[-i];cho = True;break
                elif G.flashKeys[-i] == 276 and     boo: self.next = [self.body[-1][0] - 1, self.body[-1][1]];self.heading = G.flashKeys[-i];cho = True;break
                elif G.flashKeys[-i] == 275 and     boo: self.next = [self.body[-1][0] + 1, self.body[-1][1]];self.heading = G.flashKeys[-i];cho = True;break
        if not cho:
            if self.heading == 273: self.next = [self.body[-1][0], self.body[-1][1] - 1]
            elif self.heading == 274: self.next = [self.body[-1][0], self.body[-1][1] + 1]
            elif self.heading == 276: self.next = [self.body[-1][0] - 1, self.body[-1][1]]   
            elif self.heading == 275: self.next = [self.body[-1][0] + 1, self.body[-1][1]]
        G.flashKeys = []
        if Pos.Check(self.next) or Pos.Check(self.next, '~'):
            if self.fat == 0:
                Pos.P[self.body[0][0]][self.body[0][1]] = Pos.FREE
                del self.body[0]
                Pos.P[self.body[0][0]][self.body[0][1]] = Pos.TAIL
            elif self.fat > 0:
                self.fat -= 1
            self.body.append(self.next[:])
            Pos.P[self.next[0]][self.next[1]] = Pos.HEAD
            Pos.P[self.body[-2][0]][self.body[-2][1]] = Pos.SNAKE
        elif Pos.Check(self.next, Pos.KILLER):
            self.Death()
        elif Pos.Check(self.next, Pos.FOOD):
            G.score += 1
            self.fat += 1
            self.body.append(self.next[:])
            Pos.P[self.next[0]][self.next[1]] = Pos.HEAD
            Pos.P[self.body[-2][0]][self.body[-2][1]] = Pos.SNAKE
            Pos.GenFood()
        Cam.target = [self.body[-1][0]*Pos.sSize+Pos.sSize/2-G.framePos[0]-G.frameSize[0]/2,
                       self.body[-1][1]*Pos.sSize+Pos.sSize/2-G.framePos[1]-G.frameSize[1]/2]  if len(self.body) != 0 else self.spawnPoint[:]


class Camera:
    def __init__(self):
        self.cen = [(Pos.SIZE[0]//2+1)*Pos.sSize, Pos.SIZE[1]//2*Pos.sSize]
        self.vel = [0.0,0.0]
        self.target = [(Pos.SIZE[0]//2+1)*Pos.sSize, Pos.SIZE[1]//2*Pos.sSize]
        self.k = 0.1
        self.friction = 2
        self.bound = True

    def Move(self):
        self.vel[0]+=(self.target[0]-self.cen[0])*self.k
        self.vel[1]+=(self.target[1]-self.cen[1])*self.k
        if    self.vel[0] > self.friction: self.vel[0]-= self.friction
        elif  self.vel[0] < self.friction: self.vel[0]+= self.friction
        else: self.vel[0] = 0
        if    self.vel[1] > self.friction: self.vel[1]-= self.friction
        elif  self.vel[1] < self.friction: self.vel[1]+= self.friction
        else: self.vel[1]=0
        self.cen[0]+=self.vel[0]
        self.cen[1]+=self.vel[1]

    def SnapTo(self, originalPoint):
        point = originalPoint[:]
        self.cen = point
        self.target = point
        self.vel = [0,0]


class Game:
    def __init__(self):
        self.GREY = (50,50,50)
        self.RED = (200,10,10)
        self.GREEN = (10,200,10)
        self.BLUE = (10,10,200)
        self.lastKey = None
        self.score = 0
        self.keys = []
        self.FPS = 30
        self.rez = (800,600)
        self.flashKey = None
        self.quit = False
        self.framePos = (20,50)
        self.frameSize = (760,580)
        self.lined = None
        self.selectGame = False
        Snake.lives = 2
        self.flashKeys = []
        self.newsel = False
        self.camsel = False
        self.quitsel = False
        self.polys = {'newpoly':[(223, 123), (270, 211), (306, 173), (324, 69), (370, 92), (477, 26), (519, 75), (257, 354), (204, 295), (203, 190)],
                      'setpoly':[(357, 383), (394, 316), (405, 251), (485, 250), (540, 286), (592, 261), (640, 339), (542, 401), (491, 368), (384, 390)],
                      'quitpoly':[(311, 436), (400, 399), (446, 421), (441, 476), (384, 500), (367, 572), (316, 515)],
                      'newsel':[(248, 324), (167, 314), (129, 272), (146, 209), (214, 175), (314, 188), (351, 221), (355, 284), (316, 317)],
                      'camsel':[(463, 297), (454, 265), (484, 207), (564, 184), (652, 215), (698, 272), (619, 319), (533, 318)],
                      'quitsel':[(417, 464), (330, 426), (409, 393), (478, 424)]}
 
    def Keys(self):
        events = pygame.event.get()
        for event in events:
            if event.type == 12:
                pygame.quit()
                sys.exit()            
            if event.type == 2:
                if 273 <= int(event.key) <= 276 :
                    self.keys.append(int(event.key))
            if event.type == 3:
                if 273 <= int(event.key) <= 276 :
                    if int(event.key) in self.keys: del self.keys[self.keys.index(int(event.key))]
        if self.keys:self.flashKeys.append(self.keys[-1])

    def PlayClassic(self):
        pygame.display.set_caption('Snake! - Playing')
        self.gameOn = True
        Snake.fat -= 1
        Pos.GenerateBoard()
        Snake.Spawn()
        Pos.GenFood()
        Cam.SnapTo([Snake.spawnPoint[0]*Pos.sSize, Snake.spawnPoint[1]*Pos.sSize])
        Pos.RenderBackground()
        Pos.RenderWalls()
        Snake.lives = 2
        while self.gameOn:
            Clock.tick(self.FPS)
            G.Keys()
            if Snake.ST >= Snake.MST: Snake.Move();Snake.ST=0
            else: Snake.ST += 1
            Cam.Move()
            self.Renders()

    def PlayCampaign(self):
        pygame.display.set_caption('Snake! - Campaign')
        self.gameOn = True
        Snake.fat -= 1
        Pos.P = level[0]
        Snake.spawnPoint = spawn[0]
        Snake.Spawn()
        Pos.GenFood()
        Cam.SnapTo([Snake.spawnPoint[0]*Pos.sSize, Snake.spawnPoint[1]*Pos.sSize])
        Pos.RenderBackground()
        Pos.RenderWalls()        
        Snake.lives = 2
        while self.gameOn:
            Clock.tick(self.FPS)
            G.Keys()
            if Snake.ST >= Snake.MST: Snake.Move();Snake.ST=0
            else: Snake.ST += 1
            Cam.Move()
            self.Renders()

    def Renders(self):
        self.window.fill(self.GREY)
        self.window.blit(G.background, (0,0))
        self.window.blit(Pos.backSurf, (-Cam.cen[0],-Cam.cen[1]))
        self.window.blit(Pos.wallSurf, (-Cam.cen[0],-Cam.cen[1]))
        Pos.RenderBoard()
        self.scoreText = self.arial20.render('Score = '+ str(self.score)+' Lives = '+str(Snake.lives),True,(50,50,200))
        self.window.blit(self.scoreText, (self.rez[0]-self.scoreText.get_rect()[2]-10 , 10))
        pygame.display.update()

    def Pip(self,point,poly):
        x,y = point
        n = len(poly)
        inside =False
        p1x,p1y = poly[0]
        for i in range(n+1):
            p2x,p2y = poly[i % n]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y
        return inside

    def FrontEnd(self):
        self.window = pygame.display.set_mode((800,600),0,32)
        Pos.LoadImages()        
        self.arial20 = pygame.font.SysFont('arial',20)
        pygame.display.set_caption('Snake! - Main Menu')
        while not self.quit:
            if self.newsel: self.PlayClassic()
            elif self.camsel: self.PlayCampaign()
            self.newsel = False
            self.camsel = False
            self.quitsel = False
            self.window.fill((0,0,0))
            self.window.blit(self.frontend, (0,0))
            for event in pygame.event.get():
                if event.type == 4:
                    if   self.Pip(event.pos,self.polys['newpoly']):  self.lined = 'new'
                    elif self.Pip(event.pos,self.polys['setpoly']):  self.lined = 'set'
                    elif self.Pip(event.pos,self.polys['quitpoly']): self.lined = 'quit'
                    else:self.lined = None
                elif event.type == 12:
                    pygame.quit()
                    sys.exit()
                elif event.type == 6 and event.button == 1:
                    if   self.Pip(event.pos,self.polys['newpoly']): self.selectGame=True
                    elif self.Pip(event.pos,self.polys['setpoly']): pass
                    elif self.Pip(event.pos,self.polys['quitpoly']): pygame.quit();sys.exit()
            if   self.lined == 'new': self.window.blit(self.newline,(0,0))
            elif self.lined == 'set': self.window.blit(self.setline,(0,0))
            elif self.lined == 'quit':self.window.blit(self.quitline,(0,0))
            pygame.display.update()
            if self.selectGame: self.selectGame = False; self.ModeSelect()
            Clock.tick(self.FPS)

    def ModeSelect(self):
        pygame.display.set_caption('Snake! - Mode selection')
        self.window = pygame.display.set_mode((800,600),0,32)
        self.lined = None
        while not self.quit:
            self.window.fill((0,0,0))
            self.window.blit(self.frontend, (0,0))
            self.window.blit(G.select, (0,0))
            for event in pygame.event.get():
                if event.type == 4:
                    if   self.Pip(event.pos,self.polys['newsel']):  self.lined = 'new'
                    elif self.Pip(event.pos,self.polys['camsel']):  self.lined = 'cam'
                    elif self.Pip(event.pos,self.polys['quitsel']): self.lined = 'quit'
                    else:self.lined = None
                elif event.type == 12:
                    pygame.quit()
                    sys.exit()
                elif event.type == 6 and event.button == 1:
                    if   self.Pip(event.pos,self.polys['newsel']): self.newsel = True
                    elif self.Pip(event.pos,self.polys['camsel']): self.camsel = True
                    elif self.Pip(event.pos,self.polys['quitsel']): self.quitsel = True
            if   self.lined == 'new': pygame.draw.polygon(self.window, (100,100,100), self.polys['newsel'])
            elif self.lined == 'cam': pygame.draw.polygon(self.window, (100,100,100), self.polys['camsel'])
            elif self.lined == 'quit':pygame.draw.polygon(self.window, (100,100,100), self.polys['quitsel'])
            if   self.newsel or self.camsel == True or self.quitsel == True:
                break
            self.newsel = False
            self.camsel = False
            self.quitsel = False
            pygame.display.update()
            Clock.tick(self.FPS)

Clock = pygame.time.Clock();Pos = Board();Cam = Camera();Snake = Snakes();G = Game();G.FrontEnd()
