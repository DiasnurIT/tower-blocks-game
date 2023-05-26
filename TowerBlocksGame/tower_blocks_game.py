import pygame
import random

# Инициализация Pygame
pygame.init()

# Размеры окна
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Blocks")

# Загрузка фонового изображения
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Загрузка звуков
fall_sound = pygame.mixer.Sound("fall.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")

# Класс блока
class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 1

# Группа спрайтов блоков
blocks_group = pygame.sprite.Group()

# Создание игровых объектов
def create_block():
    width = random.randint(50, 100)
    height = 20
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    block = Block(color, width, height)
    block.rect.x = random.randint(0, SCREEN_WIDTH - width)
    block.rect.y = -height
    blocks_group.add(block)

# Создание первого блока
create_block()

# Количество упавших блоков
fallen_blocks = 0

# Рекорд
high_score = 0

# Загрузка рекорда из файла
def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Сохранение рекорда в файл
def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

# Уровень сложности
difficulty = 1
fall_speeds = [1, 2, 3, 4, 5]

# Очки
score = 0

# Функция обновления очков
def update_score(value):
    global score
    score += value

# Отображение текста на экране
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Функция окончания игры
def game_over():
    global high_score
    pygame.mixer.Sound.play(game_over_sound)
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))
        draw_text("Game Over", pygame.font.Font(None, 48), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        draw_text("Score: " + str(score), pygame.font.Font(None, 36), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("High Score: " + str(high_score), pygame.font.Font(None, 36), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        draw_text("Press SPACE to play again", pygame.font.Font(None, 24), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        pygame.display.update()

# Основной игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                create_block()

    screen.blit(background_image, (0, 0))

    # Обновление и отрисовка блоков
    blocks_group.update()
    blocks_group.draw(screen)

    # Проверка коллизии блоков
    for block in blocks_group:
        if block.rect.colliderect(block.rect.move(0, 1)):
            block.rect.y = (block.rect.y // 20) * 20
            fallen_blocks += 1
            pygame.mixer.Sound.play(fall_sound)

            if fallen_blocks == 3:
                game_over()

    # Отрисовка количества упавших блоков и рекорда
    draw_text("Fallen Blocks: " + str(fallen_blocks), pygame.font.Font(None, 24), WHITE, 100, 20)
    draw_text("High Score: " + str(high_score), pygame.font.Font(None, 24), WHITE, SCREEN_WIDTH - 100, 20)

    # Отрисовка текущего счета
    draw_text("Score: " + str(score), pygame.font.Font(None, 24), WHITE, SCREEN_WIDTH // 2, 20)

    # Обновление уровня сложности
    if score // 10 >= difficulty and difficulty < 5:
        difficulty += 1

    # Обновление скорости падения блоков в зависимости от уровня сложности
    for block in blocks_group:
        block.rect.y += fall_speeds[difficulty - 1]

    # Удаление блоков, которые вышли за пределы экрана
    blocks_group.remove([block for block in blocks_group if block.rect.y > SCREEN_HEIGHT])

    # Проверка на коллизию блока с предыдущими блоками
    collision_blocks = pygame.sprite.spritecollide(blocks_group.sprites()[-1], blocks_group, False)
    if len(collision_blocks) > 1:
        game_over()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
