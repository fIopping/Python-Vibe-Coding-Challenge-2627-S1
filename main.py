
import os
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
puppy_was_hit = False

asset_dir = os.path.join(os.path.dirname(__file__), "assets")
puppy_source = pygame.image.load(os.path.join(asset_dir, "puppy.jpg")).convert()
crop_size = min(puppy_source.get_size())
puppy_crop = puppy_source.subsurface(pygame.Rect(0, 0, crop_size, crop_size))
puppy_image = pygame.transform.smoothscale(puppy_crop, (35, 35))

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
                puppy_was_hit = False

    if not game_over:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= 5
        if keys[pygame.K_RIGHT] and player.right < 600:
            player.x += 5

        if random.randint(1, 30) == 1:
            is_puppy = random.randint(1, 12) == 1
            enemies.append({
                "rect": pygame.Rect(random.randint(0, 565), 0, 35, 35),
                "is_puppy": is_puppy,
            })

        for bullet in bullets[:]:
            bullet.y -= 7
            if bullet.bottom < 0:
                bullets.remove(bullet)

        for enemy in enemies[:]:
            enemy_rect = enemy["rect"]
            enemy_rect.y += 3

            if enemy_rect.colliderect(player):
                game_over = True
                break

            if enemy_rect.top > 700:
                enemies.remove(enemy)
                continue

            for bullet in bullets[:]:
                if enemy_rect.colliderect(bullet):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    if enemy["is_puppy"]:
                        puppy_was_hit = True
                        game_over = True
                    else:
                        score += 1
                    break

            if game_over:
                break

        if game_over:
            enemies.clear()
            bullets.clear()

    pygame.draw.rect(screen, (0, 220, 255), player)

    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 0), bullet)

    for enemy in enemies:
        if enemy["is_puppy"]:
            screen.blit(puppy_image, enemy["rect"])
        else:
            pygame.draw.rect(screen, (255, 60, 80), enemy["rect"])

    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    if game_over:
        message = "You shot a helpless puppy" if puppy_was_hit else "GAME OVER!"
        title = font.render(message, True, (255, 60, 80))
        restart = font.render("Press R to restart", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(300, 300)))
        screen.blit(restart, (190, 345))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
