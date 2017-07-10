import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('War of Tanks')

white = (255, 255, 255)
grey = (96, 96, 96)
black = (0, 0, 0)
red = (255, 0, 0)
light_red = (255, 51, 51)
yellow = (200, 200, 0)
light_yellow = (255, 255, 0)
green = (34, 177, 76)
light_green = (0, 255, 0)
dark_green = (45, 106, 23)
blue = (0, 0, 204)
light_blue = (51, 51, 250)

start = pygame.image.load('start.png')
city = pygame.image.load('city.png')
over = pygame.image.load('game_over.png')
bg = pygame.image.load('background.png')
tk = pygame.image.load('tank.png')
tk2 = pygame.image.load('tank2.png')
boom = pygame.image.load('boom.png')
control = pygame.image.load('ctrl.png')
clock = pygame.time.Clock()


tankWidth = 40
tankHeight = 20

turretWidth = 7
wheelWidth = 5

ground_height = 35

smallfont = pygame.font.SysFont("elephant", 22)
medfont = pygame.font.SysFont("arial", 50)
largefont = pygame.font.SysFont("algerian", 85)


def text_objects(text, color, size="small"):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()


def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((buttonx + (buttonwidth / 2)), buttony + (buttonheight / 2))
    gameDisplay.blit(textSurf, textRect)


def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (int(display_width / 2), int(display_height / 2) + y_displace)
    gameDisplay.blit(textSurf, textRect)


def tank(x, y, turPos):
    x = int(x)
    y = int(y)

    possibleTurrets = [(x - 27, y - 2),
                       (x - 26, y - 5),
                       (x - 25, y - 8),
                       (x - 23, y - 12),
                       (x - 20, y - 14),
                       (x - 18, y - 15),
                       (x - 15, y - 17),
                       (x - 13, y - 19),
                       (x - 11, y - 21)
                       ]

    pygame.draw.line(gameDisplay, dark_green, (x, y), possibleTurrets[turPos], turretWidth)
    gameDisplay.blit(tk, (x - 25, y - 10))

    return possibleTurrets[turPos]


def enemy_tank(x, y):
    x = int(x)
    y = int(y)
    gameDisplay.blit(tk2, (x - 25, y - 10))


def credits():
    credit = True

    while credit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.blit(bg, (0, 0))
        message_to_screen("Credit", green, -120, size="large")
        message_to_screen("This Lab project is done by", blue, -50)
        message_to_screen("Nazmul Haque", black, 10, size="medium")
        message_to_screen("Roll: 1510476128", black, 60)
        message_to_screen("Batch: 2014-15", black, 100)
        message_to_screen("Programming Language: Python (v 3.4.5)", black, 150)


        button("Main", 350, 500, 100, 50, yellow, light_yellow, action="main")
        button("Quit", 550, 500, 100, 50, red, light_red, action="quit")

        pygame.display.update()

        clock.tick(15)


def game_controls():
    gcont = True

    while gcont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.blit(control, (0, 0))
        message_to_screen("Controls", green, -100, size="large")
        message_to_screen("Fire: Spacebar", black, -30)
        message_to_screen("Move Turret: Up and Down arrows", black, 10)
        message_to_screen("Move Tank: Left and Right arrows", black, 50)
        message_to_screen("Pause: P", black, 90)

        button("Play", 150, 500, 100, 50, green, light_green, action="play")
        button("Main", 350, 500, 100, 50, yellow, light_yellow, action="main")
        button("Quit", 550, 500, 100, 50, red, light_red, action="quit")

        pygame.display.update()

        clock.tick(15)


def button(text, x, y, width, height, inactive_color, active_color, action=None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(click)
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x, y, width, height))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()

            if action == "controls":
                game_controls()

            if action == "credits":
                credits()

            if action == "play":
                gameLoop()

            if action == "main":
                game_intro()

    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, width, height))

    text_to_button(text, black, x, y, width, height)

def pause():
    paused = True
    message_to_screen("Paused", black, -100, size="large")
    message_to_screen("Press C to continue, Q to quit and M for main menu", black, 25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_m:
                    game_intro()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        clock.tick(5)


def barrier(xlocation, randomHeight, barrier_width):
    pygame.draw.rect(gameDisplay, grey, [xlocation, display_height - randomHeight , barrier_width, randomHeight])


def explosion(x, y):
    explode = True

    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        magnitude = 1
        size = 10

        while magnitude < size:

            gameDisplay.blit(boom, (x - 20, y - 10))

            magnitude += 1

            pygame.display.update()
            clock.tick(50)

        explode = False


def fireShell(xy, tankx, tanky, turPos, gun_power, xlocation, barrier_width, randomHeight, enemyTankX, enemyTankY):
    fire = True
    damage = 0

    startingShell = list(xy)

    #print("FIRE!", xy)

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.draw.circle(gameDisplay, red, (startingShell[0], startingShell[1]), 5)

        startingShell[0] -= (12 - turPos) * 2

        # y = x**2
        startingShell[1] += int((((startingShell[0] - xy[0]) * 0.015 / (gun_power / 50)) ** 2) - (turPos + turPos / (12 - turPos)))

        if enemyTankX + 100 > startingShell[0] > enemyTankX - 20 and enemyTankY + 60 > startingShell[1] > enemyTankY - 10:
            hit_x = int((startingShell[0]))
            hit_y = int(startingShell[1])
            damage = 25
            explosion(hit_x, hit_y)
            fire = False

        elif startingShell[1] > display_height - ground_height:
            hit_x = int((startingShell[0] * display_height - ground_height) / startingShell[1])
            hit_y = int(display_height - ground_height)
            explosion(hit_x, hit_y)
            fire = False

        check_x_1 = startingShell[0] <= xlocation + barrier_width
        check_x_2 = startingShell[0] >= xlocation

        check_y_1 = startingShell[1] <= display_height
        check_y_2 = startingShell[1] >= display_height - randomHeight

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            hit_x = int((startingShell[0]))
            hit_y = int(startingShell[1])
            print("Impact:", hit_x, hit_y)
            explosion(hit_x, hit_y)
            fire = False

        pygame.display.update()
        clock.tick(60)
    return damage

def power(level):
    text = smallfont.render("Power: " + str(level) + "%", True, black)
    gameDisplay.blit(text, [display_width / 2, 0])

def score(s):
    text = smallfont.render(" Point: "+str(s) , True, light_red)
    gameDisplay.blit(text, [0, 0])


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.blit(start, (0, 0))

        message_to_screen("Tank Battle", black, -200, size="large")
        button("Play", 150, 300, 100, 50, green, light_green, action="play")
        button("Controls", 150, 400, 100, 50, yellow, light_yellow, action="controls")
        button("Credits", 150, 500, 100, 50, blue, light_blue, action="credits")
        button("Quit", 550, 500, 100, 50, red, light_red, action="quit")


        pygame.display.update()

        clock.tick(15)

def game_over(s):
    game_over = True

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.blit(over, (0,0))
        text = medfont.render("Your Point is: " + str(s), True, white)
        gameDisplay.blit(text, [270, 460])

        button("Play Again", 150, 520, 150, 50, green, light_green, action="play")
        # button("Credits", 350, 500, 100, 50, yellow, light_yellow, action="credits")
        button("Quit", 550, 520, 100, 50, red, light_red, action="quit")

        pygame.display.update()

        clock.tick(15)

def health_bars(player_health):
    if player_health > 75:
        player_health_color = green
    elif player_health > 50:
        player_health_color = yellow
    else:
        player_health_color = red

    pygame.draw.rect(gameDisplay, player_health_color, (680, 25, player_health, 25))

def gameLoop():
    gameExit = False
    gameOver = False
    FPS = 15
    s = 0
    player_health = 100

    barrier_width = 20

    mainTankX = display_width * 0.9
    mainTankY = display_height * 0.9
    tankMove = 0
    currentTurPos = 0
    changeTur = 0

    fire_power = 50
    power_change = 0

    xlocation = (display_width / 2) + random.randint(-0.15 * display_width, 0.15 * display_width)
    randomHeight = random.randrange(display_height * 0.1, display_height * 0.5)

    enemyTankX = random.randrange(50,  200)
    enemyTankY = random.randrange(100,  200)

    while not gameExit:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:


                if event.key == pygame.K_LEFT:
                    tankMove = -5

                elif event.key == pygame.K_RIGHT:
                    tankMove = 5

                elif event.key == pygame.K_UP:
                    changeTur = 1

                elif event.key == pygame.K_DOWN:
                    changeTur = -1

                elif event.key == pygame.K_p:
                    pause()

                elif event.key == pygame.K_SPACE:
                    damage = fireShell(gun, mainTankX, mainTankY, currentTurPos, fire_power, xlocation, barrier_width,
                                       randomHeight, enemyTankX, enemyTankY)
                    if damage != 0:
                        s = s + 1
                        enemyTankX = random.randrange(50, xlocation - 200)
                        enemyTankY = random.randrange(100, display_width - 100)
                    else:
                        player_health -= 10

                elif event.key == pygame.K_a:
                    power_change = -1
                elif event.key == pygame.K_d:
                    power_change = 1

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tankMove = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    changeTur = 0

                if event.key == pygame.K_a or event.key == pygame.K_d:
                    power_change = 0


        mainTankX += tankMove

        currentTurPos += changeTur

        if currentTurPos > 8:
            currentTurPos = 8
        elif currentTurPos < 0:
            currentTurPos = 0

        if mainTankX - (tankWidth / 2) < xlocation + barrier_width:
            mainTankX += 5

        # gameDisplay.fill(white)
        gameDisplay.blit(city, (0, 0))

        health_bars(player_health)

        gun = tank(mainTankX, mainTankY, currentTurPos)
        enemy_tank(enemyTankX, enemyTankY)

        fire_power += power_change

        if fire_power > 150:
            fire_power = 150
        elif fire_power < 1:
            fire_power = 1

        power(fire_power)
        score(s)

        barrier(xlocation, randomHeight, barrier_width)
        #        gameDisplay.fill(green, rect=[0, display_height - ground_height, display_width, ground_height])
        pygame.display.update()

        if player_health < 2:
            game_over(s)

        clock.tick(FPS)

    pygame.quit()
    quit()


game_intro()
gameLoop()
