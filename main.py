import pygame
import os

pygame.init()
pygame.font.init()

fontSize = 60
myfont = pygame.font.SysFont('Calibri', fontSize, True)

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
BACKCOLOR = (255, 225, 255)

# Wizard image loading and transforming
WIZARDWidth = 80
WIZARDHeight = 80
WIZARD = pygame.image.load(os.path.join('Assets', 'wizardPlaceholder.png'))
WIZARD = pygame.transform.scale(WIZARD, (WIZARDWidth, WIZARDHeight))
WIZARD = pygame.transform.rotate(WIZARD, 0)

# Goblin image loading and transforming
GOBLINWidth = 60
GOBLINHeight = 100
GOBLIN = pygame.image.load(os.path.join('Assets', 'goblin.png'))
GOBLIN = pygame.transform.scale(GOBLIN, (GOBLINWidth, GOBLINHeight))

# Character trait stats
health = 10
ability_power = 10
defense = 10

# Draws the characters and background
def draw_window(wiz, gob, missiles):
    WINDOW.fill(BACKCOLOR)
    pygame.draw.rect(WINDOW, (0, 0, 0), BORDERONE)
    pygame.draw.rect(WINDOW, (0, 0, 0), BORDERTWO)
    pygame.draw.rect(WINDOW, (0, 0, 0), BORDERTHREE)
    pygame.draw.rect(WINDOW, (0, 0, 0), BORDERFOUR)
    WINDOW.blit(WIZARD, (wiz.x, wiz.y))
    WINDOW.blit(GOBLIN, (gob.x, gob.y))
    textsurface = myfont.render('STACK: ' + ''.join(spellStack), False, (0, 0, 0))
    WINDOW.blit(textsurface, (fontSize, HEIGHT - fontSize))

    for shot in missiles:
        pygame.draw.rect(WINDOW, (0, 89, 200), shot)

    pygame.display.update()


top = -1
spellStack = []
spellsOut = []


class spells():
    def __init__(self, name, stat):
        self.name = name
        self.stat = stat

    def cast(self):
        spellsOut.append(self)

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

# WASD controls for the wizard
def controls(keys_pressed, wiz, top):
    if keys_pressed[pygame.K_w] and wiz.y - SPEED > 0:
        wiz.y -= SPEED
    if keys_pressed[pygame.K_s] and wiz.y + SPEED + wiz.height < HEIGHT:
        wiz.y += SPEED
    if keys_pressed[pygame.K_a] and wiz.x - SPEED > 0:
        wiz.x -= SPEED
    if keys_pressed[pygame.K_d] and wiz.x + SPEED + wiz.width < WIDTH:
        wiz.x += SPEED

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
    follow_x = wiz.x + (WIZARDWidth / 2)
    follow_y = wiz.y + (WIZARDHeight / 2)
    goblin_x = gob.x
    goblin_y = gob.y

    dx, dy = (follow_x - goblin_x, follow_y - goblin_y)
    stepx, stepy = (dx / 60., dy / 60.)
    gob.x += stepx
    gob.y += stepy


def handle_missiles(missiles, wiz, gob):
    for shots in missiles:
        shots.x += MISSILEVELOCITY
        if gob.colliderect(shots):
            pygame.event.post(pygame.event.Event(GOB_HIT))
            missiles.remove(shots)
        if BORDERONE.colliderect(shots):
            pygame.event.post(pygame.event.Event(BORDER_HIT))
            missiles.remove(shots)
        if BORDERTWO.colliderect(shots):
            pygame.event.post(pygame.event.Event(BORDER_HIT))
            missiles.remove(shots)
        if BORDERTHREE.colliderect(shots):
            pygame.event.post(pygame.event.Event(BORDER_HIT))
            missiles.remove(shots)
        if BORDERFOUR.colliderect(shots):
            pygame.event.post(pygame.event.Event(BORDER_HIT))
            missiles.remove(shots)


def main():
    wiz = pygame.Rect(WIDTH / 2, HEIGHT / 2, WIZARDWidth, WIZARDHeight)
    gob = pygame.Rect(WIDTH - 800, HEIGHT - 400, GOBLINWidth, GOBLINHeight)

    missiles = []

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and len(missiles) < MAXINPUTS:
                missile = pygame.Rect(wiz.x + wiz.width, wiz.y + wiz.height // 2, 10, 5)
                missiles.append(missile)
                spellStack.clear()

        enemy_movement(wiz, gob)
        keys_pressed = pygame.key.get_pressed()
        controls(keys_pressed, wiz, top)
        handle_missiles(missiles, wiz, gob)

        draw_window(wiz, gob, missiles)

    pygame.quit()


if __name__ == "__main__":
    main()