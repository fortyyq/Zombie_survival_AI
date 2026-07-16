import pygame
import sys
import cv2

from settings import *
from player import Player
from zombie import Zombie
from bullet import Bullet
from hand_detector import HandDetector

pygame.init()
pygame.mixer.init()

# Sounds
gun_sound = pygame.mixer.Sound("sounds/gun.mp3")
explosion_sound = pygame.mixer.Sound("sounds/explosion.mp3")

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival AI")

# Background
background = pygame.image.load("images/bg.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Heart Image
heart_img = pygame.image.load("images/heart.png").convert_alpha()
heart_img = pygame.transform.scale(heart_img, (30, 30))

clock = pygame.time.Clock()

# Camera
cap = cv2.VideoCapture(0)
detector = HandDetector()

# Player
player = Player()

# Zombies
zombies = [
    Zombie(),
    Zombie(),
    Zombie()
]

# Bullet
bullet = Bullet()

# Game Variables
score = 0
lives = 3

# High Score
try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
except:
    high_score = 0

font = pygame.font.SysFont(None, 40)

menu = True
running = True
# ==========================
# START MENU
# ==========================

while running and menu:

    screen.blit(background, (0, 0))

    title = font.render("ZOMBIE SURVIVAL AI", True, RED)
    start = font.render("Press SPACE to Start", True, BLACK)
    exit_game = font.render("Press ESC to Exit", True, BLACK)

    screen.blit(title, (WIDTH//2 - 170, HEIGHT//2 - 60))
    screen.blit(start, (WIDTH//2 - 170, HEIGHT//2))
    screen.blit(exit_game, (WIDTH//2 - 170, HEIGHT//2 + 40))

    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            menu = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                menu = False

            elif event.key == pygame.K_ESCAPE:
                running = False
                menu = False


# ==========================
# MAIN GAME LOOP
# ==========================

while running:

    # Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Camera
    success, frame = cap.read()

    if success:

        frame = cv2.flip(frame, 1)

        frame, lmList = detector.findHands(frame)

        x = detector.getHandX(lmList)

        if x is not None:
            player.move(x)

        if len(lmList) != 0:

            fingers = detector.fingersUp(lmList)

            if fingers == [0, 1, 0, 0, 0]:

                if not bullet.active:
                    bullet.shoot(player)
                    gun_sound.play()

        cv2.imshow("Camera", frame)
        cv2.waitKey(1)
        # ==========================
    # Move Zombies
    # ==========================

    for zombie in zombies:

        zombie.move()

        # Zombie reached bottom
        if zombie.y > HEIGHT:
            lives -= 1
            zombie.reset()

        # Zombie touched player
        if (
            zombie.x < player.x + player.width
            and zombie.x + zombie.width > player.x
            and zombie.y < player.y + player.height
            and zombie.y + zombie.height > player.y
        ):
            lives -= 1
            zombie.reset()

    # ==========================
    # Move Bullet
    # ==========================

    bullet.move()

    # ==========================
    # Bullet Collision
    # ==========================

    if bullet.active:

        for zombie in zombies:

            if (
                bullet.x < zombie.x + zombie.width
                and bullet.x + bullet.width > zombie.x
                and bullet.y < zombie.y + zombie.height
                and bullet.y + bullet.height > zombie.y
            ):

                score += 1

                # High Score Save
                if score > high_score:

                    high_score = score

                    with open("highscore.txt", "w") as file:
                        file.write(str(high_score))

                bullet.active = False
                explosion_sound.play()

                zombie.reset()
                break
            # ==========================
    # Draw Background
    # ==========================

    screen.blit(background, (0, 0))

    # Zombies
    for zombie in zombies:
        zombie.draw(screen)

    # Player
    player.draw(screen)

    # Bullet
    bullet.draw(screen)

    # Score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (20, 20))

    # High Score
    high_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(high_text, (20, 60))

    # Lives Text
    lives_text = font.render("Lives:", True, RED)
    screen.blit(lives_text, (20, 100))

    # Heart Images
    for i in range(lives):
        screen.blit(heart_img, (130 + i * 35, 95))

    # ==========================
    # Game Over
    # ==========================

    if lives <= 0:

        waiting = True

        while waiting:

            screen.blit(background, (0, 0))

            game_over = font.render("GAME OVER", True, RED)
            restart = font.render("Press R to Restart", True, BLACK)
            exit_game = font.render("Press ESC to Exit", True, BLACK)

            screen.blit(game_over, (WIDTH//2 - 140, HEIGHT//2 - 40))
            screen.blit(restart, (WIDTH//2 - 150, HEIGHT//2 + 10))
            screen.blit(exit_game, (WIDTH//2 - 150, HEIGHT//2 + 50))

            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    waiting = False
                    running = False

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_r:

                        score = 0
                        lives = 3

                        try:
                            with open("highscore.txt", "r") as file:
                                high_score = int(file.read())
                        except:
                            high_score = 0

                        bullet.active = False

                        player = Player()

                        zombies = [
                            Zombie(),
                            Zombie(),
                            Zombie()
                        ]

                        waiting = False

                    elif event.key == pygame.K_ESCAPE:
                        waiting = False
                        running = False

    pygame.display.flip()
    clock.tick(FPS)

# ==========================
# Close Game
# ==========================

cap.release()
cv2.destroyAllWindows()

pygame.quit()
sys.exit()