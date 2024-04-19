import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.25
FLAP_FORCE = -6
PIPE_WIDTH = 50
PIPE_GAP = 150
PIPE_SPEED = 3
BIRD_SIZE = 30
BIRD_COLOR = (255, 255, 0)
BACKGROUND_COLOR = (0, 0, 0)
FONT_SIZE = 36
SCORE_POSITION = (10, 10)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Fonts
font = pygame.font.Font(None, FONT_SIZE)

# Clock
clock = pygame.time.Clock()

# Player bird
bird_rect = pygame.Rect(WIDTH // 2 - BIRD_SIZE // 2, HEIGHT // 2 - BIRD_SIZE // 2, BIRD_SIZE, BIRD_SIZE)
bird_velocity = 0

# Pipes
pipes = []

# Score
score = 0

# Function to create a new pipe pair
def create_pipe_pair():
    gap_y = random.randint(PIPE_GAP, HEIGHT - PIPE_GAP)
    top_pipe = pygame.Rect(WIDTH, 0, PIPE_WIDTH, gap_y)
    bottom_pipe = pygame.Rect(WIDTH, gap_y + PIPE_GAP, PIPE_WIDTH, HEIGHT - gap_y - PIPE_GAP)
    pipes.append((top_pipe, bottom_pipe))

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = FLAP_FORCE

    # Move the bird
    bird_velocity += GRAVITY
    bird_rect.y += bird_velocity

    # Generate new pipes
    if len(pipes) == 0 or pipes[-1][0].x < WIDTH - 200:
        create_pipe_pair()

    # Move and draw pipes
    for top_pipe, bottom_pipe in pipes:
        top_pipe.x -= PIPE_SPEED
        bottom_pipe.x -= PIPE_SPEED
        pygame.draw.rect(screen, (0, 255, 0), top_pipe)
        pygame.draw.rect(screen, (0, 255, 0), bottom_pipe)

        # Check for collisions with pipes
        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
            running = False

        # Increase score if bird passes through the gap
        if top_pipe.x + PIPE_WIDTH == bird_rect.x:
            score += 1

    # Remove pipes that have gone off the screen
    pipes = [(top_pipe, bottom_pipe) for top_pipe, bottom_pipe in pipes if top_pipe.x > -PIPE_WIDTH]

    # Check for collisions with the top and bottom of the screen
    if bird_rect.y < 0 or bird_rect.y > HEIGHT - BIRD_SIZE:
        running = False

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw the bird
    pygame.draw.rect(screen, BIRD_COLOR, bird_rect)

    # Display score
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, SCORE_POSITION)

    # Update the display
    pygame.display.flip()

    # Limit frames per second
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
