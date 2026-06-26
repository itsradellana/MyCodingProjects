import asyncio
import pygame
from pygame import *
from random import randint
from time import time as timer

# Game state variables (module level for easy access)
lost = 0
score = 0
life = 3
num_fire = 0
rel_time = False
last_time = 0

async def main():
    global lost, score, life, num_fire, rel_time, last_time
    
    mixer.init()
    mixer.music.load('space.ogg')
    mixer.music.play()
    fire_sound = mixer.Sound('fire.ogg')
    lost_sound = mixer.Sound("lost.ogg")
    win_sound = mixer.Sound("win.ogg")

    font.init()
    font2 = font.Font(None, 36)

    img_back = 'galaxy.jpg'
    img_hero = 'rocket.png'

    class GameSprite(sprite.Sprite):
        def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, asteroid=False):
            sprite.Sprite.__init__(self)
            self.image = transform.scale(image.load(player_image), (size_x, size_y))
            self.speed = player_speed
            self.rect = self.image.get_rect()
            self.rect.x = player_x
            self.rect.y = player_y
            self.asteroid = asteroid

        def reset(self):
            window.blit(self.image, (self.rect.x, self.rect.y))

    class Player(GameSprite):
        def update(self):
            keys = key.get_pressed()
            if keys[K_LEFT] and self.rect.x > 5:
                self.rect.x -= self.speed
            if keys[K_RIGHT] and self.rect.x < win_width - 80:
                self.rect.x += self.speed
            if keys[K_UP]:
                self.rect.y -= self.speed
            if keys[K_DOWN]:
                self.rect.y += self.speed

        def fire(self):
            global num_fire, rel_time
            if num_fire < 7 and not rel_time:
                bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
                bullets.add(bullet)
                fire_sound.play()
                num_fire += 1

    class Enemy(GameSprite):
        def update(self):
            self.rect.y += self.speed
            global lost

            if self.rect.y > win_height:
                self.rect.x = randint(80, win_width - 80)
                self.rect.y = 0
                if not self.asteroid:
                    lost += 1

    class Bullet(GameSprite):
        def update(self):
            self.rect.y += self.speed
            if self.rect.y < 0:
                self.kill()

    win_width = 900
    win_height = 700
    display.set_caption('Galaxy Defender')
    window = display.set_mode((win_width, win_height))
    background = transform.scale(image.load(img_back), (win_width, win_height))
    ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

    monsters = sprite.Group()
    for i in range(3):
        monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
        monsters.add(monster)

    bullets = sprite.Group()

    asteroids = sprite.Group()
    for i in range(3):
        asteroid = Enemy('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1, 7), True)
        asteroids.add(asteroid)

    finish = False
    run = True
    font1 = font.Font(None, 80)
    win_text = font1.render('YOU WIN!', True, (255, 255, 255))
    lose_text = font1.render('YOU LOSE!', True, (180, 0, 0))

    while run:
        for e in event.get():
            if e.type == QUIT:
                run = False
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    ship.fire()
                if e.key == K_r and num_fire >= 5 and not rel_time:
                    rel_time = True
                    last_time = timer()

        if not finish:
            window.blit(background, (0, 0))

            ship.update()
            monsters.update()
            bullets.update()
            asteroids.update()

            ship.reset()
            monsters.draw(window)
            bullets.draw(window)
            asteroids.draw(window)

            if rel_time:
                now_time = timer()
                if now_time - last_time < 3:
                    reload_text = font2.render('hold on, reloading~ :)', 1, (150, 0, 0))
                    window.blit(reload_text, (260, 460))
                else:
                    num_fire = 0
                    rel_time = False

            collides = sprite.groupcollide(monsters, bullets, True, True)
            for c in collides:
                score += 1
                monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                monsters.add(monster)

            if sprite.spritecollide(ship, monsters, True):
                monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                monsters.add(monster)
                life -= 1

            if sprite.spritecollide(ship, asteroids, True):
                asteroid = Enemy('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
                asteroids.add(asteroid)
                life -= 1

            if lost >= 3 or life < 1:
                finish = True
                window.blit(lose_text, (300, 300))
                lost_sound.play()

            if score >= 10:
                finish = True
                window.blit(win_text, (300, 300))
                win_sound.play()

            text = font2.render('Score: ' + str(score), 1, (225, 225, 225))
            window.blit(text, (10, 20))

            text_life = font2.render('Life: ' + str(life), 1, (225, 225, 225))
            window.blit(text_life, (10, 50))

            text_lost = font2.render('Lost: ' + str(lost), 1, (225, 225, 225))
            window.blit(text_lost, (10, 80))

            text_ammo = font2.render('Bullets: ' + str(7 - num_fire), 1, (225, 225, 225))
            window.blit(text_ammo, (10, 110))

        display.update()
        await asyncio.sleep(0.05)  # 50ms delay = same as original time.delay(50)

# Start the game
asyncio.run(main())
