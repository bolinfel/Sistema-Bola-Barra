import pygame
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 20
PLATFORM_WIDTH = 300
PLATFORM_HEIGHT = 10
GRAVITY = 0.5
FRICTION = 0.99  # Rolling friction

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Rolling on Rotating Platform")

# Font for displaying values
font = pygame.font.Font(None, 36)

# Ball properties
ball_x = WIDTH // 2
ball_y = HEIGHT // 2 - 100
ball_speed_x = 0
ball_speed_y = 0

# Platform properties
platform_x = WIDTH // 2
platform_y = HEIGHT // 2
platform_angle = 0  # Degrees
angle_speed = 2

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Platform control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        platform_angle += angle_speed
    if keys[pygame.K_RIGHT]:
        platform_angle -= angle_speed
    platform_angle = max(-30, min(30, platform_angle))  # Limit angle

    # Convert angle to radians
    rad_angle = math.radians(platform_angle)
    
    # Simulate ball physics
    acceleration = GRAVITY * math.sin(rad_angle)
    ball_speed_x += acceleration
    ball_speed_x *= FRICTION  # Apply friction
    ball_x += ball_speed_x
    
    # Keep ball on rotated platform
    left_limit = platform_x - PLATFORM_WIDTH // 2 + BALL_RADIUS
    right_limit = platform_x + PLATFORM_WIDTH // 2 - BALL_RADIUS
    ball_x = max(left_limit, min(right_limit, ball_x))
    
    # Calculate rotated ball position
    ball_relative_x = ball_x - platform_x
    ball_relative_y = -BALL_RADIUS  # Ball is above the platform
    rotated_ball_x = platform_x + ball_relative_x * math.cos(rad_angle) - ball_relative_y * math.sin(rad_angle)
    rotated_ball_y = platform_y + ball_relative_x * math.sin(rad_angle) + ball_relative_y * math.cos(rad_angle)
    
    # Draw rotated platform
    platform_surface = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT), pygame.SRCALPHA)
    platform_surface.fill(BLUE)
    rotated_surface = pygame.transform.rotate(platform_surface, platform_angle)
    rotated_rect = rotated_surface.get_rect(center=(platform_x, platform_y))
    screen.blit(rotated_surface, rotated_rect.topleft)
    
    # Draw ball
    pygame.draw.circle(screen, RED, (int(rotated_ball_x), int(rotated_ball_y)), BALL_RADIUS)
    
    # Display values
    text_speed = font.render(f"Speed: {ball_speed_x:.2f}", True, BLACK)
    text_angle = font.render(f"Angle: {platform_angle}°", True, BLACK)
    text_position = font.render(f"Position: {ball_x - platform_x:.2f}", True, BLACK)
    
    screen.blit(text_speed, (10, 10))
    screen.blit(text_angle, (10, 40))
    screen.blit(text_position, (10, 70))
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()