
import pygame
import time, random, os, math

# init game
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1200, 800))
done = False

# init timers
pygame.time.set_timer(pygame.USEREVENT + 1, 50) # move timer
pygame.time.set_timer(pygame.USEREVENT + 2, 100) # move timer
pygame.time.set_timer(pygame.USEREVENT + 3, 50) # move timer
pygame.time.set_timer(pygame.USEREVENT + 4, 500)
pygame.time.set_timer(pygame.USEREVENT + 5, 100)
pygame.time.set_timer(pygame.USEREVENT + 6, 1000)

# init font
font = pygame.font.Font(None,24)

# init background
bgimg = pygame.image.load("bg.png")
ww, wh = pygame.display.get_surface().get_size()
bgimg = pygame.transform.scale(bgimg, (ww,wh))
bgsize = bgimg.get_rect()

# init character info

characters = pygame.image.load("ch.png")
chsize = characters.get_rect()
chw = chsize[2] // 12
chh = chsize[3] // 8
p1_x = 0
p1_y = 0
p1_chno = random.randint(0, 6)
p1_chdr = 0
p1_chmt = 1
p1_ismove = False
p1_life = 1
p1_bullet = [0, 0, 0, 0, 0, 0] # x, y, w, h, d, l

p2_x = 0
p2_y = 0
p2_chno = random.randint(0, 6)
p2_chdr = 0
p2_chmt = 1
p2_ismove = False
p2_life = 1
p2_dashcount = 5


score = 0
# monster

monster = pygame.image.load("monster.png")
monster_size = monster.get_rect()
monster_width = monster_size[2] / 4
monster_height = monster_size[3] / 4
mob = []

def p1_move_bullet():
        if p1_bullet[5] > 0:
                if p1_bullet[4] == 0:
                        p1_bullet[1] += 20
                elif p1_bullet[4] == 1:
                        p1_bullet[0] -= 20
                elif p1_bullet[4] == 2:
                        p1_bullet[0] += 20
                elif p1_bullet[4] == 3:
                        p1_bullet[1] -= 20
                p1_bullet[5] -= 1

def draw_player1_attack():
        if p1_bullet[5] > 0:
                brect = pygame.Rect(p1_bullet[0], p1_bullet[1], p1_bullet[2], p1_bullet[3])
                pygame.draw.rect(screen, (255, 0, 0), brect)

def player1_attack():
        global p1_bullet
        if p1_bullet[5] <= 0:
                p1_bullet[5] = 15
                p1_bullet[4] = p1_chdr
                if p1_chdr == 0:
                        p1_bullet[0] = p1_x
                        p1_bullet[1] = p1_y + chh
                        p1_bullet[2] = chw
                        p1_bullet[3] = 20
                elif p1_chdr == 1:
                        p1_bullet[0] = p1_x - 20
                        p1_bullet[1] = p1_y
                        p1_bullet[2] = 20
                        p1_bullet[3] = chh
                elif p1_chdr == 2:
                        p1_bullet[0] = p1_x + chw
                        p1_bullet[1] = p1_y
                        p1_bullet[2] = 20
                        p1_bullet[3] = chh
                elif p1_chdr == 3:
                        p1_bullet[0] = p1_x
                        p1_bullet[1] = p1_y - 20
                        p1_bullet[2] = chw
                        p1_bullet[3] = 20

def zen_monster():
        global mob
        zen_xy = random.choice([[660, 60], [1110, 210], [0, 270], [180, 630]])
        zen_x = zen_xy[0]
        zen_y = zen_xy[1]
        
        if p1_life > 0 and p2_life > 0:
                target = random.randint(1, 2)
        elif p1_life > 0:
                target = 1
        else:
                target = 2

        mob.append([zen_x, zen_y, 0, 0, False, target])


def move_monster():
        global mob
        for m in mob:
                if m[4]:
                        m[2] = (m[2] + 1) % 4
                        if m[2] in [1, 2]:
                                if m[5] == 1:
                                        if m[0] < p1_x:
                                                m[0] += 5
                                        else:
                                                m[0] -= 5
                                        if m[1] < p1_y:
                                                m[1] += 5
                                        else:
                                                m[1] -= 5
                                else:
                                        if m[0] < p2_x:
                                                m[0] += 5
                                        else:
                                                m[0] -= 5
                                        if m[1] < p2_y:
                                                m[1] += 5
                                        else:
                                                m[1] -= 5

                        if m[2] == 0:
                                m[4] = False

def start_move_monster():
        global mob
        for m in mob:
                if not m[4]:
                        m[2] = 0
                        m[4] = True
                        if m[5] == 1:
                                if m[0] < p1_x:
                                        m[3] = 2
                                else:
                                        m[3] = 1
                                if m[1] < p1_y:
                                        m[3] = 0
                                else:
                                        m[3] = 3
                        else:
                                if m[0] < p2_x:
                                        m[3] = 2
                                else:
                                        m[3] = 1
                                if m[1] < p2_y:
                                        m[3] = 0
                                else:
                                        m[3] = 3


def get_mob_rect(direc, mot):
        x = mot * monster_width
        y = direc * monster_height
        return (x, y, monster_width, monster_height)


def draw_monster():
        global mob
        for m in mob:
                drawrect = pygame.Rect(m[0], m[1], monster_width, monster_height) 
                mobrect = get_mob_rect(m[3], m[2])
                screen.blit(monster, drawrect, mobrect)


def get_ch(chno, direction, motion):
        x = ((chno%4) * (chw*3)) + (motion * chw)
        y = (chno // 4) * (chh*4) + (direction * chh)
        return (x, y, chw, chh)


def player1_move():
        global p1_ismove, p1_chmt, p1_chdr, p1_x, p1_y
        if p1_ismove:
                p1_chmt = (p1_chmt + 1) % 3
                if p1_chdr == 0:
                        p1_y += 10
                        if (p1_y+chh) > 800:
                                p1_y = p1_y - chh
                elif p1_chdr == 1:
                        p1_x -= 10
                        if p1_x < 0:
                                p1_x = 0
                elif p1_chdr == 2:
                        p1_x += 10
                        if (p1_x+chw) > 1200:
                                p1_x = p1_x - chw
                elif p1_chdr == 3:
                        p1_y -= 10
                        if p1_y < 0:
                                p1_y = 0

                if p1_chmt == 1:
                        p1_ismove = False

def player1_moveup():
        global p1_ismove, p1_chmt, p1_chdr
        if not p1_ismove:
                p1_ismove = True
                p1_chdr = 3


def player1_movedown():
        global p1_ismove, p1_chmt, p1_chdr
        if not p1_ismove:
                p1_ismove = True
                p1_chdr = 0


def player1_moveleft():
        global p1_ismove, p1_chmt, p1_chdr
        if not p1_ismove:
                p1_ismove = True
                p1_chdr = 1


def player1_moveright():
        global p1_ismove, p1_chmt, p1_chdr
        if not p1_ismove:
                p1_ismove = True
                p1_chdr = 2


def player1_draw():
        global p1_x, p1_y
        prect = pygame.Rect(p1_x, p1_y, chw, chh)
        chrect = get_ch(p1_chno, p1_chdr, p1_chmt)
        screen.blit(characters, prect, chrect)

def player2_move():
        global p2_ismove, p2_chmt, p2_chdr, p2_x, p2_y
        if p2_ismove:
                p2_chmt = (p2_chmt + 1) % 3
                if p2_chdr == 0:
                        p2_y += 10
                        if (p2_y + chh) > 800:
                                p2_y = p2_y - chh
                elif p2_chdr == 1:
                        p2_x -= 10
                        if p2_x < 0:
                                p2_x = 0
                elif p2_chdr == 2:
                        p2_x += 10
                        if (p2_x + chw) > 1200:
                                p2_x = p2_x - chw
                elif p2_chdr == 3:
                        p2_y -= 10
                        if p2_y < 0:
                                p2_y = 0

                if p2_chmt == 1:
                        p2_ismove = False

def player2_moveup():
        global p2_ismove, p2_chmt, p2_chdr
        if not p2_ismove:
                p2_ismove = True
                p2_chdr = 3


def player2_movedown():
        global p2_ismove, p2_chmt, p2_chdr
        if not p2_ismove:
                p2_ismove = True
                p2_chdr = 0


def player2_moveleft():
        global p2_ismove, p2_chmt, p2_chdr
        if not p2_ismove:
                p2_ismove = True
                p2_chdr = 1


def player2_moveright():
        global p2_ismove, p2_chmt, p2_chdr
        if not p2_ismove:
                p2_ismove = True
                p2_chdr = 2


def player2_draw():
        global p2_x, p2_y
        prect = pygame.Rect(p2_x, p2_y, chw, chh)
        chrect = get_ch(p2_chno, p2_chdr, p2_chmt)
        screen.blit(characters, prect, chrect)


def draw_background():
        screen.blit(bgimg, bgsize)


def collide_player():
        global p1_life, p2_life, mob, score
        p1rect = pygame.Rect(p1_x, p1_y, chw, chh)
        p2rect = pygame.Rect(p2_x, p2_y, chw, chh)

        if p1_bullet[5] > 0:
                brect = pygame.Rect(p1_bullet[0], p1_bullet[1], p1_bullet[2], p1_bullet[3])
                delmob = []
                for m in mob:
                        mrect = pygame.Rect(m[0], m[1], monster_width, monster_height)
                        if mrect.colliderect(brect):
                                delmob.append(m)

                for m in delmob:
                        if m in mob:
                                score += 100
                                mob.remove(m)

        for m in mob:
                mrect = pygame.Rect(m[0], m[1], monster_width, monster_height)
                if p1_life > 0 and mrect.colliderect(p1rect):
                        p1_life = 0
                if p2_life > 0 and mrect.colliderect(p2rect):
                        p2_life = 0

def player2_dash():
        global p2_dashcount, p2_x, p2_y, score
        if p2_dashcount > 0:
                p2_dashcount -= 1
                if p2_chdr == 0:
                        p2_y += 50
                elif p2_chdr == 1:
                        p2_x -= 50
                elif p2_chdr == 2:
                        p2_x += 50
                elif p2_chdr == 3:
                        p2_y -= 50
                
                if p2_y < 0:
                        p2_y = 0
                if (p2_y+chh) > 800:
                        p2_y = 800 - chh
                if p2_x < 0:
                        p2_x = 0
                if (p2_x+chw) > 1200:
                        p2_x = 1200 - chw

                delrect = pygame.Rect(p2_x-60, p2_y-60, 120, 120)
                delmob = []
                for m in mob:
                        mrect = pygame.Rect(m[0], m[1], monster_width, monster_height)
                        if delrect.colliderect(mrect):
                                delmob.append(m)

                for m in delmob:
                        if m in mob:
                                score += 100
                                mob.remove(m)


while not done and (p1_life > 0 or p2_life > 0):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == (pygame.USEREVENT + 1):
                        if p1_life > 0: player1_move()
                        if p2_life > 0: player2_move()
                if event.type == (pygame.USEREVENT + 2):
                        start_move_monster()
                if event.type == (pygame.USEREVENT + 3):
                        move_monster()
                if event.type == (pygame.USEREVENT + 4):
                        zen_monster()
                if event.type == (pygame.USEREVENT + 5):
                        p1_move_bullet()
                if event.type == (pygame.USEREVENT + 6):
                        if p2_dashcount < 5:
                                p2_dashcount += 1
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
                        player2_dash()
        
        
        pressed = pygame.key.get_pressed()

        # player1 key 
        if p1_life > 0:
                if pressed[pygame.K_w]: 
                        player1_moveup()
                if pressed[pygame.K_s]: 
                        player1_movedown()
                if pressed[pygame.K_a]: 
                        player1_moveleft()
                if pressed[pygame.K_d]: 
                        player1_moveright()
                if pressed[pygame.K_SPACE]:
                        player1_attack()
                if pressed[pygame.K_LSHIFT]:
                        p2_x = p1_x
                        p2_y = p1_y

        # player2 key
        if p2_life > 0:
                if pressed[pygame.K_UP]: 
                        player2_moveup()
                if pressed[pygame.K_DOWN]: 
                        player2_movedown()
                if pressed[pygame.K_LEFT]: 
                        player2_moveleft()
                if pressed[pygame.K_RIGHT]: 
                        player2_moveright()
                if pressed[pygame.K_RSHIFT]:
                        p1_x = p2_x
                        p1_y = p2_y
                
        
        #print(p2_x, p2_y)
        screen.fill((255, 255, 255))
        
        collide_player()
        draw_background()
        if p1_life > 0: player1_draw()
        if p2_life > 0: player2_draw()
        draw_monster()
        draw_player1_attack()

        text = font.render('score: {0}'.format(score), True, (255,0,0),(255,255,255))
        textrect = pygame.Rect(10, 10, 100, 100)
        screen.blit(text, textrect)

        text = font.render('p2 dash: {0}'.format(p2_dashcount), True, (128,128,128),(255,255,255))
        textrect = pygame.Rect(200, 10, 100, 100)
        screen.blit(text, textrect)


        pygame.display.flip()
        clock.tick(60)
         
print('score:', score)