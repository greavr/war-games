import pygame

from code.settings import SettingsSet

def MainLoop(CurrentSettings: SettingsSet = SettingsSet()):
    # Initialize Pygame
    pygame.init()

    # Set screen dimensions
    screen_width = CurrentSettings.Resolution[0]
    screen_height = CurrentSettings.Resolution[1]
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Set Game FPS
    clock = pygame.time.Clock()
    dt = 0

    # Set window title
    pygame.display.set_caption(CurrentSettings.GameTitle)

    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game logic (update game state)
        # ...

        # Clear the screen
        screen.fill((0, 0, 0))  # Black background

        # Drawing code
        # ...

        # Update the display
        pygame.display.flip()

        # Limit to FPS
        dt = clock.tick(CurrentSettings.FPS) / 1000

    # Quit Pygame
    pygame.quit()

if __name__ == '__main__':
    """  Main Entry  """
    