import pygame
import random

from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    RLEACCEL,
)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
mnozstvi = 0
Nscore = 0
r = 0
g = 0
b = 0
pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -3)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 3)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-3, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(3, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        self.rect.move_ip(0, +1)

class Enemy(pygame.sprite.Sprite, ):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("images/missile.png").convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect= self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(1, 3)
        self.a = round(random.randint(0, 2))
    def update(self):
        global mnozstvi
        if self.a == 1:
            self.rect.move_ip(-self.speed, +self.a)
        if self.a == 2:
            self.rect.move_ip(-self.speed, -self.a)
        if self.rect.right < 0 or self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0:
            mnozstvi += 1
            #print(str(mnozstvi))
            self.kill()
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("images/cloud.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH+ 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
    def update(self):
        self.rect.move_ip(-1,0)
        if self.rect.right < 0:
            self.kill()

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
ADDCLOUD = pygame.USEREVENT + 1
pygame.time.set_timer(ADDCLOUD, 1000)
ADDENEMY = pygame.USEREVENT + 2
if mnozstvi < 480:  # do 250-svetle modrá, nad 250 tmavě modrá, od 480 rudá
    pygame.time.set_timer(ADDENEMY,round((500-mnozstvi)/2))
else:
    pygame.time.set_timer(ADDENEMY, 20)

player = Player()
clouds = pygame.sprite.Group()
enemies = pygame.sprite.Group()
#all_sprites = pygame.sprite.Group()
#all_sprites.add(player)

pygame.mixer.music.load("sound/Sky_dodge_theme.ogg")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.3)

move_up_sound = pygame.mixer.Sound("sound/Jet_up.ogg")
move_down_sound = pygame.mixer.Sound("sound/Jet_down.ogg")
collision_sound = pygame.mixer.Sound("sound/Boom.ogg")

move_up_sound.set_volume(0.3)
move_down_sound.set_volume(0.3)
collision_sound.set_volume(1.0)

running = True
runningT = False

font = pygame.font.Font('freesansbold.ttf', 32)

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            #all_sprites.add(new_enemy)
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            #all_sprites.add(new_cloud)
    if Nscore < mnozstvi:
        Nscore = mnozstvi
    if mnozstvi < 250 :
        screen.fill((r, g, b))
        text = font.render("Score = " + str(mnozstvi), True, (150, 150, 150), (r, g, b))   #(135,206,250)
        text2 = font.render("Nej. score = " + str(Nscore), True, (150, 150, 150), (r, g, b))
        if r < 135:
            r += 1
        if g < 206:
            g += 1
        if b < 250:
            b += 1
    elif mnozstvi >= 250 and mnozstvi < 480:
        screen.fill((r, g, b))
        text = font.render("Score = " + str(mnozstvi), True, (150, 150, 150), (r, g, b))  #(27, 53, 194)
        text2 = font.render("Nej. score = " + str(Nscore), True, (150, 150, 150), (r, g, b))
        if r > 27:
            r -= 1
        if g > 53:
            g -= 1
        if b > 194:
            b -= 1
    elif mnozstvi >= 480:
        screen.fill((r, g, b))
        text = font.render("Score = " + str(mnozstvi), True, (150, 150, 150), (r, g, b))   #(130, 13, 13)
        text2 = font.render("Nej. score = " + str(Nscore), True, (150, 150, 150), (r, g, b))
        if r < 130:
            r += 1
        if g > 13:
            g -= 1
        if b > 13:
            b -= 1
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    clouds.update()

    textRect = text.get_rect()
    textRect = (10, 10)
    screen.blit(text, textRect)
    textRect2 = text.get_rect()
    textRect2 = (10, 50)
    screen.blit(text2, textRect2)
    '''
    surf = pygame.Surface((50,50))
    surf.fill((0,0,0))
    rect = surf.get_rect()
    surf_center = (
        (SCREEN_WIDTH-surf.get_width())/2,
        (SCREEN_HEIGHT - surf.get_height()) / 2,
    )
    '''
    #for entity in all_sprites:
    #    screen.blit(entity.surf, entity.rect)
    for entity in enemies:
        screen.blit(entity.surf, entity.rect)
    screen.blit(player.surf, player.rect)
    for entity in clouds:
        screen.blit(entity.surf, entity.rect)
    #aby mohly enemies být taky za mrakem
    if pygame.sprite.spritecollideany(player, enemies):
        screen.fill((0, 0, 0))
        text = font.render("Score je " + str(mnozstvi), True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)
        screen.blit(text, textRect)

        text2 = font.render("Nejvyssi score je " + str(Nscore), True, (255, 255, 255), (0, 0, 0))
        textRect2 = text.get_rect()
        textRect2.center = (SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 2)
        screen.blit(text2, textRect2)

        text3 = font.render("Pro pokracovani stisknete sipku nahoru", True, (255, 255, 255), (0, 0, 0))
        textRect3 = text.get_rect()
        textRect3.center = (SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2 - 50)
        screen.blit(text3, textRect3)

        pygame.time.delay(500)
        collision_sound.play()
        pygame.time.delay(500)

        pygame.display.flip()
        '''
        player.kill()
        move_up_sound.stop()
        move_down_sound.stop()
        '''
        runningT = True
        while runningT:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                        runningT = False
                        player.kill()
                        move_up_sound.stop()
                        move_down_sound.stop()
                    if event.key == K_UP:
                        runningT = False
                        enemies = ""
                        enemies = pygame.sprite.Group()
                        mnozstvi = 0
                        r = 0
                        g = 0
                        b = 0
                elif event.type == QUIT:
                    running = False
                    runningT = False
                    player.kill()
                    move_up_sound.stop()
                    move_down_sound.stop()
            #print(pressed_keys)
            clock.tick(30)
    pygame.display.flip()
    clock.tick(30)
pygame.mixer.music.stop()
pygame.mixer.quit()