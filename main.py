import pygame
import os

pygame.init()

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


# Draws the characters and background
def draw_window(wiz, gob, missiles):
    WINDOW.fill(BACKCOLOR)
    pygame.draw.rect(WINDOW, (0, 0, 0), BORDERONE)
    pygame.draw.rect(WINDOW, (0, 0, 0), BORDERTWO)
    pygame.draw.rect(WINDOW, (0, 0, 0), BORDERTHREE)
    pygame.draw.rect(WINDOW, (0, 0, 0), BORDERFOUR)
    WINDOW.blit(WIZARD, (wiz.x, wiz.y))
    WINDOW.blit(GOBLIN, (gob.x, gob.y))

    for shot in missiles:
        pygame.draw.rect(WINDOW, (0, 89, 200), shot)

    pygame.display.update()


# WASD controls for the wizard
def controls(keys_pressed, wiz):
    if keys_pressed[pygame.K_w] and wiz.y - SPEED > 0:
        wiz.y -= SPEED
    if keys_pressed[pygame.K_s] and wiz.y + SPEED + wiz.height < HEIGHT:
        wiz.y += SPEED
    if keys_pressed[pygame.K_a] and wiz.x - SPEED > 0:
        wiz.x -= SPEED
    if keys_pressed[pygame.K_d] and wiz.x + SPEED + wiz.width < WIDTH:
        wiz.x += SPEED


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

        keys_pressed = pygame.key.get_pressed()
        controls(keys_pressed, wiz)
        handle_missiles(missiles, wiz, gob)

        draw_window(wiz, gob, missiles)

    pygame.quit()


if __name__ == "__main__":
    main()
