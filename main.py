import pygame
import random
import os

NUM_BOMBS = 2

pygame.init()

pygame.display.set_caption("Shawn's pygame")
clock = pygame.time.Clock()
imgPath = os.path.join(os.path.dirname(__file__), "img")
stageNum = 1

def isBomb(item_index):
    return True if item_index < NUM_BOMBS else False

def runGame(bg):
    global stageNum

    background = pygame.image.load(os.path.join(imgPath, f"{bg}.png"))
    screen_width = background.get_width()
    screen_height = background.get_height()
    screen = pygame.display.set_mode((screen_width, screen_height))

    characters = {'left': [
        pygame.image.load(os.path.join(imgPath, "molang-0.png")),
        pygame.image.load(os.path.join(imgPath, "molang-1.png")),
        pygame.image.load(os.path.join(imgPath, "molang-0.png")),
        pygame.image.load(os.path.join(imgPath, "molang-2.png"))
        ]}
    characters['right'] = [ pygame.transform.flip(char, True, False) for char in characters["left"]]
    character_dead = pygame.image.load(os.path.join(imgPath, "molang-tot.png"))
    charactor_index = 0
    character = characters["left"][charactor_index]
    character_size = character.get_rect().size
    character_width = character_size[0]
    character_height = character_size[1]
    character_x_pos = (screen_width - character_width) / 2
    character_y_pos = screen_height - character_height
    character_speed = 1 + (0.1 * stageNum)
    character_jump = -3
    to_x = 0
    to_y = 0

    itemdir = os.path.join(imgPath, "item")
    itemfiles = os.listdir(itemdir)
    items = []
    for filename in itemfiles:
        items.append(pygame.image.load(os.path.join(itemdir, filename)))
    item_index = random.randint(0, len(items) - 1)
    item = items[item_index]
    item_size = item.get_rect().size
    item_width = item_size[0]
    item_height = item_size[1]
    item_x_pos = random.randint(0, screen_width - item_width)
    item_y_pos = 0
    item_speed = 1 + (0.5 * stageNum)

    normal_font = pygame.font.Font(None, 40)
    gameover_font = pygame.font.Font(None, 80)

    stage_time = 10
    start_ticks = pygame.time.get_ticks()

    running = True
    isLeft = True
    isDead = False
    tick = 0
    isMoving = False

    while running:
        dt = clock.tick(240)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                isMoving = True
                if event.key == pygame.K_LEFT:
                    to_x -= character_speed
                    if not isLeft:
                        isLeft = True
                if event.key == pygame.K_RIGHT:
                    to_x += character_speed
                    if isLeft:
                        isLeft = False
                if event.key == pygame.K_SPACE:
                    to_y = character_jump
                if event.key == pygame.K_ESCAPE:
                    running = False
                    stageNum = -1
            if event.type == pygame.KEYUP:
                isMoving = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    to_x = 0
            if event.type == pygame.QUIT:
                running = False
                stageNum = -1

        if isMoving:
            tick = (tick + 1) % (4 * 10)
            charactor_index = int(tick / 10)
        to_y += 0.05
        character_x_pos += to_x * dt
        character_y_pos += to_y * dt
        item_y_pos += item_speed
        
        if character_x_pos < 0:
            character_x_pos = 0
        elif character_x_pos > screen_width - character_width:
            character_x_pos = screen_width - character_width
        if character_y_pos < 0:
            character_y_pos = 0
        elif character_y_pos > screen_height - character_height:
            character_y_pos = screen_height - character_height

        character_rect = character.get_rect()
        character_rect.left = character_x_pos + (character_width / 2)
        character_rect.top = character_y_pos + (character_height / 2)
        item_rect = item.get_rect()
        item_rect.left = item_x_pos + (item_width / 2)
        item_rect.top = item_y_pos + (item_height / 2)
        if character_rect.colliderect(item_rect):
            if not isBomb(item_index):
                item_y_pos = 0
                item_x_pos = random.randint(0, screen_width - item_width)
                item_index = random.randint(0, len(items) - 1)
                item = items[item_index]
            else:
                isDead = True
        if item_y_pos > screen_height - item_height:
            if not isBomb(item_index):
                print("Failed :(")
                isDead = True
            else:
                item_y_pos = 0
                item_x_pos = random.randint(0, screen_width - item_width)
                item_index = random.randint(0, len(items) - 1)
                item = items[item_index]

        screen.blit(background, (0, 0))
        screen.blit(item, (item_x_pos, item_y_pos))

        game_time = stage_time - (pygame.time.get_ticks() - start_ticks) / 1000
        timeText = normal_font.render(str(int(game_time)), True, (255, 255, 255))
        screen.blit(timeText, (10, 10))
        
        stageText = normal_font.render(f"STAGE {stageNum}" if stageNum > 0 else "GAME OVER", True, (0, 0, 255))
        screen.blit(stageText, (screen_width - 180, 10))
        
        character = characters["left"][charactor_index] if isLeft else characters["right"][charactor_index]
        screen.blit(character if not isDead else character_dead, (character_x_pos, character_y_pos))
        if isDead:
            screen.blit(gameover_font.render("G A M E  O V E R", True, (255, 0, 0)), (screen_width / 2 - 100, screen_height / 2 - 40))
            running = False
            stageNum = -1
        if game_time <= 0:
            screen.blit(gameover_font.render(f"STAGE {stageNum} P A S S", True, (0, 255, 0)), (screen_width / 2 - 120, screen_height / 2 - 40))
            running = False
        pygame.display.update()

while stageNum > 0:
    bambooland = "bambooland" + str(random.randint(0, 1))
    runGame(bambooland)
    pygame.time.delay(1000)
    stageNum += 1

pygame.quit()