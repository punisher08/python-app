import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock
FPS = 60
CLOCK = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
SKY = (135, 206, 235)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)

# Fonts
FONT = pygame.font.SysFont("Arial", 30)

# Bird
BIRD_WIDTH = BIRD_HEIGHT = 30
bird = pygame.Rect(100, HEIGHT // 2, BIRD_WIDTH, BIRD_HEIGHT)
bird_movement = 0
gravity = 0.5
jump = -10

# Pipes
pipe_width = 60
pipe_gap = 250
pipe_speed = 3
pipes = []

# Score
score = 0
game_over = False

def create_pipe():
    top_height = random.randint(100, 400)
    bottom_height = HEIGHT - top_height - pipe_gap
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, top_height)
    bottom_pipe = pygame.Rect(WIDTH, top_height + pipe_gap, pipe_width, bottom_height)
    return top_pipe, bottom_pipe

def reset_game():
    global bird, bird_movement, pipes, score, game_over
    bird = pygame.Rect(100, HEIGHT // 2, BIRD_WIDTH, BIRD_HEIGHT)
    bird_movement = 0
    pipes = []
    score = 0
    game_over = False

# Game loop
while True:
    CLOCK.tick(FPS)
    SCREEN.fill(SKY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Flap on SPACE
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_movement = jump
            if event.key == pygame.K_r and game_over:
                reset_game()

    if not game_over:
        # Apply gravity
        bird_movement += gravity
        bird.y += int(bird_movement)

        # Add new pipes
        if not pipes or pipes[-1][0].x < WIDTH - 200:
            pipes.append(create_pipe())

        # Move and draw pipes
        for top, bottom in pipes:
            top.x -= pipe_speed
            bottom.x -= pipe_speed
            pygame.draw.rect(SCREEN, GREEN, top)
            pygame.draw.rect(SCREEN, GREEN, bottom)

        # Remove old pipes
        pipes = [pair for pair in pipes if pair[0].x + pipe_width > 0]

        # Check for collisions
        for top, bottom in pipes:
            if bird.colliderect(top) or bird.colliderect(bottom):
                game_over = True
        if bird.top <= 0 or bird.bottom >= HEIGHT:
            game_over = True

        # Increase score
        for top, _ in pipes:
            if top.x + pipe_width == bird.x:
                score += 1

    # Draw bird
    pygame.draw.ellipse(SCREEN, YELLOW, bird)

    # Draw score or restart message
    if game_over:
        text = FONT.render("Game Over! Press R to Restart", True, WHITE)
        SCREEN.blit(text, (40, HEIGHT // 2 - 20))
    else:
        text = FONT.render(f"Score: {score}", True, WHITE)
        SCREEN.blit(text, (10, 10))

    pygame.display.update()
