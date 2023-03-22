# Space Invader 1.0
# Main File
# By: Peerapat Lam (Jacky)

# Importing all module needed...
import pygame
import os
import time
import random
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 850, 850
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invader 2.0")

# Load images for our game...
RED_SPACE_SHIP = pygame.image.load(os.path.join("images", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("images", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("images", "pixel_ship_blue_small.png"))

# Main Player...
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("images", "pixel_ship_yellow.png"))

# Laser...
RED_LASER = pygame.image.load(os.path.join("images", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("images", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("images", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("images", "pixel_laser_yellow.png"))

# Background...
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("images", "background-black.png")), (HEIGHT, WIDTH))

# Background Music...
BACKGROUND_MUSIC = pygame.mixer.music.load("BACKGROUND_MUSIC.wav")
pygame.mixer.music.play(-1)

# Sound Effects...
EXPLOSION_SOUND = pygame.mixer.Sound("EXPLOSION.wav")
LASER_SOUND = pygame.mixer.Sound("LASER_SOUND.wav")
START = pygame.mixer.Sound("START.wav")
OVER = pygame.mixer.Sound("OVER.wav")


# Declaring the lasers...
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, velocity):
        self.y += velocity

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)
    
    def collision(self, obj):
        return collide(self, obj)
        


# Declaring general ship's class....
class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health 
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0 

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, velocity, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10 
                self.lasers.remove(laser)
                EXPLOSION_SOUND.play()

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()


# Declaring player's properties...
class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, velocity, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs: 
                    if laser.collision(obj):
                        objs.remove(obj) 
                        EXPLOSION_SOUND.play()
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                            EXPLOSION_SOUND.play()

    def draw(self, window):
        super().draw(window)
        self.health_bar(window)

    def health_bar(self, window):
        # Red part of health
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        # Green part of health
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))


# Declaring enemy's properties...
class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color, health = 100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, velocity):
        self.y += velocity

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 19, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


# Object collision...
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


# Other essential properties...
def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("arialblack", 45)
    lost_font1 = pygame.font.SysFont("arialblack", 60)
    lost_font2 = pygame.font.SysFont("arialblack", 40)

    enemies = []
    wave_length = 5
    enemy_velocity = 1

    player_velocity = 5 # Move by 5 pixels
    laser_velocity = 6 # Move by 6 pixels 

    player = Player(375, 650)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

# Drawing the background...
    def redraw_window():
        WIN.blit(BACKGROUND, (0,0))
        # Draw Text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

# Drawing enemies...
        for enemy in enemies:
            enemy.draw(WIN)

# Drawing player...
        player.draw(WIN)

# Game over...
        if lost:
            OVER.play()
            lost_label1 = lost_font1.render("Game Over!", 1, (255,255,255))
            lost_label2 = lost_font2.render("Game Restarting in 3 Seconds", 1, (255,255,255))
            WIN.blit(lost_label1, (WIDTH / 2 - lost_label1.get_width() / 2, 320))
            WIN.blit(lost_label2, (WIDTH / 2 - lost_label2.get_width() / 2, 450))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

# Implementing the lives system and loosing the game...
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:    # Display "Game Over!" for 3 seconds
                run = False
            else:
                continue

# Spawning enemies...
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

# Quit the game by pressing the "x"...
        for event in pygame.event.get():
            if event.type ==  pygame.QUIT:
                quit()

# Player's movement...
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_velocity > 0:                                   # Move Left
            player.x -= player_velocity
        if keys[pygame.K_d] and player.x + player_velocity + player.get_width() < WIDTH:          # Move Right
            player.x += player_velocity
        if keys[pygame.K_w] and player.y - player_velocity > 0:                                   # Move Up
            player.y -= player_velocity
        if keys[pygame.K_s] and player.y + player_velocity + player.get_height() + 16 < HEIGHT:   # Move Down
            player.y += player_velocity
        if keys[pygame.K_SPACE]:
            LASER_SOUND.play()
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_velocity)
            enemy.move_lasers(laser_velocity, player) 

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
                EXPLOSION_SOUND.play()
            elif enemy.y + enemy.get_height() > HEIGHT: 
                lives -= 1
                enemies.remove(enemy)
                EXPLOSION_SOUND.play()

        player.move_lasers(-laser_velocity, enemies)


# Main Menu...
def main_menu():
    title_font1 = pygame.font.SysFont("arialblack", 55)
    title_font2 = pygame.font.SysFont("arialblack", 65)
    run = True
    while run:
        WIN.blit(BACKGROUND, (0, 0))
        title_label1 = title_font1.render("Click To Begin!" , 1, (255, 255, 255))
        title_label2 = title_font2.render("Space Invader 2.0" , 1, (255, 255, 255))
        WIN.blit(title_label1, (WIDTH / 2 - title_label1.get_width() / 2, 450))
        WIN.blit(title_label2, (WIDTH / 2 - title_label2.get_width() / 2, 320))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                START.play()
                main()
    pygame.quit()


main_menu()