import sys
import pygame

tile_images = {
    'wall': pygame.image.load('wall.png'),
    'empty': pygame.image.load('grass2.png'),
    'hole': pygame.image.load('hole2.png')
}
ball_image = pygame.image.load('mouse.png')
ball_in_hole_image = pygame.image.load('mouse_in_hole.png')

tile_width = tile_height = 50

# группы спрайтов
all_sprites = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
holes_group = pygame.sprite.Group()

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

class Ball(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = ball_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

def load_level(filename):
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

def generate_level(level, screen):
    ball = None
    walls_group.empty()
    holes_group.empty()
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                obj = Tile('empty', x, y)
            elif level[y][x] == '#':
                obj = Tile('wall', x, y)
                obj.add(walls_group)
            elif level[y][x] == '@':
                obj = Ball(x, y)
                ball = obj
            elif level[y][x] == '0':
                obj = Tile('hole', x, y)
                obj.add(holes_group)
            screen.blit(obj.image, obj.rect)
    return ball

def movement(obj, direction, step, walls, holes):
    current_x = obj.rect.x
    current_y = obj.rect.y
    ball_in_hole = False
    if direction == 'left':
        while not pygame.sprite.spritecollideany(obj, walls):
            if pygame.sprite.spritecollideany(obj, holes):
                ball_in_hole = True
                break
            obj.rect.x -= step
        if not ball_in_hole:
            obj.rect.x += step
    elif direction == 'right':
        while not pygame.sprite.spritecollideany(obj, walls):
            if pygame.sprite.spritecollideany(obj, holes):
                ball_in_hole = True
                break
            obj.rect.x += step
        if not ball_in_hole:
            obj.rect.x -= step
    elif direction == 'up':
        while not pygame.sprite.spritecollideany(obj, walls):
            if pygame.sprite.spritecollideany(obj, holes):
                ball_in_hole = True
                break
            obj.rect.y -= step
        if not ball_in_hole:
            obj.rect.y += step
    elif direction == 'down':
        while not pygame.sprite.spritecollideany(obj, walls):
            if pygame.sprite.spritecollideany(obj, holes):
                ball_in_hole = True
                break
            obj.rect.y += step
        if not ball_in_hole:
            obj.rect.y -= step
    if obj.rect.x != current_x or obj.rect.y != current_y:
        if ball_in_hole:
            screen.blit(ball_in_hole_image, obj.rect)
        else:
            screen.blit(obj.image, obj.rect)

        empty.rect.x = current_x
        empty.rect.y = current_y
        screen.blit(empty.image, empty.rect)

        pygame.display.flip()

        return ball_in_hole

def endlevel(screen):
    fon = pygame.transform.scale(pygame.image.load('fon.png'), (screen.get_width(), tile_height))
    text_coord = screen.get_height() - tile_height
    screen.blit(fon, (0, text_coord))
    font = pygame.font.Font(None, 30)
    line = 'Congratulations! Press [SPACE] to start a new level.'
    string_rendered = font.render(line, 1, pygame.Color('white'))
    text_rect = string_rendered.get_rect()
    text_rect.top = text_coord + 16
    text_rect.x = 10
    screen.blit(string_rendered, text_rect)
    pygame.display.flip()

def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':

    FPS = 60
    empty = Tile('empty', 0, 0)

    pygame.init()
    pygame.display.set_caption('Help the mouse')
    size = width, height = 1000, 1000
    screen = pygame.display.set_mode(size)

    #Заставка
    screen.blit(pygame.image.load('title.png'), (0, 0))
    pygame.display.flip()
    start = False
    while not start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True

    current_level = 1
    max_level = 2
    success = False

    new_ball = generate_level(load_level('map1.txt'), screen)
    pygame.display.flip()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                # do smth
                # current_x = new_ball.rect.x
                # current_y = new_ball.rect.y
                if not success:
                    if event.key == pygame.K_LEFT:
                        success = movement(new_ball, 'left', tile_width, walls_group, holes_group)
                    elif event.key == pygame.K_RIGHT:
                        success = movement(new_ball, 'right', tile_width, walls_group, holes_group)
                    elif event.key == pygame.K_UP:
                        success = movement(new_ball, 'up', tile_height, walls_group, holes_group)
                    elif event.key == pygame.K_DOWN:
                        success = movement(new_ball, 'down', tile_height, walls_group, holes_group)
                    if success:
                        endlevel(screen)
                else:
                    if event.key == pygame.K_SPACE:
                        current_level += 1
                        if current_level > max_level:
                            current_level = 1
                        new_ball = generate_level(load_level('map' + str(current_level) + '.txt'), screen)
                        pygame.display.flip()
                        success = False

                clock.tick(FPS)
