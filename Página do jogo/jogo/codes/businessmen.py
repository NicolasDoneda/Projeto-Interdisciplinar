import pygame
from enemy_laser import EnemyLaser

class Businessmen(pygame.sprite.Sprite):
    def __init__(self, x, y, delay=10):
        super().__init__()
        file_path = './graphics/red.png'
        original_image = pygame.image.load(file_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, (100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2
        self.last_move_time = pygame.time.get_ticks()
        self.delay = delay
        self.can_shoot = True
        self.shoot_cooldown = 1000  # Alterado para 1 segundo e meio
        self.last_shot_time = pygame.time.get_ticks()

    def update(self, current_time):
        if current_time - self.last_move_time >= self.delay:
            self.rect.x += self.speed

        # Muda a direção ao tocar na borda
        if self.rect.right >= 600 or self.rect.left <= 0:
            self.speed *= -1
            self.rect.y += 20  # Desce uma linha
        self.last_move_time = current_time

    def shoot(self, current_time):
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            self.last_shot_time = current_time
            return EnemyLaser(self.rect.center, 5)
        return None