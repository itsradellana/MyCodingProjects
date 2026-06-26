from pygame import *
from random import randint
from time import time as timer
from math import sin, cos, sqrt
import sys

try:
    FINGERDOWN
except NameError:
    FINGERDOWN = USEREVENT + 10
    FINGERUP = USEREVENT + 11
    FINGERMOTION = USEREVENT + 12

show_touch = False
try:
    touch.init()
    if touch.get_num_devices() > 0:
        show_touch = True
except:
    _p = sys.platform.lower()
    if 'android' in _p or 'ios' in _p or _p.startswith('emscripten'):
        show_touch = True

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
lost_sound = mixer.Sound("lost.wav")
win_sound = mixer.Sound("win.wav")

font.init()
font2 = font.Font(None, 36)

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
lost = 0
score = 0
life = 3

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
        if (keys[K_LEFT] or t_left) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (keys[K_RIGHT] or t_right) and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] or t_up:
            self.rect.y -= self.speed
        if keys[K_DOWN] or t_down:
            self.rect.y += self.speed

    def fire(self):
        global num_fire
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

js_finger = None
js_cx, js_cy = 130, 565
js_r = 55
js_tx, js_ty = js_cx, js_cy
t_left = False
t_right = False
t_up = False
t_down = False

shoot_finger = None
shoot_bx, shoot_by = 770, 565
shoot_br = 42

reload_finger = None
reload_bx, reload_by = 260, 565
reload_br = 36
last_touch_shoot = 0
shoot_cooldown = 0.28

def update_js(fx, fy):
    global t_left, t_right, t_up, t_down, js_tx, js_ty
    dx = fx - js_cx
    dy = fy - js_cy
    dist = sqrt(dx * dx + dy * dy)
    if dist > js_r:
        dx = dx / dist * js_r
        dy = dy / dist * js_r
    js_tx = js_cx + dx
    js_ty = js_cy + dy
    th = js_r * 0.3
    t_left = dx < -th
    t_right = dx > th
    t_up = dy < -th
    t_down = dy > th

def reset_js():
    global t_left, t_right, t_up, t_down, js_tx, js_ty, js_finger
    js_finger = None
    t_left = t_right = t_up = t_down = False
    js_tx, js_ty = js_cx, js_cy

def reset_game():
    global lost, score, life, num_fire, rel_time, last_time, finish
    global monsters, bullets, asteroids, ship
    global closing, bounce_time
    global js_finger, js_tx, js_ty, t_left, t_right, t_up, t_down
    global shoot_finger, reload_finger, last_touch_shoot

    lost = 0
    score = 0
    life = 3
    num_fire = 0
    rel_time = False
    last_time = 0
    finish = False
    closing = False
    bounce_time = 0

    js_finger = None
    js_tx, js_ty = js_cx, js_cy
    t_left = t_right = t_up = t_down = False
    shoot_finger = None
    reload_finger = None
    last_touch_shoot = 0

    lost_sound.stop()
    win_sound.stop()
    mixer.music.play()

    ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

    monsters = sprite.Group()
    for i in range(3):
        monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
        monsters.add(monster)

    asteroids = sprite.Group()
    for i in range(3):
        asteroid = Enemy('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1, 7), True)
        asteroids.add(asteroid)

    bullets = sprite.Group()

win_width = 900
win_height = 700
display.set_caption('Shooter')
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
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

rel_time = False
num_fire = 0
last_time = 0
bounce_time = 0
closing = False

button_width = 260
button_height = 70
button_x = (win_width - button_width) // 2
button_y = 420
font_button = font.Font(None, 52)

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
        elif show_touch and e.type == FINGERDOWN:
            fx = e.x * win_width
            fy = e.y * win_height
            if (fx - js_cx) ** 2 + (fy - js_cy) ** 2 <= (js_r * 1.6) ** 2:
                js_finger = e.finger_id
                update_js(fx, fy)
            if (fx - shoot_bx) ** 2 + (fy - shoot_by) ** 2 <= shoot_br ** 2:
                shoot_finger = e.finger_id
                ship.fire()
                last_touch_shoot = timer()
            if (fx - reload_bx) ** 2 + (fy - reload_by) ** 2 <= reload_br ** 2:
                reload_finger = e.finger_id
                if num_fire >= 5 and not rel_time:
                    rel_time = True
                    last_time = timer()
        elif show_touch and e.type == FINGERMOTION:
            if e.finger_id == js_finger:
                update_js(e.x * win_width, e.y * win_height)
        elif show_touch and e.type == FINGERUP:
            if e.finger_id == js_finger:
                reset_js()
            elif e.finger_id == shoot_finger:
                shoot_finger = None
            elif e.finger_id == reload_finger:
                reload_finger = None
        elif e.type == MOUSEBUTTONDOWN and e.button == 1:
            if finish and not closing:
                button_rect = Rect(button_x, button_y, button_width, button_height)
                if button_rect.collidepoint(e.pos):
                    closing = True
                    bounce_time = timer()

    if not finish:
        if show_touch and shoot_finger is not None:
            if timer() - last_touch_shoot > shoot_cooldown:
                ship.fire()
                last_touch_shoot = timer()

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
                reload_text = font2.render('Reloading... (3s)', 1, (255, 255, 255))
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
            window.blit(lose, (300, 300))
            lost_sound.play()

        if score >= 10:
            finish = True
            window.blit(win, (300, 300))
            win_sound.play()

        text = font2.render('Score: ' + str(score), 1, (225, 225, 225))
        window.blit(text, (10, 20))

        text_life = font2.render('Life: ' + str(life), 1, (225, 225, 225))
        window.blit(text_life, (10, 50))

        text_lost = font2.render('Lost: ' + str(lost), 1, (225, 225, 225))
        window.blit(text_lost, (10, 80))

        text_ammo = font2.render('Bullets: ' + str(7 - num_fire), 1, (225, 225, 225))
        window.blit(text_ammo, (10, 110))

        if show_touch:
            ui = Surface((win_width, win_height), SRCALPHA)

            draw.circle(ui, (255, 255, 255, 35), (js_cx, js_cy), js_r)
            draw.circle(ui, (255, 255, 255, 70), (js_cx, js_cy), js_r, 2)
            draw.line(ui, (255, 255, 255, 25), (js_cx - js_r + 10, js_cy), (js_cx + js_r - 10, js_cy))
            draw.line(ui, (255, 255, 255, 25), (js_cx, js_cy - js_r + 10), (js_cx, js_cy + js_r - 10))
            draw.circle(ui, (255, 255, 255, 130), (int(js_tx), int(js_ty)), 22)
            draw.circle(ui, (255, 255, 255, 170), (int(js_tx), int(js_ty)), 22, 2)

            draw.circle(ui, (255, 80, 80, 80), (shoot_bx, shoot_by), shoot_br)
            draw.circle(ui, (255, 150, 150, 110), (shoot_bx, shoot_by), shoot_br, 3)
            s_txt = font2.render('S', True, (255, 255, 255))
            ui.blit(s_txt, s_txt.get_rect(center=(shoot_bx, shoot_by)))

            draw.circle(ui, (80, 80, 255, 80), (reload_bx, reload_by), reload_br)
            draw.circle(ui, (150, 150, 255, 110), (reload_bx, reload_by), reload_br, 3)
            r_txt = font2.render('R', True, (255, 255, 255))
            ui.blit(r_txt, r_txt.get_rect(center=(reload_bx, reload_by)))

            window.blit(ui, (0, 0))

    if finish:
        if bounce_time == 0:
            bounce_time = timer()
        elapsed = timer() - bounce_time

        if elapsed < 0.5:
            decay = 1 - elapsed / 0.5
            bounce = int(cos(elapsed * 14) * decay * 5)
        else:
            bounce = 0
            if closing:
                reset_game()

    if finish:
        window.blit(background, (0, 0))
        if score >= 10:
            window.blit(win, (300, 200))
        else:
            window.blit(lose, (300, 200))

        button_rect = Rect(button_x, button_y, button_width, button_height).inflate(bounce, bounce)
        mouse_x, mouse_y = mouse.get_pos()
        hovered = button_rect.collidepoint(mouse_x, mouse_y)

        border_color = (100, 255, 100) if hovered else (50, 200, 50)
        draw.rect(window, border_color, button_rect, border_radius=15)

        fill_color = (0, 150, 0) if not hovered else (0, 210, 0)
        inner_rect = button_rect.inflate(-6, -6)
        draw.rect(window, fill_color, inner_rect, border_radius=12)

        btn_text = font_button.render('PLAY AGAIN', True, (255, 255, 255))
        text_rect = btn_text.get_rect(center=button_rect.center)
        window.blit(btn_text, text_rect)

    display.update()
    time.delay(50)
