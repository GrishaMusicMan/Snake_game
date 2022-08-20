import pygame

FRAME_COLOR = [0, 255, 204]

size = [400, 600]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Змейка")

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Выход')
            pygame.quit()

        screen.fill(FRAME_COLOR)
        pygame.display.flip()