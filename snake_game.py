"""
Snake Eater
Made with Pygame
"""

import sys, time, random
import pygame as py

# Difficulty settings
# Easy      -> 10
# Medium    -> 25
# Hard      -> 40
# Harder    -> 60
# Impossible-> 120
difficulty = 25

# Window size
frame_size_x = 720
frame_size_y = 480


# Checks for errors encoutered
check_errors = py.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Initialise game window
py.display.set_caption('Snake Eater')
game_window = py.display.set_mode((frame_size_x, frame_size_y))


# Colors (R, G, B)
black = py.Color(0, 0, 0)
white = py.Color(255, 255, 255)
red = py.Color(255, 0, 0)
green = py.Color(0, 255, 0)
blue = py.Color(0, 0, 255)

# FPS (frames per second) controller
fps_controller = py.time.Clock()

# Game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-20, 50]]

food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0


# Game Over
def game_over():
    my_font = py.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    py.display.flip()
    time.sleep(3)
    py.quit()
    sys.exit()


# Score
def show_score(choice, color, font, size):
    score_font = py.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()


# Main logic
while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == py.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == py.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == py.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == py.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == py.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            # Esc -> Create event to quit the game
            if event.key == py.K_ESCAPE:
                py.event.post(py.event.Event(py.QUIT))
    
    # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
    
    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10
    
    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Spawning food on the screen
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True

    # GFX
    game_window.fill(black)
    for pos in snake_body:
        # Snake body
        # .draw.rect(play_superface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        py.draw.rect(game_window, green, py.Rect(pos[0], pos[1], 10, 10))
    

    # Snake food
    py.draw.rect(game_window, white, py.Rect(food_pos[0], food_pos[1], 10, 10))

    # Game Over conditions
    # Getting out of bounds
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        game_over()
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()
    
    show_score(1, white, 'consolas', 20)
    # Refresh game screen
    py.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)