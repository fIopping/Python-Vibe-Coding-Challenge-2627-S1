import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from main import (
    create_bullet,
    move_bullets,
    move_enemies,
    move_player,
    spawn_enemy,
)


class GameplayTests(unittest.TestCase):
    def test_player_moves_at_constant_speed_and_stays_on_screen(self):
        player = pygame.Rect(280, 620, 40, 40)
        position_x = float(player.x)

        position_x = move_player(player, position_x, False, True, 1)
        self.assertEqual(player.x, 560)

        position_x = move_player(player, position_x, True, False, 1)
        self.assertEqual(player.x, 260)

    def test_player_speed_is_consistent_across_frame_rates(self):
        positions = []
        for frame_count in (45, 60):
            player = pygame.Rect(100, 620, 40, 40)
            position_x = float(player.x)
            for _ in range(frame_count):
                position_x = move_player(
                    player, position_x, False, True, 1 / frame_count
                )
            positions.append(position_x)

        for position in positions:
            self.assertAlmostEqual(position, 400)

    def test_bullets_move_and_are_removed_after_leaving_screen(self):
        player = pygame.Rect(100, 20, 40, 40)
        bullet = create_bullet(player)
        bullet["y"] = 20
        bullet["rect"].y = 20
        bullets = [bullet]

        move_bullets(bullets, 1)

        self.assertEqual(bullets, [])

    def test_bullet_and_enemy_speed_are_consistent_across_frame_rates(self):
        for frame_count in (45, 60):
            bullet = {"rect": pygame.Rect(100, 500, 6, 15), "y": 500.0}
            enemy = {
                "rect": pygame.Rect(100, 0, 35, 35),
                "y": 0.0,
                "is_puppy": False,
            }

            for _ in range(frame_count):
                move_bullets([bullet], 1 / frame_count)
                move_enemies([enemy], 1 / frame_count)

            self.assertAlmostEqual(bullet["y"], 80)
            self.assertAlmostEqual(enemy["y"], 180)

    def test_spawned_enemy_fits_inside_playfield(self):
        enemy = spawn_enemy()

        self.assertGreaterEqual(enemy["rect"].left, 0)
        self.assertLessEqual(enemy["rect"].right, 600)
        self.assertIsInstance(enemy["is_puppy"], bool)


if __name__ == "__main__":
    unittest.main()
