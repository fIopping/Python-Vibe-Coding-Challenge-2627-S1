import os
import random

import pygame


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
PLAYER_SPEED = 300
BULLET_SPEED = 420
ENEMY_SPEED = 180
ENEMY_SPAWN_INTERVAL = 0.5
FIRE_INTERVAL = 0.22


def move_player(player, position_x, move_left, move_right, delta_time):
    direction = int(move_right) - int(move_left)
    position_x = max(
        0,
        min(SCREEN_WIDTH - player.width, position_x + direction * PLAYER_SPEED * delta_time),
    )
    player.x = round(position_x)
    return position_x


def move_bullets(bullets, delta_time):
    for bullet in bullets:
        bullet["y"] -= BULLET_SPEED * delta_time
        bullet["rect"].y = round(bullet["y"])
    bullets[:] = [bullet for bullet in bullets if bullet["rect"].bottom >= 0]


def move_enemies(enemies, delta_time):
    for enemy in enemies:
        enemy["y"] += ENEMY_SPEED * delta_time
        enemy["rect"].y = round(enemy["y"])


def create_bullet(player):
    rect = pygame.Rect(player.centerx - 3, player.top, 6, 15)
    return {"rect": rect, "y": float(rect.y)}


def spawn_enemy():
    return {
        "rect": pygame.Rect(random.randint(0, SCREEN_WIDTH - 35), 0, 35, 35),
        "y": 0.0,
        "is_puppy": random.randint(1, 12) == 1,
    }


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Shooter")
    clock = pygame.time.Clock()

    player = pygame.Rect(280, 620, 40, 40)
    player_x = float(player.x)
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

    spawn_timer = ENEMY_SPAWN_INTERVAL
    fire_timer = 0
    running = True

    while running:
        delta_time = min(clock.tick(60) / 1000, 0.05)
        screen.fill((10, 10, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    player.x = 280
                    player_x = float(player.x)
                    bullets.clear()
                    enemies.clear()
                    score = 0
                    game_over = False
                    puppy_was_hit = False
                    spawn_timer = ENEMY_SPAWN_INTERVAL
                    fire_timer = 0

        if not game_over:
            keys = pygame.key.get_pressed()
            player_x = move_player(
                player,
                player_x,
                keys[pygame.K_LEFT],
                keys[pygame.K_RIGHT],
                delta_time,
            )

            fire_timer = max(0, fire_timer - delta_time)
            if keys[pygame.K_SPACE] and fire_timer == 0:
                bullets.append(create_bullet(player))
                fire_timer = FIRE_INTERVAL

            spawn_timer -= delta_time
            if spawn_timer <= 0:
                enemies.append(spawn_enemy())
                spawn_timer += ENEMY_SPAWN_INTERVAL

            move_bullets(bullets, delta_time)
            move_enemies(enemies, delta_time)

            for enemy in enemies[:]:
                enemy_rect = enemy["rect"]

                if enemy_rect.colliderect(player):
                    game_over = True
                    break

                if enemy_rect.top > SCREEN_HEIGHT:
                    enemies.remove(enemy)
                    continue

                for bullet in bullets[:]:
                    if enemy_rect.colliderect(bullet["rect"]):
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
            pygame.draw.rect(screen, (255, 255, 0), bullet["rect"])

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

    pygame.quit()


if __name__ == "__main__":
    main()
