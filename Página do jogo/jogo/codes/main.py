import pygame
import sys
from player import Player
from businessmen import Businessmen
from inimigo2 import TechBro
from inimigo3 import StartupCEO
import random
from botao_retry import Button

class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Carrega e configura o background
        self.background = pygame.image.load('./graphics/fundo.jpg').convert()  # Adicione sua imagem de fundo aqui
        # Redimensiona a imagem para o tamanho da tela
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        
        self.reset_game()

    def reset_game(self):
        player_sprite = Player((self.screen_width / 2, self.screen_height), self.screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        self.all_enemies = pygame.sprite.Group()
        self.setup_enemies()
        
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.enemy_lasers = pygame.sprite.Group()

    def setup_enemies(self):
        # Configuração para 3 linhas de inimigos diferentes
        # Primeira linha: Businessmen
        for i in range(3):
            x = i * 150 + 100  # Espaçamento horizontal
            y = 50  # Primeira linha
            businessman = Businessmen(x, y)
            self.all_enemies.add(businessman)

        # Segunda linha: TechBros
        for i in range(3):
            x = i * 150 + 100
            y = 150  # Segunda linha
            techbro = TechBro(x, y)
            self.all_enemies.add(techbro)

        # Terceira linha: StartupCEOs
        for i in range(3):
            x = i * 150 + 100
            y = 250  # Terceira linha
            ceo = StartupCEO(x, y)
            self.all_enemies.add(ceo)

    def run(self, screen):
        # Desenha o background primeiro
        screen.blit(self.background, (0, 0))
        
        current_time = pygame.time.get_ticks()
        
        self.player.update()

        if len(self.all_enemies) == 0:
            return "WIN"

        for enemy in self.all_enemies:
            enemy.update(current_time)
            if random.randint(1, 100) == 1:
                laser = enemy.shoot(current_time)
                if laser:
                    self.enemy_lasers.add(laser)

        for laser in self.player.sprite.lasers:
            hits = pygame.sprite.spritecollide(laser, self.all_enemies, True)
            if hits:
                laser.kill()
                self.score += len(hits) * 10

        self.enemy_lasers.update()
        enemy_hits = pygame.sprite.spritecollide(self.player.sprite, self.enemy_lasers, True)
        if enemy_hits:
            if self.player.sprite.take_damage():
                return "GAME_OVER"

        self.player.sprite.lasers.draw(screen)
        self.enemy_lasers.draw(screen)
        self.player.draw(screen)
        self.all_enemies.draw(screen)

        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        lives_text = self.font.render(f'Lives: {self.player.sprite.lives}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

        return "PLAYING"

def main():
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Steve contra os empresários')
    clock = pygame.time.Clock()

    game = Game(screen_width, screen_height)
    game_state = "PLAYING"

    retry_button = Button(
        x=screen_width // 2 - 100, 
        y=screen_height // 2 + 100, 
        width=200, 
        height=50, 
        text="Retry"
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state in ["GAME_OVER", "WIN"]:
                if retry_button.handle_event(event):
                    game.reset_game()
                    game_state = "PLAYING"

        if game_state == "PLAYING":
            screen.blit(game.background, (0, 0))  # Desenha o background antes de tudo
            game_state = game.run(screen)
        elif game_state == "GAME_OVER":
            screen.blit(game.background, (0, 0))  # Mantém o background mesmo na tela de game over
            game_over_text = pygame.font.Font(None, 74).render('GAME OVER', True, (255, 0, 0))
            score_text = pygame.font.Font(None, 36).render(f'Score: {game.score}', True, (255, 255, 255))
            
            screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 100))
            screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 - 30))
            
            retry_button.draw(screen)

        elif game_state == "WIN":
            screen.blit(game.background, (0, 0))  # Mantém o background mesmo na tela de vitória
            win_text = pygame.font.Font(None, 74).render('VOCÊ VENCEU!', True, (0, 255, 0))
            score_text = pygame.font.Font(None, 36).render(f'Score Final: {game.score}', True, (255, 255, 255))
            
            screen.blit(win_text, (screen_width // 2 - win_text.get_width() // 2, screen_height // 2 - 100))
            screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 - 30))
            
            retry_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()