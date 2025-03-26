import pgzrun
import random

# Игровое окно
cell = Actor('border')
cell1 = Actor('floor')
cell2 = Actor("crack")
cell3 = Actor("bones")

size_w = 9  # Ширина поля в клетках
size_h = 10  # Высота поля в клетках
WIDTH = cell.width * size_w
HEIGHT = cell.height * size_h

defeat = Actor('defeat')
win_fon = Actor('win')

win = 0
mode = "level_1"
modes_game = ['level_1', 'level_2', 'level_3', 'level_4', 'level_5']
colli = 0

TITLE = "WeCode и Драконы"  # Заголовок окна игры
FPS = 30  # Количество кадров в секунду
my_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 1, 1, 1, 1, 1, 1, 1, 0],
          [0, 1, 1, 2, 1, 3, 1, 1, 0],
          [0, 1, 1, 1, 2, 1, 1, 1, 0],
          [0, 1, 3, 2, 1, 1, 3, 1, 0],
          [0, 1, 1, 1, 1, 3, 1, 1, 0],
          [0, 1, 1, 3, 1, 1, 2, 1, 0],
          [0, 1, 1, 1, 1, 1, 1, 1, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [-1, -1, -1, -1, -1, -1, -1, -1, -1]]  # Строка с атакой и здоровьем


# Главный герой
def new_char():
    global char
    char = Actor('stand')
    char.top = cell.height
    char.left = cell.width
    char.health = 100
    char.attack = 5


new_char()

# Генерация врагов
enemies = []


# Списки здоровья и координат

# Health и attack воспринимают кортежи с начальным и максимальным значением
def new_enemies(value, health, attack):
    poses = []
    for i in range(value):
        while True:
            x = random.randint(1, 7) * cell.width
            y = random.randint(1, 7) * cell.height
            pos = (x, y)
            if pos not in poses:
                poses.append(pos)
                break
            else:
                poses.remove(pos)
        enemy = Actor("enemy", topleft=(x, y))
        enemy.health = random.randint(health[0], health[1])
        enemy.attack = random.randint(attack[0], attack[1])
        enemy.bonus = random.randint(0, 2)
        enemies.append(enemy)


new_enemies(5, (15, 20), (5, 5))

# Бонусы
hearts = []
swords = []


# Отрисовка карты
def map_draw():
    for i in range(len(my_map)):
        for j in range(len(my_map[0])):
            if my_map[i][j] == 0:
                cell.left = cell.width * j
                cell.top = cell.height * i
                cell.draw()
            elif my_map[i][j] == 1:
                cell1.left = cell.width * j
                cell1.top = cell.height * i
                cell1.draw()
            elif my_map[i][j] == 2:
                cell2.left = cell.width * j
                cell2.top = cell.height * i
                cell2.draw()
            elif my_map[i][j] == 3:
                cell3.left = cell.width * j
                cell3.top = cell.height * i
                cell3.draw()

            # Отрисовка


def draw():
    if mode in modes_game:
        screen.fill("#2f3542")
        map_draw()
        char.draw()
        screen.draw.text("HP:", center=(25, 475), color='white', fontsize=20)
        screen.draw.text(str(char.health), center=(75, 475), color='white', fontsize=20)
        screen.draw.text("AP:", center=(375, 475), color='white', fontsize=20)
        screen.draw.text(str(char.attack), center=(425, 475), color='white', fontsize=20)
        for i in range(len(enemies)):
            enemies[i].draw()
            # Отрисовка здоровья врага
            screen.draw.text(str(enemies[i].health), topleft=(enemies[i].x + 5, enemies[i].y - 30), color='white',
                             fontsize=18)
        # отрисовка бонусов
        for i in range(len(hearts)):
            hearts[i].draw()
        for i in range(len(swords)):
            swords[i].draw()
    # Окно победы или поражения
    elif mode == "win":
        screen.fill("white")
        win_fon.draw()
    elif mode == 'defeat':
        screen.fill('white')
        defeat.draw()


# Управление
def on_key_down(key):
    global colli, enemies, hearts, swords, mode, win
    old_x = char.x
    old_y = char.y
    if key == keys.D and char.x + cell.width < WIDTH - cell.width:
        char.x += cell.width
        char.image = 'stand'
    elif key == keys.A and char.x - cell.width > cell.width:
        char.x -= cell.width
        char.image = 'left'
    elif key == keys.S and char.y + cell.height < HEIGHT - cell.height * 2:
        char.y += cell.height
    elif key == keys.W and char.y - cell.height > cell.height:
        char.y -= cell.height
    elif key == keys.RETURN and mode != 'game':
        enemies = []
        new_enemies(5, (15, 20), (5, 5))
        hearts = []
        swords = []
        win = 0
        new_char()
        mode = 'level_1'

    # Столкновение с врагами
    enemy_index = char.collidelist(enemies)
    if enemy_index != -1:
        char.x = old_x
        char.y = old_y
        colli = 1
        enemy = enemies[enemy_index]
        enemy.health -= char.attack
        if enemy.health <= 0:
            enemies.pop(enemy_index)
            # Добавление бонусов
            if enemy.bonus == 1:
                heart = Actor('heart')
                heart.pos = enemy.pos
                hearts.append(heart)
            if win < 3:
                if enemy.bonus == 2:
                    sword = Actor('sword')
                    sword.pos = enemy.pos
                    swords.append(sword)
        else:
            char.health -= enemy.attack

    victory()


# Логика победы или поражения
def victory():
    global mode, win
    if enemies == [] and char.health > 0 and (mode != 'defeat' and mode != 'win'):
        if win == 1:
            mode = "level_2"
            new_enemies(6, (20, 25), (5, 10))
        elif win == 2:
            mode = 'level_3'
            new_enemies(7, (25, 30), (10, 15))
        elif win == 3:
            mode = 'level_4'
            new_enemies(8, (30, 35), (15, 20))
        elif win == 4:
            mode = 'level_5'
            new_enemies(9, (35, 40), (20, 25))
        win += 1
        char.health = 100
        if win == 5:
            mode = "win"
    if char.health <= 0:
        mode = "defeat"


# Логика бонусов
def update(dt):
    for i in range(len(hearts)):
        if char.colliderect(hearts[i]):
            char.health += 5
            hearts.pop(i)
            break

    for i in range(len(swords)):
        if char.colliderect(swords[i]):
            char.attack += 5
            swords.pop(i)
            break


# pgzero
import random

# Игровое окно
cell = Actor('border')
cell1 = Actor('floor')
cell2 = Actor("crack")
cell3 = Actor("bones")

size_w = 9  # Ширина поля в клетках
size_h = 10  # Высота поля в клетках
WIDTH = cell.width * size_w
HEIGHT = cell.height * size_h

defeat = Actor('defeat')
win_fon = Actor('win')

win = 0
mode = "level_1"
modes_game = ['level_1', 'level_2', 'level_3', 'level_4', 'level_5']
colli = 0

TITLE = "WeCode и Драконы"  # Заголовок окна игры
FPS = 30  # Количество кадров в секунду
my_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 1, 1, 1, 1, 1, 1, 1, 0],
          [0, 1, 1, 2, 1, 3, 1, 1, 0],
          [0, 1, 1, 1, 2, 1, 1, 1, 0],
          [0, 1, 3, 2, 1, 1, 3, 1, 0],
          [0, 1, 1, 1, 1, 3, 1, 1, 0],
          [0, 1, 1, 3, 1, 1, 2, 1, 0],
          [0, 1, 1, 1, 1, 1, 1, 1, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [-1, -1, -1, -1, -1, -1, -1, -1, -1]]  # Строка с атакой и здоровьем


# Главный герой
def new_char():
    global char
    char = Actor('stand')
    char.top = cell.height
    char.left = cell.width
    char.health = 100
    char.attack = 5


new_char()

# Генерация врагов
enemies = []


# Списки здоровья и координат

# Health и attack воспринимают кортежи с начальным и максимальным значением
def new_enemies(value, health, attack):
    poses = []
    for i in range(value):
        while True:
            x = random.randint(1, 7) * cell.width
            y = random.randint(1, 7) * cell.height
            pos = (x, y)
            if pos not in poses:
                poses.append(pos)
                break
            else:
                poses.remove(pos)
        enemy = Actor("enemy", topleft=(x, y))
        enemy.health = random.randint(health[0], health[1])
        enemy.attack = random.randint(attack[0], attack[1])
        enemy.bonus = random.randint(0, 2)
        enemies.append(enemy)


new_enemies(5, (15, 20), (5, 5))

# Бонусы
hearts = []
swords = []


# Отрисовка карты
def map_draw():
    for i in range(len(my_map)):
        for j in range(len(my_map[0])):
            if my_map[i][j] == 0:
                cell.left = cell.width * j
                cell.top = cell.height * i
                cell.draw()
            elif my_map[i][j] == 1:
                cell1.left = cell.width * j
                cell1.top = cell.height * i
                cell1.draw()
            elif my_map[i][j] == 2:
                cell2.left = cell.width * j
                cell2.top = cell.height * i
                cell2.draw()
            elif my_map[i][j] == 3:
                cell3.left = cell.width * j
                cell3.top = cell.height * i
                cell3.draw()

            # Отрисовка


def draw():
    if mode in modes_game:
        screen.fill("#2f3542")
        map_draw()
        char.draw()
        screen.draw.text("HP:", center=(25, 475), color='white', fontsize=20)
        screen.draw.text(str(char.health), center=(75, 475), color='white', fontsize=20)
        screen.draw.text("AP:", center=(375, 475), color='white', fontsize=20)
        screen.draw.text(str(char.attack), center=(425, 475), color='white', fontsize=20)
        for i in range(len(enemies)):
            enemies[i].draw()
            # Отрисовка здоровья врага
            screen.draw.text(str(enemies[i].health), topleft=(enemies[i].x + 5, enemies[i].y - 30), color='white',
                             fontsize=18)
        # отрисовка бонусов
        for i in range(len(hearts)):
            hearts[i].draw()
        for i in range(len(swords)):
            swords[i].draw()
    # Окно победы или поражения
    elif mode == "win":
        screen.fill("white")
        win_fon.draw()
    elif mode == 'defeat':
        screen.fill('white')
        defeat.draw()


# Управление
def on_key_down(key):
    global colli, enemies, hearts, swords, mode, win
    old_x = char.x
    old_y = char.y
    if key == keys.D and char.x + cell.width < WIDTH - cell.width:
        char.x += cell.width
        char.image = 'stand'
    elif key == keys.A and char.x - cell.width > cell.width:
        char.x -= cell.width
        char.image = 'left'
    elif key == keys.S and char.y + cell.height < HEIGHT - cell.height * 2:
        char.y += cell.height
    elif key == keys.W and char.y - cell.height > cell.height:
        char.y -= cell.height
    elif key == keys.RETURN and mode != 'game':
        enemies = []
        new_enemies(5, (15, 20), (5, 5))
        hearts = []
        swords = []
        win = 0
        new_char()
        mode = 'level_1'

    # Столкновение с врагами
    enemy_index = char.collidelist(enemies)
    if enemy_index != -1:
        char.x = old_x
        char.y = old_y
        colli = 1
        enemy = enemies[enemy_index]
        enemy.health -= char.attack
        if enemy.health <= 0:
            enemies.pop(enemy_index)
            # Добавление бонусов
            if enemy.bonus == 1:
                heart = Actor('heart')
                heart.pos = enemy.pos
                hearts.append(heart)
            if win < 3:
                if enemy.bonus == 2:
                    sword = Actor('sword')
                    sword.pos = enemy.pos
                    swords.append(sword)
        else:
            char.health -= enemy.attack

    victory()


# Логика победы или поражения
def victory():
    global mode, win
    if enemies == [] and char.health > 0 and (mode != 'defeat' and mode != 'win'):
        if win == 1:
            mode = "level_2"
            new_enemies(6, (20, 25), (5, 10))
        elif win == 2:
            mode = 'level_3'
            new_enemies(7, (25, 30), (10, 15))
        elif win == 3:
            mode = 'level_4'
            new_enemies(8, (30, 35), (15, 20))
        elif win == 4:
            mode = 'level_5'
            new_enemies(9, (35, 40), (20, 25))
        win += 1
        char.health = 100
        if win == 5:
            mode = "win"
    if char.health <= 0:
        mode = "defeat"


# Логика бонусов
def update(dt):
    for i in range(len(hearts)):
        if char.colliderect(hearts[i]):
            char.health += 5
            hearts.pop(i)
            break

    for i in range(len(swords)):
        if char.colliderect(swords[i]):
            char.attack += 5
            swords.pop(i)
            break

pgzrun.go()
