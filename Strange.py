import pygame
import os
import random

pygame.init()
pygame.font.init()

fontSize = 60
myfont = pygame.font.SysFont('Calibri', fontSize, True)

# Character trait base stats
health = 10
ability_power = 10
defense = 10

# Stack
top = -1
spellStack = []

# Window size
WIDTH = 1366
HEIGHT = 768
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# Window title
pygame.display.set_caption("Strange")

BORDERONE = pygame.Rect(0, 0, 5, HEIGHT + 100)
BORDERTWO = pygame.Rect(0, HEIGHT - 5, WIDTH, 5)
BORDERTHREE = pygame.Rect(WIDTH - 5, 0, 5, HEIGHT + 100)
BORDERFOUR = pygame.Rect(0, 0, WIDTH, 5)

# FPS constant
FPS = 60

# Speed constant for character movement
SPEED = 5

# Events of collisions
GOB_HIT = pygame.USEREVENT + 1
BORDER_HIT = pygame.USEREVENT + 2

# Constants for magic missile
MISSILEVELOCITY = 10
MAXINPUTS = 2

# Change RGB values for the background color
BACKGROUND = pygame.image.load(os.path.join('Assets', 'background.jpg'))


# Wizard class and sprite group
class WIZARD(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.missileFire = pygame.mixer.Sound(os.path.join('Assets', 'missile.wav'))

    def shoot(self):
        self.missileFire.play()


wizard = WIZARD(os.path.join('Assets', 'wizardSmall.png'))
WIZARD_group = pygame.sprite.Group()
WIZARD_group.add(wizard)


# Goblin class and sprite group
class GOBLIN(pygame.sprite.Sprite):
    def __init__(self, image_path, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]


GOBLIN_group = pygame.sprite.Group()
for goblin in range(4):
    new_goblin = GOBLIN(os.path.join('Assets', 'goblinSmall.png'), random.randrange(0, WIDTH), random.randrange(0, HEIGHT))
    GOBLIN_group.add(new_goblin)


# Draws the characters and background
def draw_window(wiz, missiles, spells):
    WINDOW.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WINDOW, (0, 0, 0), BORDERONE)
    pygame.draw.rect(WINDOW, (0, 0, 0), BORDERTWO)
    pygame.draw.rect(WINDOW, (0, 0, 0), BORDERTHREE)
    pygame.draw.rect(WINDOW, (0, 0, 0), BORDERFOUR)
    GOBLIN_group.draw(WINDOW)
    WIZARD_group.draw(WINDOW)
    pygame.mouse.set_visible(False)
    textsurface = myfont.render('STACK: ' + ''.join(spellStack), False, (0, 0, 0))
    WINDOW.blit(textsurface,(fontSize,HEIGHT-fontSize))

    if len(spellStack) == 3:
        spellString = get_spell(''.join(spellStack), wiz).name
        spellText = myfont.render(spellString, False, (0, 0, 0))
        WINDOW.blit(spellText, (200, 200))

    for shot in missiles:
        pygame.draw.rect(WINDOW, (200, 0, 0), shot)
    pygame.display.update()

    for shot in spells:
        shot.getShape()


class Spell:
    def __init__(self, name, stat, x, y):
        self.name = name
        self.stat = stat
        self.x = x
        self.y = y

    def getShape(self):
        if self.name == 'Fireball':
            return pygame.draw.circle(WINDOW,(230,20,0),(self.x,self.y),15)
        elif self.name == 'Sonic Blast':
            return pygame.draw.circle(WINDOW,(50, 168, 166),(self.x,self.y),15)
        elif self.name == 'Heal':
            return
        elif self.name == 'Cosmic Drain':
            return
        elif self.name == 'Shield':
            return
        elif self.name == 'Thorns':
            return


# WASD controls for the wizard
def controls(keys_pressed, wiz, top):
    if keys_pressed[pygame.K_w] and wiz.rect.y - SPEED > 0:
        wiz.rect.y -= SPEED
    if keys_pressed[pygame.K_s] and wiz.rect.y + SPEED + wiz.rect.height < HEIGHT:
        wiz.rect.y += SPEED
    if keys_pressed[pygame.K_a] and wiz.rect.x - SPEED > 0:
        wiz.rect.x -= SPEED
    if keys_pressed[pygame.K_d] and wiz.rect.x + SPEED + wiz.rect.width < WIDTH:
        wiz.rect.x += SPEED

    if keys_pressed[pygame.K_j] and len(spellStack) < 3 and spellStack.count('j') < 1:
        top += 1
        spellStack.append('j')

    if keys_pressed[pygame.K_k] and len(spellStack) < 3 and spellStack.count('k') < 1:
        top += 1
        spellStack.append('k')

    if keys_pressed[pygame.K_l] and len(spellStack) < 3 and spellStack.count('l') < 1:
        top += 1
        spellStack.append('l')


# Goblin moves towards player location
def enemy_movement(wiz, gob):
    follow_x = wiz.rect.x + (wiz.rect.width/2)
    follow_y = wiz.rect.y + (wiz.rect.height/2)
    goblin_x = gob.rect.x
    goblin_y = gob.rect.y

    dx, dy = (follow_x - goblin_x, follow_y - goblin_y)
    stepx, stepy = (dx/60., dy/60.)
    gob.rect.x += stepx
    gob.rect.y += stepy


def handle_missiles(missiles, gob):
    for shots in missiles:
        shots.x += MISSILEVELOCITY
        if gob.rect.colliderect(shots):
            pygame.event.post(pygame.event.Event(GOB_HIT))
            missiles.remove(shots)
        if BORDERONE.rect.colliderect(shots):
            pygame.event.post(pygame.event.Event(BORDER_HIT))
            missiles.remove(shots)
        if BORDERTWO.rect.colliderect(shots):
            pygame.event.post(pygame.event.Event(BORDER_HIT))
            missiles.remove(shots)
        if BORDERTHREE.rect.colliderect(shots):
            pygame.event.post(pygame.event.Event(BORDER_HIT))
            missiles.remove(shots)
        if BORDERFOUR.rect.colliderect(shots):
            pygame.event.post(pygame.event.Event(BORDER_HIT))
            missiles.remove(shots)


def handle_spells(spells, wiz):
    for shots in spells:
        shots.x += MISSILEVELOCITY


# Returns the stat to be used in spell calculation
def get_stat(type):
    x = 0
    y = 0
    z = 0
    if type == "hp":
        x = 2
        y = .25
        z = .25
        hp = (health * x) + (ability_power * y) + (defense * z)
        return hp
    elif type == "ap":
        x = 1.5
        y = .375
        z = .125
        ap = (ability_power * x) + (health * y) + (defense * z)
        return ap
    elif type == "df":
        x = .1
        y = .075
        z = .025
        df = (defense * x) + (health * y) + (ability_power * z)
        return df


# Returns the spell to be cast
def get_spell(cast, wiz):
    if cast == "jkl":
        stat = get_stat("hp")
        spellcast = Spell("Heal", stat, wiz.x + wiz.width, wiz.y + wiz.height//2)
        return spellcast
    elif cast == "jlk":
        stat = get_stat("hp") / 2
        spellcast = Spell("Cosmic Drain", stat, wiz.x + wiz.width, wiz.y + wiz.height//2)
        return spellcast
    elif cast == "kjl":
        stat = get_stat("ap") * 1.2
        spellcast = Spell("Sonic Blast", stat, wiz.x + wiz.width, wiz.y + wiz.height//2)
        return spellcast
    elif cast == "klj":
        stat = get_stat("ap") * 2
        spellcast = Spell("Fireball", stat, wiz.x + wiz.width, wiz.y + wiz.height//2)
        return spellcast
    elif cast == "ljk":
        stat = get_stat("df")
        spellcast = Spell("Shield", stat, wiz.x + wiz.width, wiz.y + wiz.height//2)
        return spellcast
    elif cast == "lkj":
        stat = get_stat("df") * 25
        spellcast = Spell("Thorns", stat, wiz.x + wiz.width, wiz.y + wiz.height//2)
        return spellcast


def main():
    missiles = []
    spellsOut = []

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and len(missiles) < MAXINPUTS:
                missile = pygame.Rect(wizard.rect.x + wizard.rect.width, wizard.rect.y + wizard.rect.height // 2, 10, 5)
                missiles.append(missile)
                if (''.join(spellStack) == 'klj'):
                    spellCast = Spell('Fireball', 5, wizard.x + wizard.width, wizard.y + wizard.height // 2)
                    spellsOut.append(spellCast)
                spellStack.clear()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.display.update()
                WINDOW.fill((0, 0, 0))
                font = pygame.font.Font('freesansbold.ttf', 32)
                text = font.render('GAME OVER', True, (0, 255, 0))
                textRect = text.get_rect()
                textRect.center = (WIDTH // 2, HEIGHT // 2)
                WINDOW.blit(text, textRect)
                pygame.display.update()
                pygame.time.wait(5000)
                run = False

        enemy_movement(wizard, new_goblin)
        keys_pressed = pygame.key.get_pressed()
        controls(keys_pressed, wizard, top)
        handle_missiles(missiles, new_goblin)
        handle_spells(spellsOut, wizard)

        draw_window(wizard, missiles, spellsOut)

    pygame.quit()


if __name__ == "__main__":
    main()