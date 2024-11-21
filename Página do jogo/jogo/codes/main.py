import pygame
import sys
from player import Player
import obstacle
from businessmen import Businessmen

pygame.init()

class Game:
    def __init__(self):
        # Configuração do player
        player_sprite = Player((screen_width / 2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

      # Configuração dos empresários
        self.businessmen_setup(rows=3, cols=6)
       

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
        

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def businessmen_setup(self, rows, cols):
        self.businessmen = pygame.sprite.Group()  # Grupo para armazenar os empresários
        for row_index in range(rows):
            for col_index in range(cols):
                x = col_index * 70 + 50  # Ajuste de espaçamento entre sprites de empresários
                y = row_index * 70 + 50  # Ajuste de espaçamento entre linhas
            businessman = Businessmen(x, y)  # Cria um empresário
            self.businessmen.add(businessman)  # Adiciona ao grupo


    def run(self):
        self.player.update()
        self.player.sprite.lasers.update()

        # Verificar colisões
        for laser in self.player.sprite.lasers:
            hit = pygame.sprite.spritecollide(laser, self.businessmen, True)  # Remove empresários atingidos
            if hit:
                laser.kill()

        # Atualizar e desenhar sprites
        self.businessmen.update()
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.businessmen.draw(screen)

        

if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((30, 30, 30))
        game.run()
        pygame.display.flip()
        clock.tick(60)
