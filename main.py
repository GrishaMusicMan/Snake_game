import pygame
import sys
import random
import pygame_menu

pygame.init()
bg_image = pygame.image.load("snake_cover.gif")
SIZE_BLOCK = 20
COUNT_BLOCKS = 20
FRAME_COLOR = (0, 255, 204)
HEADER_COLOR = (0, 204, 153)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (204, 255, 255)
SNAKE_COLOR = (0, 102, 0)
MARGIN = 1
HEADER_MARGIN = 70

size = [SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS + HEADER_MARGIN]

print(size)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Змейка")
timer = pygame.time.Clock()
courier = pygame.font.SysFont('courier', 36)


class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_down(self):
        return 0 <= self.x

    def is_up(self):
        return self.x < SIZE_BLOCK

    def is_right(self):
        return self.y < SIZE_BLOCK

    def is_left(self):
        return 0 <= self.y

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def start_the_game():
    def get_random_empty_block():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
            empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return empty_block

    snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
    apple = get_random_empty_block()
    d_row = buf_row = 0
    d_col = buf_col = 1
    total = 0
    speed = 1

    def draw_block(color, row, column):
        pygame.draw.rect(screen, color, [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                                         HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1),
                                         SIZE_BLOCK,
                                         SIZE_BLOCK])

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Выход')
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    d_row = -1
                    d_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    d_row = 1
                    d_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    d_row = 0
                    d_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    d_row = 0
                    d_col = 1

        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

        text_total = courier.render(f'Total {total}', 0, WHITE)
        text_speed = courier.render(f'Speed {speed}', 0, WHITE)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK + 200, SIZE_BLOCK))

        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (row * column) % 2 == 0:
                    color = WHITE
                else:
                    color = BLUE

                draw_block(color, row, column)
        draw_block(RED, apple.x, apple.y)

        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        head = snake_blocks[-1]

        # d_row = buf_row
        # d_col = buf_col
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)

        if head == apple:
            total += 1
            speed = total // 5 + 1
            snake_blocks.append(apple)
            apple = get_random_empty_block()

        if not new_head.is_right():
            new_head.y = 0

        elif not new_head.is_left():
            new_head.y = COUNT_BLOCKS - 1

        elif not new_head.is_down():
            new_head.x = COUNT_BLOCKS - 1

        elif not new_head.is_up():
            new_head.x = 0

        if new_head in snake_blocks:
            print('crash yourself')
            break

        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        pygame.display.flip()
        timer.tick(3 + speed)


main_theme = pygame_menu.themes.THEME_BLUE.copy()
main_theme.set_background_color_opacity(0.4)
menu = pygame_menu.Menu('', 250, 250, False,
                        theme=main_theme)

menu.add.text_input('Name :', default='Grisha')
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

while True:

    screen.blit(bg_image, (0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()
