import pygame
import random
pygame.init()


class Target(pygame.sprite.Sprite):
    FRAMES = ["data/sprites/sprites_1.png", "data/sprites/sprites_2.png"]

    def __init__(self, pos, tile_size_, gr, speed):
        super().__init__(gr)
        self.size = tile_size_
        self.image = pygame.image.load(Target.FRAMES[0]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.pos = pos
        self.rect = self.image.get_rect()
        self.frame = 0
        self.move = 0
        self.speed = speed

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
            if player.score > 10:
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
    def __init__(self, pos, speed, gr, score):
        super().__init__(gr)
        self.score = score
        self.image = pygame.image.load("data/sprites/sprites_0.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.start_speed = speed
        self.speed = [0, 0]
        self.start_a = [0, 9.8]
        self.shooted = False
        self.balls = 10
        self.gr = gr

    def update(self, keys_, frame_speed_, screen_, screen_cap_, tile_size_):
        if not self.shooted:
            if keys_[pygame.K_SPACE]:
                self.shooted = True
                if self.balls is not None:
                    self.balls -= 1
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
                pygame.draw.circle(screen_, (0, 0, 0), tr_pos, tile_size_ * 0.1, 0)
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
                self.__init__([1, 5], [1, 9.8], self.gr, self.score)
        self.rect.center = ((screen_cap_[0] + tile_size_ * self.pos[0]),
                            screen_cap_[1] + tile_size_ * self.pos[1])


if __name__ == "__main__":
    screen = pygame.display.set_mode(eval(open("data/config.txt", "r", encoding="utf-8").readlines()[0]))
    screen_size = screen.get_size()
    player_sprites = pygame.sprite.Group()
    target_sprites = pygame.sprite.Group()
    tile_size = min(screen_size) / 10
    screen_cap_x = (screen_size[0] - tile_size * 10) / 2
    screen_cap_y = (screen_size[1] - tile_size * 10) / 2
    screen_cap = screen_cap_x, screen_cap_y
    ball = Ball([1, 5], [1, 9.8], player_sprites, 0)
    target = Target([9, 5], tile_size, target_sprites, 1)
    clock = pygame.time.Clock()
    running = True
    FONT = pygame.font.Font("data/font/retro-land-mayhem.ttf", 35)
    BG = pygame.image.load("data/sprites/BG.png")
    BG = pygame.transform.scale(BG, (min(screen_size), min(screen_size)))
    while running:
        frame_speed = clock.tick() / 1000
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                running = False
        screen.fill((0, 0, 0))
        screen.blit(BG, screen_cap)
        player_sprites.update(keys, frame_speed, screen, screen_cap, tile_size)
        player_sprites.draw(screen)
        target_sprites.update(frame_speed, screen, screen_cap, tile_size, ball, player_sprites)
        target_sprites.draw(screen)
        text = FONT.render(f"Score: {ball.score}", True, (255, 255, 255))
        screen.blit(text, (0, 0))
        pygame.display.flip()
    pygame.quit()
