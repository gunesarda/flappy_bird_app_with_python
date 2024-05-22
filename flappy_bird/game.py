import pygame
import random

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

BIRD_WIDTH = 80
BIRD_HEIGHT = 80

GAP = 200

BIRD_SPEED = 5

PIPE_SPEED = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

bird_img = pygame.image.load('kus.png')
bird_img = pygame.transform.scale(bird_img, (BIRD_WIDTH, BIRD_HEIGHT))

pipe_img = pygame.image.load('pipe.png')
PIPE_WIDTH = 100
PIPE_HEIGHT = 400
pipe_img = pygame.transform.scale(pipe_img, (PIPE_WIDTH, PIPE_HEIGHT))

clock = pygame.time.Clock()

class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.25
        self.lift = -8

    def show(self):
        screen.blit(bird_img, (self.x, self.y))

    def update(self):
        self.velocity += self.gravity
        self.velocity *= 0.9
        self.y += self.velocity

        if self.y > SCREEN_HEIGHT - BIRD_HEIGHT:
            return True
        if self.y < 0:
            return True
        return False

    def up(self):
        self.velocity += self.lift

class Pipe:
    def __init__(self):
        self.gap_y = random.randint(50, SCREEN_HEIGHT - GAP - 50)
        self.top_pipe = pygame.transform.flip(pipe_img, False, True)
        self.bottom_pipe = pipe_img
        self.x = SCREEN_WIDTH+100
        self.width = PIPE_WIDTH
        self.speed = PIPE_SPEED

    def show(self):
        top_pipe_y = self.gap_y - self.top_pipe.get_height()
        screen.blit(self.top_pipe, (self.x, top_pipe_y))
        screen.blit(self.bottom_pipe, (self.x, self.gap_y + GAP))

    def update(self):
        self.x -= self.speed

    def offscreen(self):
        return self.x < -self.width

def draw():
    screen.fill(WHITE)
    for pipe in pipes:
        pipe.show()
    bird.show()
    show_score()  
    pygame.display.update()

def show_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render("Skor: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

def update():
    global score
    if bird.update():
        return True
    for pipe in pipes:
        pipe.update()
        if pipe.offscreen():
            pipes.remove(pipe)
            score += 1  
        if bird.x + BIRD_WIDTH > pipe.x and bird.x < pipe.x + pipe.width:
            if bird.y < pipe.gap_y or bird.y + BIRD_HEIGHT > pipe.gap_y + GAP:
                return True
    return False

def run_game():
    global pipes, bird, score  
    bird = Bird()
    pipes = [Pipe()]
    score = 0  
    running = True
    game_over = False
    font = pygame.font.Font(None, 36)
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_over:
                        bird.up()
                    else:
                        bird = Bird()
                        pipes = [Pipe()]
                        score = 0  
                        game_over = False

        if not game_over:
            if pipes[-1].x < SCREEN_WIDTH - 200:
                pipes.append(Pipe())

            draw()
            if update():
                game_over_text = font.render("Kaybettin!", True, BLACK)
                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))
                restart_text = font.render("Yeniden Oyna (SPACE)", True, BLACK)
                screen.blit(restart_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 40))
                pygame.display.update()
                game_over = True

    pygame.quit()

if __name__ == "__main__":
    run_game()