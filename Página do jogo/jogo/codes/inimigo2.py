import pygame
from enemy_laser import EnemyLaser
from math import sin

class TechBro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        file_path = './graphics/blue.png'  # Sugiro que tenha uma imagem para este inimigo
        original_image = pygame.image.load(file_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, (100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_x = 3
        self.speed_y = 0.5
        self.direction = 1
        self.last_move_time = pygame.time.get_ticks()
        self.can_shoot = True

    def update(self, current_time):
        # Movimento em zigue-zague
        self.rect.x += self.speed_x * self.direction
        self.rect.y += self.speed_y

        # Inverte direção nas bordas
        if self.rect.right >= 600 or self.rect.left <= 0:
            self.direction *= -1
            self.rect.y += 30  # Desce mais rápido

    def shoot(self, current_time):
     cooldown = 2000  # Tempo entre tiros em milissegundos (2 segundos)
     if current_time - self.last_shot_time >= cooldown:  # Verifica o cooldown
        self.last_shot_time = current_time
        return EnemyLaser(self.rect.center, 5)
     return None
