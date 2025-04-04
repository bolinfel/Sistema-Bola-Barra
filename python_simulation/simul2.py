import pygame

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Rectangle")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Rectangle properties
rect_width, rect_height = 350, 20
rect_x, rect_y = (WIDTH / 2) - (rect_width/2), HEIGHT/2 - (rect_height/2) # postion in center

# Main loop
running = True
while running:
    screen.fill(WHITE)  # Fill the screen with white background
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Draw rectangle
    pygame.draw.rect(screen, BLUE, (rect_x, rect_y, rect_width, rect_height))
    
    # Update display
    pygame.display.flip()

# Quit pygame
pygame.quit()
