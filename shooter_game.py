from pygame import *
from random import randint
from time import sleep

win_width = 900
win_height = 700
window = display.set_mode((win_width, win_height))
display.set_caption("Расстрел чубриков")
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
FPS = 60
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 80)
lose = font2.render('Ты проиграл, лошара!', True, (255, 0, 0))
win = font2.render('Ты выиграл, красава!', True, (255, 215, 0))
# clock = clock.Clock()
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
shot = mixer.Sound('fire.ogg')
lost = 0
kills = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 10, self.rect.top, 15, 20, 30)
        bullets.add(bullet)
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()



class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            self.rect.y = 0
            self.rect.x = randint(1, win_width - 15)
            global lost
            lost += 1

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(1, win_width - 15), 0, randint(1, 5), 65, 65)
    monsters.add(monster)
bullets = sprite.Group()

player = Player('rocket.png', 450, 600, 25, 60, 60)
finish = False
run = True
while run:


    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                shot.play()
    if not finish:
        window.blit(background, (0, 0))
        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprite_list:
            kills += 1
            monster = Enemy('ufo.png', randint(1, win_width - 15), 0, randint(1, 5), 65, 65)
            monsters.add(monster)
        if kills >= 10:
            window.blit(win, (20, 200))
            
            finish = True
        if lost >= 3:
            window.blit(lose, (20, 200))
            
            finish = True
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        text_lose = font1.render(' Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 10))
        text_win = font1.render(' Убито: ' + str(kills), 1, (255, 255, 255))
        window.blit(text_win, (10, 50))
        display.update()
        time.delay(FPS)


        