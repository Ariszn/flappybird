import pygame as pg
from pygame.locals import *     #pygame所有常量
from itertools import cycle     #迭代器
from tkinter import *
from PIL import Image, ImageTk
import random
import sys

def GetObjectAlpha(object_image):
    '''用于获取图片的Alpha层信息 不为0的像素点则True'''
    alpha_matrix = []
    for i in range(object_image.get_width()):
        alpha_matrix.append([])
        for j in range(object_image.get_height()):
            if object_image.get_at((i, j))[3] != 0:
                alpha_matrix[i].append(True)
            else:
                alpha_matrix[i].append(False)

    return alpha_matrix


class Bird:
    def __init__(self):
        self.Speed = -9  # up
        self.Acc = 1  # down
        self.DownSpeed = 10

        self.Rot = 45  # 最初角度
        self.Av = 3  # 角速度
        self.MinAn = 20  # 最小的角度

        self.FlapAcc = -9
        self.Flapped = False

        # 三种颜色的小鸟随机产生
        self.ColorBirds = (
            # red bird
            (
                'assets/sprites/redbird-upflap.png',
                'assets/sprites/redbird-midflap.png',
                'assets/sprites/redbird-downflap.png',
            ),
            # blue bird
            (
                # amount by which base can maximum shift to left
                'assets/sprites/bluebird-upflap.png',
                'assets/sprites/bluebird-midflap.png',
                'assets/sprites/bluebird-downflap.png',
            ),
            # yellow bird
            (
                'assets/sprites/yellowbird-upflap.png',
                'assets/sprites/yellowbird-midflap.png',
                'assets/sprites/yellowbird-downflap.png',
            ),
        )


    def getRandomBird(self):
        '''生成随机颜色小鸟'''
        choice = random.randint(0, len(self.ColorBirds) - 1)

        chosenBird = (
            pg.image.load(self.ColorBirds[choice][0]).convert_alpha(),
            pg.image.load(self.ColorBirds[choice][1]).convert_alpha(),
            pg.image.load(self.ColorBirds[choice][2]).convert_alpha(),
        )
        return chosenBird

    def getBirdAlpha(self):
        '''获取小鸟三个姿势的Alpha信息'''
        ALPHA['bird'] = (GetObjectAlpha(OBJECT['bird'][0]),
                         GetObjectAlpha(OBJECT['bird'][1]),
                         GetObjectAlpha(OBJECT['bird'][2]),
                         )


class Gold:
    def __init__(self):
        self.goldlist = []

    def getGoldAlpha(self):
        ALPHA['Gold'] = GetObjectAlpha(OBJECT['Gold'])

    def getgoldy(self):
        y = random.randint(int(GRASS_Y * 0.3), int(GRASS_Y * 0.7))
        return y

    def Addgold(self):
        self.goldlist.append({'x': int(WIDTH * 0.8) + 10, 'y': self.getgoldy()})


class Pipe:
    def __init__(self):
        # 上管道和下管道
        self.upperPipeGroup = []
        self.lowerPipeGroup = []

    def getPipeAlpha(self):
        '''Initialize the pipe alpha'''
        ALPHA['Upper_pipe'] = GetObjectAlpha(OBJECT['Upper_pipe'])
        ALPHA['Lower_pipe'] = GetObjectAlpha(OBJECT['Lower_pipe'])

    def getRandomPipe(self):
        '''return Y index of the upper and lower pipes '''
        gapY = random.randint(0, int(GRASS_Y * 0.6 - PIPEGAP))
        gapY += int(GRASS_Y * 0.2)
        pipe_height = OBJECT['Upper_pipe'].get_height()
        # pipeX = WIDTH + 8

        return [gapY - pipe_height, gapY + PIPEGAP]

    def getPipeGroups(self):
        '''initialize the pipe groups'''
        pipeYGroup1 = self.getRandomPipe()
        pipeYGroup2 = self.getRandomPipe()

        self.upperPipeGroup = [
            {'x': WIDTH + 150, 'y': pipeYGroup1[0]},
            {'x': WIDTH + 300, 'y': pipeYGroup2[0]}
        ]

        self.lowerPipeGroup = [
            {'x': WIDTH + 150, 'y': pipeYGroup1[1]},
            {'x': WIDTH + 300, 'y': pipeYGroup2[1]}
        ]

    def addNewPipe(self):
        '''add new pipeGroup(upper one and lower one) in the screen'''
        newPipe = self.getRandomPipe()
        self.upperPipeGroup.append({'x': WIDTH + 10, 'y': newPipe[0]})
        self.lowerPipeGroup.append({'x': WIDTH + 10, 'y': newPipe[1]})


class Game:
    def __init__(self):
        # 设置pygame初始的各种音效和图像列表
        # 窗口标题，长宽初始化，clock设置

        '''
        全局变量（没有变化的）
        #WIDTH、HEIGHT：屏幕宽度、屏幕高度
        #FPS：刷新的帧率
        #PIPEGAP：管道中间缝隙宽度
        #GRASSY：草地Y坐标
        '''
        global WIDTH, HEIGHT, FPS, PIPEGAP, GRASS_Y

        WIDTH, HEIGHT = 288, 512  # 根据图片素材大小设定
        PIPEGAP = 110
        GRASS_Y = int(HEIGHT * 0.79)  # 下面草地的Y坐标
        FPS = 30

        '''
        全局变量
        #OBJECT：图片
        #MUSIC：音效
        #ALPHA：图片透明层，用于像素级别判断碰撞
        '''
        global OBJECT, MUSIC, ALPHA
        OBJECT, MUSIC, ALPHA = {}, {}, {}
        self.score = 0

        self.bird = Bird()
        self.pipe = Pipe()
        self.gold = Gold()
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('Our Flappy Bird')

    def InitialOJandMS(self):
        '''初始化OBJECT和MUSIC'''

        OBJECT['Upper_pipe'] = pg.transform.rotate(pg.image.load('assets/sprites/pipe-green.png').convert_alpha(), 180)
        OBJECT['Lower_pipe'] = pg.image.load('assets/sprites/pipe-green.png').convert_alpha()
        OBJECT['Gold'] = pg.image.load('assets/sprites/gold2.png').convert_alpha()
        OBJECT['numbers'] = (
            pg.image.load('assets/sprites/0.png').convert_alpha(),
            pg.image.load('assets/sprites/1.png').convert_alpha(),
            pg.image.load('assets/sprites/2.png').convert_alpha(),
            pg.image.load('assets/sprites/3.png').convert_alpha(),
            pg.image.load('assets/sprites/4.png').convert_alpha(),
            pg.image.load('assets/sprites/5.png').convert_alpha(),
            pg.image.load('assets/sprites/6.png').convert_alpha(),
            pg.image.load('assets/sprites/7.png').convert_alpha(),
            pg.image.load('assets/sprites/8.png').convert_alpha(),
            pg.image.load('assets/sprites/9.png').convert_alpha()
        )

        OBJECT['gameover'] = pg.image.load('assets/sprites/gameover.png').convert_alpha()
        OBJECT['welcome'] = pg.image.load('assets/sprites/message.png').convert_alpha()
        OBJECT['grass'] = pg.image.load('assets/sprites/base.png').convert_alpha()
        OBJECT['background'] = pg.image.load('assets/sprites/background-day.png').convert()
        OBJECT['bird'] = self.bird.getRandomBird()
        OBJECT['play'] = pg.image.load('assets/sprites/play.png').convert_alpha()
        OBJECT['rank'] = pg.image.load('assets/sprites/rank.png').convert_alpha()
        OBJECT['ranked'] = pg.image.load('assets/sprites/ranked.png').convert_alpha()
        OBJECT['exit'] = pg.image.load('assets/sprites/exit.png').convert_alpha()
        OBJECT['tip'] = pg.image.load('assets/sprites/tip.png').convert_alpha()
        
        MUSIC['die'] = pg.mixer.Sound('assets/audio/die.wav')
        MUSIC['hit'] = pg.mixer.Sound('assets/audio/hit.wav')
        MUSIC['score'] = pg.mixer.Sound('assets/audio/point.wav')
        MUSIC['swoosh'] = pg.mixer.Sound('assets/audio/swoosh.wav')
        MUSIC['flywing'] = pg.mixer.Sound('assets/audio/wing.wav')

    def InitialAlpha(self):
        self.bird.getBirdAlpha()
        self.pipe.getPipeAlpha()
        self.gold.getGoldAlpha()

        
    def GameInterface(self):
        '''游戏欢迎界面 随时接收键盘点击事件开始游戏'''
        '''开始游戏时返回当前小鸟位置以及状态 便于开始游戏时能承接'''

        bird_height = OBJECT['bird'][0].get_height()
        welcome_width = OBJECT['welcome'].get_width()
        welcome_height = OBJECT['welcome'].get_height()
        play_width = OBJECT['play'].get_width()
        play_height = OBJECT['play'].get_height()
        rank_width = OBJECT['rank'].get_width()
        rank_height = OBJECT['rank'].get_height()
        
        self.bird.x = int(WIDTH*0.2)
        self.bird.y = int((HEIGHT-bird_height)/2)

        welcome_x = int((WIDTH-welcome_width)/2)
        welcome_y = int((HEIGHT-welcome_height)/3)
        play_x = int(WIDTH-play_width*3)
        play_y = int(HEIGHT-play_height*5)
        rank_x = int(WIDTH-rank_width*1.66)
        rank_y = int(HEIGHT-play_height*5.08)

        grass_x = 0
        global GRASS_SHIFT
        GRASS_SHIFT = OBJECT['grass'].get_width() - OBJECT['background'].get_width()

        # 小鸟动作
        bird_motion = 0
        it = 0
        bird_motion_it = cycle([0, 1, 2, 1])

        # val:小鸟位移大小 dir：+1为上，-1为下
        birdSHMval = {'val': 0, 'dir': 1}

        while True:
            for event in pg.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pg.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    # make first flap sound and return values for mainGame
                    MUSIC['flywing'].play()
                    self.bird.y += birdSHMval['val']
                    return {
                        'grass_x': grass_x,
                        'bird_motion_it': bird_motion_it
                    }
                if event.type == pg.MOUSEBUTTONDOWN and play_x<=event.pos[0]<=play_x+play_width and play_y<=event.pos[1]<=play_y+play_height :
                    # 鼠标点击  play
                    MUSIC['flywing'].play()
                    self.bird.y += birdSHMval['val']
                    return {
                        'grass_x': grass_x,
                        'bird_motion_it': bird_motion_it
                    }
                if event.type == pg.MOUSEBUTTONDOWN and rank_x<=event.pos[0]<=rank_x+rank_width and rank_y<=event.pos[1]<=rank_y+rank_height :
                    # 鼠标点击 rank
                    MUSIC['swoosh'].play()
                    rank = Rank()

            '''在循环内不断更新小鸟上下摆动的动作和草地的平移'''
            if it and it % 3 == 0:
                bird_motion = next(bird_motion_it)
            it = (it + 1) % 30
            grass_x = (grass_x - 4) % -GRASS_SHIFT

            '''让val在[-8，+8]之间变化'''
            if abs(birdSHMval['val']) == 8:
                birdSHMval['dir'] *= -1

            if birdSHMval['dir'] == 1:
                birdSHMval['val'] += 1
            else:
                birdSHMval['val'] -= 1

            '''根据设定位置，在屏幕上绘制位图，不断更新窗口'''
            self.screen.blit(OBJECT['background'],(0,0))
            self.screen.blit(OBJECT['bird'][bird_motion],(self.bird.x,self.bird.y+birdSHMval['val']))
            self.screen.blit(OBJECT['welcome'],(welcome_x,welcome_y))
            self.screen.blit(OBJECT['grass'],(grass_x,GRASS_Y))
            self.screen.blit(OBJECT['play'],(play_x,play_y))
            self.screen.blit(OBJECT['rank'],(rank_x,rank_y))

            pg.display.update()
            self.clock.tick(FPS)
            
    def Gaming(self, birdState):
        '''开始游戏 不断调整小鸟的高度、角度和管道的移动 判断碰撞'''
        bird_motion_it = birdState['bird_motion_it']
        grass_x, grass_y = birdState['grass_x'], GRASS_Y

        bird_motion = it = 0

        self.pipe.getPipeGroups()

        '''小鸟的运动速度，运动加速度，最初角度，角速度，摆动速度
        self.bird.Speed = -9 #up
        self.bird.Acc = 1 #down
        self.bird.DownSpeed = 10

        self.bird.Rot = 45 #最初角度
        self.bird.Av = 3 #角速度
        self.bird.MinAn = 20 #最小的角度

        self.bird.FlapAcc = -9
        self.bird.Flapped = False'''

        ''''''
        pipeSpeed = -4  # 管道在x轴的移动速度
        num = random.randint(3, 5)  # 生成金币的上限
        flag = 0
        while True:
            for event in pg.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pg.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if self.bird.y + OBJECT['bird'][0].get_height() > 0:  # 如果小鸟高度在限定范围内则继续上升
                        self.bird.Speed = self.bird.FlapAcc  # 上升
                        self.bird.Flapped = True
                        MUSIC['flywing'].play()  # 并播放飞行音效
                        #按键按下的同时判断是否吃到金币
                        ifgold = self.checkgoldCrash(bird_motion)
                        if ifgold:
                            self.score += 3
                            self.gold.goldlist.pop(0)
                            MUSIC['score'].play();
                        # check if midlle position of bird in pipe and get score
                        self.checkScore()

            # 检查管道碰撞
            isCrashed = self.checkCrash(bird_motion)
            if isCrashed['crashed']:
                return {
                    'CrashGround': isCrashed['ground'],
                    'grass_x': grass_x
                }

            #检查金币碰撞
            ifgold = self.checkgoldCrash(bird_motion)
            if ifgold:
                self.score += 3
                self.gold.goldlist.pop(0)
                MUSIC['score'].play();
            # check if midlle position of bird in pipe and get score
            self.checkScore()

            # grass shift
            grass_x = (grass_x - 4) % - GRASS_SHIFT

            # bird motion change
            if it and it % 3 == 0:
                bird_motion = next(bird_motion_it)
            it = (it + 1) % 20

            # bird rotates
            if self.bird.Rot > -90:
                self.bird.Rot -= self.bird.Av

            #小鸟加速下降
            if self.bird.Speed < self.bird.DownSpeed and not self.bird.Flapped:
                self.bird.Speed += self.bird.Acc

            # if flap the bird then make its angle 45
            if self.bird.Flapped:
                self.bird.Flapped = False
                self.bird.Rot = 45

            # make the bird down or up
            bird_height = OBJECT['bird'][bird_motion].get_height()
            self.bird.y += min(self.bird.Speed, grass_y - self.bird.y - bird_height)

            # Shift the pipes left
            for up, low in zip(self.pipe.upperPipeGroup, self.pipe.lowerPipeGroup):
                up['x'] += pipeSpeed
                low['x'] += pipeSpeed

            # Shift the golds left
            if self.gold.goldlist:
                for i in self.gold.goldlist:
                    i['x'] += pipeSpeed

            # add new pipes when the first pipegroup disappears
            if len(self.pipe.upperPipeGroup) > 0 and 0 < self.pipe.upperPipeGroup[0]['x'] < 5:
                self.pipe.addNewPipe()
                flag += 1

            if flag == num:  # 如果次数到达了生成金币的次数
                self.gold.Addgold()  # 生成金币
                flag = 0
                num = random.randint(3, 5)  # 更新随机数

            # remove the first pipegroup when it disappears
            pipe_width = OBJECT['Upper_pipe'].get_width()
            if len(self.pipe.upperPipeGroup) > 0 and pipe_width + self.pipe.upperPipeGroup[0]['x'] < 0:
                self.pipe.upperPipeGroup.pop(0)
                self.pipe.lowerPipeGroup.pop(0)

            # remove the first gold when it disappears
            gold_width = OBJECT['Gold'].get_width()
            if len(self.gold.goldlist) >0 and pipe_width + self.gold.goldlist[0]['x'] < 0:
                self.gold.goldlist.pop(0)

            # show the objects on the screen
            self.screen.blit(OBJECT['background'], (0, 0))

            for up, low in zip(self.pipe.upperPipeGroup, self.pipe.lowerPipeGroup):
                self.screen.blit(OBJECT['Upper_pipe'], (up['x'], up['y']))
                self.screen.blit(OBJECT['Lower_pipe'], (low['x'], low['y']))

            self.screen.blit(OBJECT['grass'], (grass_x, grass_y))

            if self.gold.goldlist:
                for i in self.gold.goldlist:
                    self.screen.blit(OBJECT['Gold'], (i['x'], i['y']))

            # print the score
            self.showScore()

            # visibleRot: the angle used in rotating the bird image
            visibleRot = self.bird.MinAn
            if self.bird.Rot <= self.bird.MinAn:
                visibleRot = self.bird.Rot

            # rotate the image of bird
            bird_rotated = pg.transform.rotate(OBJECT['bird'][bird_motion], visibleRot)
            self.screen.blit(bird_rotated, (self.bird.x, self.bird.y))

            pg.display.update()
            self.clock.tick(FPS)

    def checkCrash(self, motion):
        '''
        判断是否撞到地面或者管道
        是否撞地：判断当前y+图片高度是否到达地面的y
        撞到管道：生成小鸟和两条管道的矩形，先判断是否有相交矩形，无相交矩形则没有碰撞
                 若有相交矩形，则用ALPHA矩阵来判断在该相交矩形内是否有像素块重叠，有则说明像素碰撞
        '''
        bird_width, bird_height = OBJECT['bird'][0].get_width(), OBJECT['bird'][0].get_height()
        pipe_width, pipe_height = OBJECT['Upper_pipe'].get_width(), OBJECT['Upper_pipe'].get_height()
        # collide with the Grass
        if self.bird.y + bird_height >= GRASS_Y - 1:
            return {'crashed': True, 'ground': True}
        else:
            # generate a rect of the bird
            birdRect = pg.Rect(self.bird.x, self.bird.y, bird_width, bird_height)
            for uppipe, lowpipe in zip(self.pipe.upperPipeGroup, self.pipe.lowerPipeGroup):
                # generate rects of the upper and lower pipes
                upRect = pg.Rect(uppipe['x'], uppipe['y'], pipe_width, pipe_height)
                lowRect = pg.Rect(lowpipe['x'], lowpipe['y'], pipe_width, pipe_height)

                # check if crashed
                Crashed1 = self.pixelCollision(birdRect, upRect, motion, 0)
                Crashed2 = self.pixelCollision(birdRect, lowRect, motion, 1)
                if Crashed1 or Crashed2:
                    return {'crashed': True, 'ground': False}

        return {'crashed': False, 'ground': False}

    def checkgoldCrash(self, motion):
        '''
        检测是否撞到金币
        '''
        bird_width, bird_height = OBJECT['bird'][0].get_width(), OBJECT['bird'][0].get_height()
        gold_width, gold_height = OBJECT['Gold'].get_width(), OBJECT['Gold'].get_height()
        birdRect = pg.Rect(self.bird.x, self.bird.y, bird_width, bird_height)
        for gold in self.gold.goldlist:
            goldRect = pg.Rect(gold['x'], gold['y'], gold_width, gold_height)
            #print(type(gold['x']), type(gold['y']))
            Crashed = self.goldpixelCollision(birdRect, goldRect, motion)
            if Crashed:
                return True
            else:
                return False

    def goldpixelCollision(self, birdRect, goldRect, motion):
        '''check collision of two objects by their pixels'''

        # get Alpha of objects
        birdAlpha = ALPHA['bird'][motion]
        goldAlpha = ALPHA['Gold']

        # get the intersecting rectangle
        interRect = birdRect.clip(goldRect)
        if interRect.width == 0 or interRect.height == 0:
            return False

        # 算出bird与重叠的矩形的x，y偏移量
        bird_xoff = interRect.x - birdRect.x
        bird_yoff = interRect.y - birdRect.y

        # 算出gold与重叠的矩形的x，y偏移量
        gold_xoff = interRect.x - goldRect.x
        gold_yoff = interRect.y - goldRect.y

        # 检查两个物体在重叠矩形处的ALPHA层是否存在像素重叠
        for x in range(interRect.width):
            for y in range(interRect.height):
                if birdAlpha[x + bird_xoff][y + bird_yoff] and goldAlpha[gold_xoff + x][gold_yoff + y]:
                    return True

        return False

    def pixelCollision(self, birdRect, pipeRect, motion, key):
        '''check collision of two objects by their pixels'''

        # get Alpha of objects
        birdAlpha = ALPHA['bird'][motion]
        if key == 0:
            PipeAlpha = ALPHA['Upper_pipe']
        else:
            PipeAlpha = ALPHA['Lower_pipe']

        # get the intersecting rectangle
        interRect = birdRect.clip(pipeRect)
        if interRect.width == 0 or interRect.height == 0:
            return False

        # 算出bird与重叠的矩形的x，y偏移量
        bird_xoff = interRect.x - birdRect.x
        bird_yoff = interRect.y - birdRect.y

        # 算出pipe与重叠的矩形的x，y偏移量
        pipe_xoff = interRect.x - pipeRect.x
        pipe_yoff = interRect.y - pipeRect.y

        # 检查两个物体在重叠矩形处的ALPHA层是否存在像素重叠
        for x in range(interRect.width):
            for y in range(interRect.height):
                if birdAlpha[x + bird_xoff][y + bird_yoff] and PipeAlpha[pipe_xoff + x][pipe_yoff + y]:
                    return True

        return False

    def checkScore(self):
        '''判断是否得分：管道中点x坐标 < 小鸟中点x坐标 < 管道中点+3（防止重复加分）'''
        bird_mid = self.bird.x + OBJECT['bird'][0].get_width() / 2
        for pipe in self.pipe.upperPipeGroup:
            pipe_mid = pipe['x'] + OBJECT['Upper_pipe'].get_width() / 2
            if bird_mid + 1 >= pipe_mid and bird_mid < pipe_mid + 3:
                self.score += 1
                MUSIC['score'].play()

    def showScore(self):
        '''在屏幕上打印分数'''
        scoreDigits = [int(x) for x in list(str(self.score))]
        totalWidth = 0  # total width of all numbers to be printed

        for digit in scoreDigits:
            totalWidth += OBJECT['numbers'][digit].get_width()

        Xoffset = int((WIDTH - totalWidth) / 2)

        for digit in scoreDigits:
            self.screen.blit(OBJECT['numbers'][digit], (Xoffset, int(HEIGHT * 0.1)))
            Xoffset += OBJECT['numbers'][digit].get_width()

    def GameOver(self, Crash):
        '''make the bird down and show game over'''
        bird_height = OBJECT['bird'][0].get_height()
        # 加快bird的角速度和向下的加速度
        self.bird.Acc = 2  # down
        self.bird.Av = 7  # 角速度

        grass_x = Crash['grass_x']

        # play the music
        MUSIC['hit'].play()
        MUSIC['die'].play()

        # 记录玩家及其分数
        f = open('ranking.txt', 'a+')
        f.write(name)
        f.write(':')
        f.write(str(self.score))
        f.write('\n')
        f.close()

        ranked_width = OBJECT['ranked'].get_width()
        ranked_height = OBJECT['ranked'].get_height()        
        ranked_x = int(WIDTH-ranked_width*2.33)
        ranked_y = int(HEIGHT-ranked_height*6.66)

        exit_width = OBJECT['ranked'].get_width()
        exit_height = OBJECT['ranked'].get_height()    
        exit_x = int(WIDTH-ranked_width*2.33)
        exit_y = int(HEIGHT-ranked_height*5.66)

        tip_width = OBJECT['tip'].get_width()
        tip_height = OBJECT['tip'].get_height()        
        tip_x = int(WIDTH-tip_width*1.414)
        tip_y = int(HEIGHT-tip_height*1.66)
        
        while True:
            for event in pg.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE) or \
                   event.type == pg.MOUSEBUTTONDOWN and exit_x<=event.pos[0]<=exit_x+exit_width and exit_y<=event.pos[1]<=exit_y+exit_height :
                    pg.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    # quit the game until the bird hit on ground
                    if self.bird.y + bird_height >= GRASS_Y:  
                        return
                if event.type == pg.MOUSEBUTTONDOWN and ranked_x<=event.pos[0]<=ranked_x+ranked_width and ranked_y<=event.pos[1]<=ranked_y+ranked_height :
                    # 鼠标点击 rank 所在的位置，显示排行榜
                    MUSIC['flywing'].play()
                    rank = Rank()


            # let the bird down
            if self.bird.y + bird_height < GRASS_Y:
                self.bird.y += min(self.bird.Speed, GRASS_Y - self.bird.y - bird_height)

            # accelerate the bird down
            if self.bird.Speed < 15:
                self.bird.Speed += self.bird.Acc

            # rotate
            if not Crash['CrashGround']:
                if self.bird.Rot > -90:
                    self.bird.Rot -= self.bird.Av

            '''在屏幕绘制位图'''
            self.screen.blit(OBJECT['background'], (0, 0))

            for up, low in zip(self.pipe.upperPipeGroup, self.pipe.lowerPipeGroup):
                self.screen.blit(OBJECT['Upper_pipe'], (up['x'], up['y']))
                self.screen.blit(OBJECT['Lower_pipe'], (low['x'], low['y']))

            self.screen.blit(OBJECT['grass'], (grass_x, GRASS_Y))
            self.showScore()

            # 旋转小鸟
            bird_rotated = pg.transform.rotate(OBJECT['bird'][1], self.bird.Rot)
            
            self.screen.blit(bird_rotated, (self.bird.x, self.bird.y))
            self.screen.blit(OBJECT['gameover'], (50, 180))
            self.screen.blit(OBJECT['ranked'],(ranked_x, ranked_y))
            self.screen.blit(OBJECT['exit'],(exit_x, exit_y))
            self.screen.blit(OBJECT['tip'],(tip_x, tip_y))
            
            pg.display.update()
            self.clock.tick(FPS)

    def RUNGAME(self):
        '''游戏入口'''
        while (True):
            self.score = 0
            self.bird = Bird()
            self.pipe = Pipe()

            self.InitialOJandMS()
            self.InitialAlpha()
            bird_state = self.GameInterface()
            Crash = self.Gaming(bird_state)
            self.GameOver(Crash)


class Rank():
    # 排行榜类
    def __init__(self):
        self.root = Tk()
        self.root.title('Player Ranking')
        self.canvas = Canvas(self.root, width=400, height=400)
        # 创建背景图
        imgpath ='assets/sprites/rank_bg.png'
        img = Image.open(imgpath)
        photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(200, 200, image=photo)
        self.ranking()

        self.canvas.pack()
        self.root.mainloop()
        
    def ranking(self):
        #读取玩家姓名和分数，生成字典{name：score}
        f = open('ranking.txt','r')
        dic = []
        for line in f:
            v = line.strip().split(':')
            for i in dic:
                if i[0]==v[0] and int(i[1])>int(v[1]): # 判断某一玩家是否有记录，取记录最大值
                    v[1] = i[1]  
            dic.append(v)
        dic=dict(dic)
        f.close()
        rank = sorted(dic.items(), key = lambda item: int(item[1]), reverse=True) #对字典排序

        base_y=180
        base = 37
        while (True):
            # 排行榜分数排名前五
            for i in range(len(rank)):
                self.canvas.create_window(204, 180+37*i, window=Label(self.root, text=rank[i][0], padx=5, pady=4))
                self.canvas.create_window(303, 180+37*i, window=Label(self.root, text=rank[i][1], padx=5, pady=4))
                if i==4:
                    break
            break

class Login():
    # 玩家登录，保存记录
    def __init__(self):
        self.root = Tk()
        self.root.title('Player Login')
        canvas = Canvas(self.root, width=288, height=512)
        # 创建登录界面背景图
        imgpath ='assets/sprites/background-day.png'
        img = Image.open(imgpath)
        photo = ImageTk.PhotoImage(img)
        canvas.create_image(148, 258, image=photo)
        imgpath1 ='assets/sprites/welcome.png'
        img1 = Image.open(imgpath1)
        photo1 = ImageTk.PhotoImage(img1)
        canvas.create_image(150, 88, image=photo1)
        # 玩家信息
        canvas.create_window(66, 180, window=Label(self.root, text='Player', padx=5, pady=4))
        #canvas.create_window(66, 220, window=Label(self.root, text='Password',  padx=5, pady=4))
        # 账号密码输入框
        self.playername = StringVar()
        canvas.create_window(188, 180, window=Entry(self.root, borderwidth=3, textvariable=self.playername))
        #canvas.create_window(188, 220, window=Entry(self.root, borderwidth=3,  show='*'))
        # 创建登录按钮
        canvas.create_window(144, 280, window=Button(self.root, width=15, bg='#87CEEB', text='Login', command=self.login))
       
        canvas.pack()
        self.root.mainloop()
        
    def login(self):
        # 保存玩家姓名
        global name
        name = self.playername.get()
        self.root.destroy()
        game = Game()
        game.RUNGAME()

# 登录游戏
Login()
