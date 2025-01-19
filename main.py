import pygame
from pygame import sprite, transform, image, key, K_LEFT, K_RIGHT
from random import randint

win_width = 700  # Define the width of the window
win_height = 500  # Define the height of the window

# Initialize pygame
pygame.init()
pygame.font.init()  # Initialize font module

# Load images
img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_bullet = 'bullet.png'
img_enemy = 'ufo.png'

# Initialize fonts
font1 = pygame.font.Font(None, 80)
font2 = pygame.font.Font(None, 36)
win = font1.render('You win!', True, (255, 255, 255))
lose = font1.render('You lose!', True, (255, 255, 255))

# Initialize score and lost counters
score = 0
lost = 0 
max_lost = 3

# Define GameSprite class
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed

    def reset(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Define Player class
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - self.rect.width - 5:
            self.rect.x += self.speed  

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, -15, 20, 20)
        bullets.add(bullet)

# Define Enemy class
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            global lost
            lost += 1   

# Define Bullet class
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

# Create game window
window = pygame.display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# Create sprite groups
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Create player object
player = Player(img_hero, 5, win_height - 100, 10, 80, 100)

# Create enemy objects
for i in range(5):
    enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, randint(1, 5), 80, 50)
    enemies.add(enemy)

# Main game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire()

    # Update game objects
    player.update()
    enemies.update()
    bullets.update()

    # Check for collisions
    collisions = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for collision in collisions:
        score += 1
        enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, randint(1, 5), 80, 50)
        enemies.add(enemy)

    # Draw everything
    window.blit(background, (0, 0))
    player.reset(window)
    enemies.draw(window)
    bullets.draw(window)

    # Display score and lost counters
    text_score = font2.render("Score: " + str(score), True, (255, 255, 255))
    window.blit(text_score, (10, 20))
    text_lost = font2.render("Lost: " + str(lost), True, (255, 255, 255))
    window.blit(text_lost, (10, 50))

    # Check for game over
    if lost >= max_lost:
        window.blit(lose, (200, 200))
        pygame.display.update()
        pygame.time.delay(3000)
        run = False

    pygame.display.update()
    pygame.time.delay(50)

pygame.quit()