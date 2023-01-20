import pygame
import random
import os
import pygame_widgets
from pygame_widgets.button import Button
pygame.init()


class Target(pygame.sprite.Sprite):
    FRAMES = ["data/sprites/target_0.png", "data/sprites/target_1.png"]

    def __init__(self, pos, tile_size_, gr, speed, player):
        super().__init__(gr)
        self.size = tile_size_
        self.image = pygame.image.load(Target.FRAMES[0]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.pos = pos
        self.rect = self.image.get_rect()
        self.frame = 0
        self.move = 0
        self.speed = speed
        if player.score >= 10:
            self.move = random.choice([1, -1])
            self.speed = player.score / 10

    def update(self, frame_speed_, screen_, screen_cap_, tile_size_, player, player_sprites_):
        self.frame += 1 * frame_speed_
        if self.frame < 0.5:
            self.image = pygame.image.load(Target.FRAMES[0]).convert_alpha()
        elif self.frame > 1:
            self.frame = 0
        elif self.frame > 0.5:
            self.image = pygame.image.load(Target.FRAMES[1]).convert_alpha()
        if self.rect.colliderect(player.rect):
            self.pos[1] = random.choice(range(1, 10))
            player.score += 1
            player.balls += 1
            if player.score >= 10:
                self.move = random.choice([1, -1])
                self.speed = player.score / 10
        if self.pos[1] > 9:
            self.pos[1] = 9
            self.move = -1
        elif self.pos[1] < 1:
            self.pos[1] = 1
            self.move = 1
        self.pos[1] += self.speed * self.move * frame_speed_
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect.center = (screen_cap_[0] + self.pos[0] * tile_size_,
                            screen_cap_[1] + self.pos[1] * tile_size_)


class Ball(pygame.sprite.Sprite):
    SKINS = ["data/sprites/player_0.png",
             "data/sprites/player_1.png",
             "data/sprites/player_2.png",
             "data/sprites/player_3.png",
             "data/sprites/player_4.png"]

    def __init__(self, pos, speed, gr, score_, balls_, tile_size_, skin):
        super().__init__(gr)
        self.score = score_
        self.skin = skin
        self.image = pygame.image.load(Ball.SKINS[self.skin]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size_, tile_size_))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.start_speed = speed
        self.speed = [0, 0]
        self.start_a = [0, 9.8]
        self.shooted = False
        self.balls = balls_
        self.gr = gr

    def update(self, events, keys_, frame_speed_, screen_, screen_cap_, tile_size_):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS:
                self.skin += 1
                if self.skin > 4:
                    self.skin = 4
                self.image = pygame.image.load(Ball.SKINS[self.skin]).convert_alpha()
                self.image = pygame.transform.scale(self.image, (tile_size_, tile_size_))
                self.rect = self.image.get_rect()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
                self.skin -= 1
                if self.skin < 0:
                    self.skin = 0
                self.image = pygame.image.load(Ball.SKINS[self.skin]).convert_alpha()
                self.image = pygame.transform.scale(self.image, (tile_size_, tile_size_))
                self.rect = self.image.get_rect()
        if not self.shooted:
            if keys_[pygame.K_SPACE]:
                self.shooted = True
            if keys_[pygame.K_UP]:
                self.start_speed[1] += 10 * frame_speed_
            if keys_[pygame.K_DOWN]:
                self.start_speed[1] -= 10 * frame_speed_
            if keys_[pygame.K_LEFT]:
                self.start_speed[0] -= 10 * frame_speed_
            if keys_[pygame.K_RIGHT]:
                self.start_speed[0] += 10 * frame_speed_
            if self.start_speed[0] > 7:
                self.start_speed[0] = 7
            elif self.start_speed[0] < 0:
                self.start_speed[0] = 0
            if self.start_speed[1] > 20:
                self.start_speed[1] = 20
            elif self.start_speed[1] < -10:
                self.start_speed[1] = -10
            speed = self.start_speed[1]
            for i in range(1, 5):
                speed -= self.start_a[1] * 0.05
                tr_pos = (screen_cap_[0] + tile_size_ * (self.pos[0] + self.start_speed[0] * 0.1 * i),
                          screen_cap_[1] + tile_size_ * (self.pos[1] - speed * 0.1 * i))
                pygame.draw.circle(screen_, (128, 128, 128), tr_pos, tile_size_ * 0.1, 0)
        else:
            if self.start_speed[1] is not None and self.start_speed[0] is not None:
                self.speed[1] = self.start_speed[1]
                self.speed[0] = self.start_speed[0]
                self.start_speed[1] = None
                self.start_speed[0] = None
            self.speed[1] -= self.start_a[1] * frame_speed_
            self.pos[0] += self.speed[0] * frame_speed_
            self.pos[1] -= self.speed[1] * frame_speed_
            if self.pos[0] > 15 or self.pos[1] > 15 or self.pos[0] < -5 or self.pos[1] < -5:
                self.__init__([1, 5], [1, 9.8], self.gr, self.score, self.balls - 1, tile_size_, self.skin)
        self.rect.center = ((screen_cap_[0] + tile_size_ * self.pos[0]),
                            screen_cap_[1] + tile_size_ * self.pos[1])


class InputBox:
    COLOR_INACTIVE = (0, 128, 0)
    COLOR_ACTIVE = (0, 255, 0)
    FONT = pygame.font.Font("data/font/Undertale-Battle-Font.ttf", 35)

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = InputBox.COLOR_INACTIVE
        self.text = text
        self.txt_surface = InputBox.FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = InputBox.COLOR_ACTIVE if self.active else InputBox.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = InputBox.FONT.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


def start_screen():
    config_file = open("data/config.txt", "r", encoding="utf-8").readlines()
    screen = pygame.display.set_mode(eval(config_file[0]))
    screen_size = screen.get_size()
    pygame.mouse.set_visible(False)
    cursor_im = pygame.transform.scale(pygame.image.load("data/sprites/cursor_0.png").convert_alpha(), (64, 64))
    user_name = InputBox(0, 0, 500, 50, "User_Name")
    c_pos = (0, 0)
    button = Button(
        screen, 100, 100, 300, 150, text='Играть',
        fontSize=50, margin=20,
        inactiveColour=(0, 128, 0),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: main(screen, user_name.text, cursor_im)
    )
    running = True
    while running:
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                main(screen, user_name.text, cursor_im)
            if event.type == pygame.MOUSEMOTION:
                c_pos = event.pos
            user_name.handle_event(event)
        user_name.update()
        user_name.rect.center = (screen_size[0] / 2, screen_size[1] / 2)
        button.setX(screen_size[0] / 2 - button.getWidth() / 2)
        button.setY(screen_size[1] / 2 - button.getHeight() / 2 + 150)
        screen.fill((0, 0, 0))
        pygame_widgets.update(events)
        user_name.draw(screen)
        screen.blit(cursor_im, c_pos)
        pygame.display.flip()
    pygame.quit()


def main(screen, name, cursor):
    c_pos = (0, 0)
    try:
        save_file = open(f"saves/{name}_sav.txt", "r", encoding="utf-8").readlines()
    except Exception as error:
        print(error)
        if not os.path.exists("saves"):
            os.mkdir("saves")
        save_file = None
    screen_size = screen.get_size()
    player_sprites = pygame.sprite.Group()
    target_sprites = pygame.sprite.Group()
    tile_size = min(screen_size) / 10
    screen_cap_x = (screen_size[0] - tile_size * 10) / 2
    screen_cap_y = (screen_size[1] - tile_size * 10) / 2
    screen_cap = screen_cap_x, screen_cap_y
    if save_file is None:
        ball = Ball([1, 5], [1, 9.8], player_sprites, 0, 10, tile_size, 0)
    else:
        ball = Ball([1, 5],
                    [1, 9.8],
                    player_sprites,
                    int(save_file[0]),
                    int(save_file[1]),
                    tile_size,
                    int(save_file[2]))
    target = Target([9, 5], tile_size, target_sprites, 1, ball)
    clock = pygame.time.Clock()
    font = pygame.font.Font("data/font/Undertale-Battle-Font.ttf", 35)
    bg = pygame.image.load("data/sprites/BG.png")
    bg = pygame.transform.scale(bg, (min(screen_size), min(screen_size)))
    bg1 = pygame.image.load("data/sprites/BG_1.png")
    bg1 = pygame.transform.scale(bg1, (min(screen_size), min(screen_size)))
    exiting = False
    running = True
    game_over = False
    while running:
        frame_speed = clock.tick() / 1000
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                exiting = True
                running = False
            if event.type == pygame.MOUSEMOTION:
                c_pos = event.pos
        if keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_r]:
            main(screen, name, cursor)
        if ball.balls <= 0:
            game_over = True
        screen.fill((0, 0, 0))
        if not game_over:
            screen.blit(bg, screen_cap)
            player_sprites.update(events, keys, frame_speed, screen, screen_cap, tile_size)
            player_sprites.draw(screen)
            target_sprites.update(frame_speed, screen, screen_cap, tile_size, ball, player_sprites)
            target_sprites.draw(screen)
            score = font.render(f"Очков: {ball.score}", True, (255, 255, 255))
            balls = font.render(f"Мячей: {ball.balls}", True, (255, 255, 255))
            screen.blit(score, (0, 0))
            screen.blit(balls, (0, screen_size[1] - 50))
        else:
            screen.blit(bg1, screen_cap)
        screen.blit(cursor, c_pos)
        pygame.display.flip()
    if not game_over:
        save_file = open(f"saves/{name}_sav.txt", "w+", encoding="utf-8")
        save_file.write(f'{ball.score}\n{ball.balls}\n{ball.skin}')
    if exiting:
        pygame.quit()


start_screen()
