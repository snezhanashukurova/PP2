import pygame
import sys
import random
import pygame_menu
import psycopg2

# Database connection
def connect_to_db():
    return psycopg2.connect(
        host="localhost",
        dbname="snake",
        user="postgres",
        password="12345678"
    )

# Pygame setup
pygame.init()
background = pygame.image.load('snake.png')

SIZE_BLOCK = 20
WHITE = (255, 255, 255)
FRAME_COLOR = (0, 255, 204)
HEADER_COLOR = (0, 204, 153)
SNAKE_COLOR = (0, 102, 0)
COUNT_BLOCKS = 20
BLUE = (204, 255, 255)
RED = (224, 0, 0)
MARGIN = 1
HEADER_MARGIN = 70

size = [SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS + HEADER_MARGIN]
screen = pygame.display.set_mode(size)
timer = pygame.time.Clock()
courier = pygame.font.SysFont('courier', 36, 1)

player_name = ""
player_score = 0
player_level = 1

class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def is_inside(self): 
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS
    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y

def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column),
                                     HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row),
                                     SIZE_BLOCK, SIZE_BLOCK])

def load_user(name):
    global player_score, player_level
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT score, level FROM snake WHERE username = %s", (name,))
    result = cur.fetchone()
    if result:
        player_score, player_level = result
    else:
        cur.execute("INSERT INTO snake (username) VALUES (%s)", (name,))
        conn.commit()
    cur.close()
    conn.close()

def save_user(name, score, level):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO snake (username, score, level)
        VALUES (%s, %s, %s)
        ON CONFLICT (username) DO UPDATE
        SET score = EXCLUDED.score, level = EXCLUDED.level
    """, (name, score, level))
    conn.commit()
    cur.close()
    conn.close()

def get_random_empty_block(snake_blocks):
    while True:
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        block = SnakeBlock(x, y)
        if block not in snake_blocks:
            return block

def start_the_game():
    global player_name, player_score, player_level
    snake_blocks = [SnakeBlock(9, 9), SnakeBlock(9, 10), SnakeBlock(9, 11)]
    apple = get_random_empty_block(snake_blocks)

    d_row = 0
    d_col = 1
    total = player_score
    speed = player_level

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_user(player_name, total, speed)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    d_row = -1
                    d_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    d_row = 1
                    d_col = 0
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    d_row = 0
                    d_col = 1
                elif event.key == pygame.K_LEFT and d_row != 0:
                    d_row = 0
                    d_col = -1
                elif event.key == pygame.K_p:
                    save_user(player_name, total, speed)
                    return

        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

        text_total = courier.render(f"Total: {total}", 1, WHITE)
        text_speed = courier.render(f"Speed: {speed}", 1, WHITE)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK + 230, SIZE_BLOCK))

        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                color = BLUE if (row + column) % 2 == 0 else WHITE
                draw_block(color, row, column)

        head = snake_blocks[-1]
        if not head.is_inside() or head in snake_blocks[:-1]:
            save_user(player_name, total, speed)
            break

        draw_block(RED, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        if apple == head:
            total += 1
            speed = total // 3 + 1
            snake_blocks.append(apple)
            apple = get_random_empty_block(snake_blocks)
        else:
            snake_blocks.pop(0)

        new_head = SnakeBlock(head.x + d_row, head.y + d_col)
        snake_blocks.append(new_head)

        pygame.display.flip()
        timer.tick(3 + speed)

def set_name(value):
    global player_name
    player_name = value

menu = pygame_menu.Menu('Snake', 400, 300, theme=pygame_menu.themes.THEME_GREEN.set_background_color_opacity(1))
menu.add.text_input('Name :', default='Player 1', onchange=set_name)
menu.add.button('Play', lambda: [load_user(player_name), start_the_game()])  # Start game after loading user
menu.add.button('Quit', pygame_menu.events.EXIT)

if __name__ == "__main__":
    while True:
        screen.blit(background, (0, 0))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen)

        pygame.display.update()
