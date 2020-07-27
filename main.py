import pygame
import random
import math
from pygame import mixer

pygame.init() # Initialize PyGame to use all the tools

# Colors

white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
black = (0,0,0)
yellow = (255,255,0)
blue = (0,0,255)

# Window
window_width, window_height = 940, 705

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Space_N_Aliens")
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 27, bold=True)  # Choosing Font

def screen_text(txt, color, x,y):
    ''' Function to Display text on window '''
    render = font.render(txt,True,color)
    window.blit(render,(x,y))

def welcome_screen():
    ''' Function to Display Welcome Screen '''
    display = False
    fps = 30

    mixer.music.load('assets/background.wav')
    mixer.music.set_volume(0.5)
    mixer.music.play(-1)

    while not display:
        welcome_img = pygame.image.load('assets/welcome_bg.png').convert_alpha()
        window.fill(black)
        window.blit(welcome_img,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    instructions()

        pygame.display.update()
        clock.tick(fps)

def instructions():
    ''' Function to Display Instructions Screen '''
    display = False
    fps = 30

    mixer.music.load('assets/background.wav')
    mixer.music.set_volume(0.5)
    mixer.music.play(-1)

    while not display:
        welcome_img = pygame.image.load('assets/instructions.png').convert_alpha()
        window.fill(black)
        window.blit(welcome_img,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()

        pygame.display.update()
        clock.tick(fps)

# Game Loop
def game_loop():
    # Game Specific Variables
    exit_game = False
    game_over = False

    # Ship Positions and Movements
    ship_x = window_width/2
    ship_y = window_height/2
    ship_img = pygame.image.load('assets/spaceship.png')
    ship_size = 15
    velocity_x = 0
    velocity_y = 0
    speed_up_x = 0
    speed_up_y = 0

    # Scores
    score_list = [0] # To fetch maximum score
    bonus_score = 0
    score = 0

    # Alien Position
    alien_x = random.randint(25,window_width-100)
    alien_y = random.randint(90, window_height-100)
    alien_img = pygame.image.load('assets/alien.png')
    alien_size = 10

    # Background
    background = pygame.image.load('assets/bg.png').convert_alpha()

    # Background Music
    mixer.music.load('assets/background.wav')
    mixer.music.set_volume(0.5)
    mixer.music.play(-1)

    # Meteors
    meteor_img = []
    meteor_x = []
    meteor_y = []
    meteor_velocity_x = []
    meteor_velocity_y = []
    num_of_meteors = 1

    fps = 30

    def display_ship():
        ''' Display Ship '''
        window.blit(ship_img, (ship_x,ship_y))

    def display_alien():
        ''' Display Alien '''
        window.blit(alien_img, (alien_x, alien_y))

    def display_meteor(meteor_img,meteor_x,meteor_y):
        ''' Display Meteor '''
        window.blit(meteor_img, (meteor_x,meteor_y))

    def is_collision(x1,x2,y1,y2):
        ''' Fetch the distance between the meteor and ship.
            And Check for collision '''
        distance = math.sqrt(math.pow(x1 - x2,2)+math.pow(y1 - y2,2))
        if distance<45: # If the distance is less than 45 then collision happens
            return True
        return False

    def game_over_screen():
        ''' Function to Display Game Over Screen '''
        display = False
        fps = 30

        def game_over_font(txt,color,pos_x,pos_y):
            font = pygame.font.SysFont('skia',40,bold=True)
            render = font.render(txt,True,color)
            window.blit(render,(pos_x, pos_y))

        mixer.music.load('assets/gameover.mp3')
        mixer.music.play()

        while not display:
            game_over_img = pygame.image.load('assets/game_over.png').convert_alpha()
            window.fill(black)
            window.blit(game_over_img,(0,0))
            game_over_font(f'Your Score: {score}',green,(window_width/2-130),(window_height/2-80))
            game_over_font(f'High Score: {max(score_list)}',white,(window_width/2-130),(window_height/2-20))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    display = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_loop()

            pygame.display.update()
            clock.tick(fps)

    while not exit_game:
        # Check Game Over
        if game_over:
            game_over_screen()
            break
        else:
            # Handling events
            for event in pygame.event.get():  # Events such as clicking, mouse movement
                # print(event)
                if event.type == pygame.QUIT:  # Exit Game
                    exit_game = True

                if event.type == pygame.KEYDOWN:  # Key Presses
                    if event.key == pygame.K_UP or event.key == pygame.K_w:  # Game Controls (Arrow Keys or W,S,A,D)
                        velocity_y = -3.3 - (speed_up_y)

                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        velocity_y = 3.3 + speed_up_y

                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        velocity_x = 3.3 + speed_up_x

                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        velocity_x = -3.3 - (speed_up_x)

            ship_x+=velocity_x # Movement of Ship in x
            ship_y+=velocity_y # Movement of Ship in y

            if is_collision(ship_x,alien_x,ship_y,alien_y): # Consuming the power_ups and replotting power_ups
                score+=10
                score_list.append(score+bonus_score)
                alien_collect_sound = mixer.Sound('assets/collect.mp3')
                alien_collect_sound.play()
                alien_x = random.randint(25,window_width-60)
                alien_y = random.randint(90, window_height-80)

            elif score%100==0 and score!=0:
                score+=10
                bonus_score+=10
                speed_up_x+=1
                speed_up_y+=1
                num_of_meteors+=1

            elif ship_x<=0 or ship_x>=window_width-40 or ship_y<=45 or ship_y>=window_height-75: # Check for Boundries
                crash_sound = mixer.Sound('assets/crash.wav')
                crash_sound.play()
                game_over = True

            # Meteor Movements

            for i in range(num_of_meteors):
                meteor_img.append(pygame.image.load('assets/meteor.png'))
                meteor_x.append(random.randint(15,window_width-15))
                meteor_y.append(random.randint(80,85))
                meteor_velocity_x.append(random.randint(2,6))
                meteor_velocity_y.append(random.randint(2,6))

                if meteor_x[i]<=0:
                    meteor_velocity_x[i] = 3

                elif meteor_x[i]>=window_width-65:
                    meteor_velocity_x[i] = -3

                elif meteor_y[i]<=75:
                    meteor_velocity_y[i] = 3

                elif meteor_y[i]>=window_height-65:
                    meteor_velocity_y[i] = -3

                meteor_x[i]+=meteor_velocity_x[i]
                meteor_y[i]+=meteor_velocity_y[i]

                # Collision Check with Meteors
                collision = is_collision(meteor_x[i],ship_x,meteor_y[i],ship_y)

                if collision:
                    crash_sound = mixer.Sound('assets/crash.wav')
                    crash_sound.play()
                    game_over = True

            window.fill(black)  # Background Color
            window.blit(background, (0,0))  # Background Img
            pygame.draw.line(window,white,(0,70),(window_width,70))
            screen_text(f"Score:{score}",white,20,25)
            screen_text(f"Bonus:{bonus_score}",yellow,760,25)
            screen_text(f"Wave:{num_of_meteors}",red,400,25)
            display_ship() # Display Ship
            display_alien() # Display Alien

            for i in range(num_of_meteors):  # Displays Meteors after each wave
                display_meteor(meteor_img[i],meteor_x[i],meteor_y[i])

            pygame.display.update()  # To reflect Changes
            clock.tick(fps)  # To provide fps to window√

    pygame.quit()
    exit()

welcome_screen()
