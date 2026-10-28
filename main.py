
import pygame
import random

pygame.init()
screen = pygame.display.set_mode((600, 700))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

player = pygame.Rect(280, 620, 40, 40)
bullets = []
enemies = []
score = 0
font = pygame.font.SysFont(None, 35)
game_over = False

running = True

while running:
    screen.fill((10, 10, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bullets.append(
                    pygame.Rect(player.centerx - 3, player.top, 6, 15)
                )

            if event.key == pygame.K_r and game_over:
                player.x = 280
                bullets.clear()
                enemies.clear()
                score = 0
                game_over = False

    if not game_over:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= 5
        if keys[pygame.K_RIGHT] and player.right < 600:
            player.x += 5

        if random.randint(1, 30) == 1:
            enemies.append(
                pygame.Rect(random.randint(0, 565), 0, 35, 35)
            )

        for bullet in bullets[:]:
            bullet.y -= 7
            if bullet.bottom < 0:
                bullets.remove(bullet)

        for enemy in enemies[:]:
            enemy.y += 3

            if enemy.colliderect(player):
                game_over = True
                break

            if enemy.top > 700:
                enemies.remove(enemy)
                continue

            for bullet in bullets[:]:
                if enemy.colliderect(bullet):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 1
                    break

        if game_over:
            enemies.clear()
            bullets.clear()

    pygame.draw.rect(screen, (0, 220, 255), player)

    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 0), bullet)

    for enemy in enemies:
        pygame.draw.rect(screen, (255, 60, 80), enemy)

    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    if game_over:
        title = font.render("GAME OVER!", True, (255, 60, 80))
        restart = font.render("Press R to restart", True, (255, 255, 255))
        screen.blit(title, (220, 300))
        screen.blit(restart, (190, 345))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
