import pygame
import random

pygame.init()
pygame.mixer.init()

width = 800
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Save the Ball by Mughal")

icon = pygame.image.load("obstacle.png")
pygame.display.set_icon(icon)

gravity = 0.7
jump_vel = -16

bg = pygame.image.load("background.png")

ft = pygame.font.SysFont("Small Bold Pixel-7", 45)
ft_big = pygame.font.SysFont("Small Bold Pixel-7", 80)

jump = pygame.mixer.Sound("jump.wav")
collision_sound = pygame.mixer.Sound("collision_sound.wav")
score_sound = pygame.mixer.Sound("score_sound.wav")

score = 0

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("dino.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)
        self.rect.x = 150
        self.rect.y = height // 2
        self.velocity_y = 0
        self.is_jumping = False

    def update(self):
        self.velocity_y += gravity
        self.rect.y += self.velocity_y

        if self.rect.y >= height - 199:
            self.rect.y = height - 199
            self.velocity_y = 0
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = jump_vel
            self.is_jumping = True

class Obstacle(pygame.sprite.Sprite):
    ob_vel = -8

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("obstacle.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 740
        self.rect.y = height - 185

    def update(self):
        self.rect.x += Obstacle.ob_vel

        if score > 0 and score % 100 == 0 and score < 2099:
            Obstacle.ob_vel -= 0.05

def generate_obstacle():
    obstacle = Obstacle()
    all_sprites.add(obstacle)

dino = Dino()
all_sprites = pygame.sprite.Group()

obstacle_timer = 0
obstacle_delay = random.randint(600, 1800)

clock = pygame.time.Clock()

running = True
game_over = False
jumped = False

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
        if game_over:
            game_over = False
            score = 0
            all_sprites.empty()
            dino.rect.y = height // 2
            dino.velocity_y = 0
            obstacle_timer = 0
            obstacle_delay = random.randint(600, 1800)
            Obstacle.ob_vel = -8
        elif not jumped:
            dino.jump()
            jump.play()
            jumped = True
    else:
        jumped = False

    collision = pygame.sprite.spritecollide(dino, all_sprites, False)
    if collision:
        if not game_over:
            game_over = True
            collision_sound.play()
    else:
        if not game_over:
            score += 1

    if score % 500 == 0 and score > 0:
        score_sound.play()

    if not game_over:
        dino.update()
        all_sprites.update()

    screen.blit(bg, dest=(0, 0))

    all_sprites.draw(screen)

    screen.blit(dino.image, dino.rect)

    if game_over:
        game_over_text = ft_big.render("Game Over", True, (255, 0, 0))
        score_text = ft.render("Final Score: " + str(score), True, (100, 100, 100))

        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2 + game_over_text.get_height() // 2 + 10))

    score_text = ft.render("Score: " + str(score), True, (100, 100, 100))
    screen.blit(score_text, (5, 5))

    pygame.display.update()

    obstacle_timer += clock.get_time()
    if obstacle_timer >= obstacle_delay and not game_over:
        generate_obstacle()
        obstacle_timer = 0
        obstacle_delay = random.randint(700, 1800)

pygame.quit()
