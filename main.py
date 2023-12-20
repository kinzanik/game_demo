import sys

import pygame
import random as r


pygame.init()
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Кто читает тот умрет')
heart_image = pygame.image.load('./data/heart.png')
box_width, box_height = 200, 200
box_x, box_y = (width - box_width) // 2, (height - box_height) // 2
heart_width, heart_height = 16, 16
heart_speed = 5
running = True
clock = pygame.time.Clock()


player = pygame.sprite.Group()
attack1 = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()


class Player(pygame.sprite.Sprite):
    default_heart = pygame.image.load('./data/heart.png')
    immortal_heart = pygame.image.load('./data/immortal_heart.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Player.default_heart
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 300 - 7, 200 - 14
        self.immortal = False
        self.immortal_timer = None
        self.immortal_duration = 2000

    def update(self, move):
        if move == 'left':
            self.rect = self.rect.move(-4, 0)
        if move == 'right':
            self.rect = self.rect.move(4, 0)
        if move == 'down':
            self.rect = self.rect.move(0, 4)
        if move == 'up':
            self.rect = self.rect.move(0, -4)

    def heat(self):
        if pygame.sprite.spritecollideany(self, attack1) and not self.immortal:
            self.immortal = True
            self.immortal_timer = pygame.time.get_ticks()
            self.image = Player.immortal_heart

        if self.immortal:
            current_time = pygame.time.get_ticks()
            if current_time - self.immortal_timer >= self.immortal_duration:
                self.immortal = False
                self.image = Player.default_heart

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def set_x(self, move):
        self.rect.x = move

    def set_y(self, move):
        self.rect.y = move


class Attack1(pygame.sprite.Sprite):
    def __init__(self, group, vector):
        super().__init__(group)
        self.vector = vector
        self.name = 'peaks'
        self.image = pygame.image.load(f'./data/attack_sprite1_{vector}.png')
        self.rect = self.image.get_rect()
        if self.vector == 'down':
            self.rect.x = r.randint((width - box_width) // 2, (width - box_width) // 2 + 180)
            self.rect.y = (height - box_height) // 2 + 5
        elif self.vector == 'up':
            self.rect.x = r.randint((width - box_width) // 2, (width - box_width) // 2 + 180)
            self.rect.y = (height - box_height) + 100 - 30
        elif self.vector == 'right':
            self.rect.x = box_x
            self.rect.y = r.randint(box_y, box_y + 170)
        elif self.vector == 'left':
            self.rect.x = box_x + 200 - 30
            self.rect.y = r.randint(box_y, box_y + 170)

    def update(self):
        if self.vector == 'down':
            self.rect = self.rect.move(0, 3)
        elif self.vector == 'up':
            self.rect = self.rect.move(0, -3)
        elif self.vector == 'right':
            self.rect = self.rect.move(3, 0)
        elif self.vector == 'left':
            self.rect = self.rect.move(-3, 0)

    def get_vector(self):
        return self.vector

    def get_name(self):
        return self.name


class Attack2(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.name = 'ball'
        self.image = pygame.image.load('./data/attack_sprite2.png')
        self.rect = self.image.get_rect()
        self.vx = 0
        while self.vx == 0:
            self.vx = r.randint(-2, 2)
        pos = r.randint(0, 1)
        if pos == 0:
            self.rect.x = r.randint(box_x + 20, box_x + box_width - 20)
            self.rect.y = box_y + 3
            self.vy = 2
        elif pos == 1:
            self.rect.x = r.randint(box_x + 20, box_x + box_width - 20)
            self.rect.y = box_y + box_height - 15
            self.vy = r.randint(-2, -1)

    def update(self):
        if self.rect.x <= box_x or self.rect.x >= box_x + box_width - 16:
            self.vx *= -1
        if self.rect.y <= box_y or self.rect.y >= box_y + box_height - 14:
            self.vy *= -1
        self.rect = self.rect.move(self.vx, self.vy)

    def get_name(self):
        return self.name


heart = Player(player)
a = 1
MYEVENTTYPE = pygame.USEREVENT
pygame.time.set_timer(MYEVENTTYPE, 200)

while running:
    screen.fill('black')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == MYEVENTTYPE:
            sps = ['up', 'down', 'left', 'right']
            # if a != 1000:
            #     Attack1(attack1, r.choice(sps))
            #     a += 1
            if a <= 10:
                Attack2(attack1)
                a += 1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.update('left')
    if keys[pygame.K_RIGHT]:
        player.update('right')
    if keys[pygame.K_UP]:
        player.update('up')
    if keys[pygame.K_DOWN]:
        player.update('down')

    if heart.get_x() < box_x:
        heart.set_x(box_x + 2)
    if heart.get_x() > box_x + box_width - heart_width:
        heart.set_x(box_x + box_width - heart_width - 2)
    if heart.get_y() < box_y:
        heart.set_y(box_y + 2)
    if heart.get_y() > box_y + box_height - heart_height:
        heart.set_y(box_y + box_height - heart_height - 2)
    pygame.draw.rect(screen, 'white', (box_x, box_y, box_width, box_height), 2)

    ban_attack = []
    for i in attack1:
        if i.get_name() == 'peaks':
            if i.get_vector() == 'down' and i.rect.y >= 270:
                ban_attack.append(i)
            elif i.get_vector() == 'up' and i.rect.y <= box_y:
                ban_attack.append(i)
            elif i.get_vector() == 'right' and i.rect.x >= box_x + 170:
                ban_attack.append(i)
            elif i.get_vector() == 'left' and i.rect.x <= box_x:
                ban_attack.append(i)

    for i in ban_attack:
        attack1.remove(i)

    player.draw(screen)
    attack1.draw(screen)
    heart.heat()
    attack1.update()

    pygame.display.flip()
    clock.tick(60)
