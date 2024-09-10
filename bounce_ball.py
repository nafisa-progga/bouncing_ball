import pygame
import sys
import time

pygame.init()
pygame.font.init()

font = pygame.font.SysFont("Arial", 30)

width, height = 800, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball")

background = (0, 0, 0)

# Ball variables
ball_radius = 15
ball_x = width // 2
ball_y = height // 2
ball_x_speed = 4
ball_y_speed = 4

score = 0
missed = 0

# Rectangle variables
rectangle_width = 100
rectangle_height = 25
rectangle_velocity = 6

# Sound effects
pygame.mixer.init()
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.set_volume(0.5)

bounce_sound = pygame.mixer.Sound('bounce_sound.wav')
missed_ball_sound = pygame.mixer.Sound('missed_ball_sound.mp3')
game_over_sound = pygame.mixer.Sound('game_over_sound.wav')


def play_background_music():
    pygame.mixer.music.play(-1)

def play_bounce_sound():
    bounce_sound.play()
    
def play_missed_ball_sound():
    missed_ball_sound.play()

def play_game_over_sound():
    game_over_sound.play()

def show_text(elapsed_time):
    time_text = font.render(f"Time: {round(elapsed_time)}s", 1,"white" )
    screen.blit(time_text, (10,10))
    
    missed_text = font.render(f"Missed: {missed}", 1, "white")
    screen.blit(missed_text, (10, 40))
    
def draw_rectangle(rectangle):
    pygame.draw.rect(screen, "brown", rectangle)
    pygame.display.update()

def draw_ball(x, y, radius):
    pygame.draw.circle(screen, "green", (x, y), radius)
    pygame.display.update()

def reset_ball():
    global ball_x, ball_y, ball_y_speed
    ball_x = width // 2
    ball_y = height // 2
    ball_y_speed = 3

def main():
    global ball_x, ball_y, ball_x_speed, ball_y_speed, score, missed

    run = True
    rectangle = pygame.Rect(200, height - rectangle_height, rectangle_width, rectangle_height)
    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    ball_count = 0
    over = False

    play_background_music()

    while run:
        #play_background_music()
        clock.tick(60)
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and rectangle.x >= 0:
            rectangle.x -= rectangle_velocity
        if keys[pygame.K_RIGHT] and rectangle.x + rectangle_velocity + rectangle.width <= width:
            rectangle.x += rectangle_velocity

        # Update ball position
        ball_y += ball_y_speed

        # Bounce off the walls
        if ball_x - ball_radius <= 0 or ball_x + ball_radius >= width:
            ball_x_speed = -ball_x_speed
            #play_bounce_sound()

        # Bounce off the top
        if ball_y - ball_radius <= 0:
            ball_y_speed = -ball_y_speed
            #play_bounce_sound()

        # Ball collides with the paddle & score count
        if ball_y + ball_radius >= rectangle.y and rectangle.colliderect(pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, 2 * ball_radius, 2 * ball_radius)):
            score += 1
            ball_y_speed = -ball_y_speed
            ball_x_speed = -ball_x_speed
            play_bounce_sound()
            
        elif ball_x + ball_radius >= rectangle.x and rectangle.colliderect(pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, 2 * ball_radius, 2 * ball_radius)):
            score += 1
            ball_y_speed = -ball_y_speed
            ball_x_speed = -ball_x_speed
            play_bounce_sound()
            
        elif ball_x - ball_radius >= rectangle.x + rectangle_width and rectangle.colliderect(pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, 2 * ball_radius, 2 * ball_radius)):
            score += 1
            ball_y_speed = -ball_y_speed
            ball_x_speed = -ball_x_speed
            play_bounce_sound()
            

        # Ball falls
        if ball_y + ball_radius >= height:
            missed += 1
            play_missed_ball_sound()
            if missed == 3:
                over = True
                play_game_over_sound()
                break
            else:
                pygame.time.delay(1000)
                reset_ball()
        


        # Clear the screen
        screen.fill(background)

        # Draw the rectangle and the ball
        show_text(elapsed_time)
        draw_rectangle(rectangle)
        draw_ball(ball_x, ball_y, ball_radius)

        pygame.display.update()
        
    screen.fill(background)    
    show_text(elapsed_time)
    pygame.display.update()
    
    if over:
        pygame.display.update()
        lost_text = font.render("GAME OVER!!!", 5, "white")
        screen.blit(lost_text, (width / 2 - lost_text.get_width() / 2, height / 2 - lost_text.get_height() / 2))

        score_text = font.render(f"Your score is: {score}", 5, "white")
        screen.blit(score_text, (width / 2 - score_text.get_width() / 2, height / 1.78 - score_text.get_height() / 2))

        pygame.display.update()
        pygame.time.delay(4000)
    
    pygame.quit()

if __name__ == "__main__":
    main()
