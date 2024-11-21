import pygame
import sys
from player import Player
import obstacle
from businessmen import Businessmen
import sys
import random
from botao_retry import Button

class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset_game()

    def reset_game(self):
        player_sprite = Player((self.screen_width / 2, self.screen_height), self.screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Configuração dos empresários com número rastreável
        self.businessmen_setup(rows=3, cols=6)
        self.total_businessmen = len(self.businessmen)
        
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.enemy_lasers = pygame.sprite.Group()

    def businessmen_setup(self, rows, cols):
        self.businessmen = pygame.sprite.Group()
        for row_index in range(rows):
            for col_index in range(cols):
                x = col_index * 70 + 50
                y = row_index * 70 + 50
                businessman = Businessmen(x, y)
                self.businessmen.add(businessman)

    def run(self, screen):
        current_time = pygame.time.get_ticks()
        
        self.player.update()

        # Verificar se todos os inimigos foram destruídos
        if len(self.businessmen) == 0:
            return "WIN"

        # Lógica de tiro dos inimigos
        for businessman in self.businessmen:
            businessman.update(current_time)
            if random.randint(1, 100) == 1:
                laser = businessman.shoot()
                if laser:
                    self.enemy_lasers.add(laser)

        # Atualizar lasers do jogador
        for laser in self.player.sprite.lasers:
            hits = pygame.sprite.spritecollide(laser, self.businessmen, True)
            if hits:
                laser.kill()
                self.score += len(hits) * 10

        # Verificar colisões de lasers inimigos com o jogador
        self.enemy_lasers.update()
        enemy_hits = pygame.sprite.spritecollide(self.player.sprite, self.enemy_lasers, True)
        if enemy_hits:
            if self.player.sprite.take_damage():
                return "GAME_OVER"

        # Desenhar elementos
        self.player.sprite.lasers.draw(screen)
        self.enemy_lasers.draw(screen)
        self.player.draw(screen)
        self.businessmen.draw(screen)

        # Renderizar pontuação e vidas
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
    pygame.display.set_caption('Space Invaders')
    clock = pygame.time.Clock()

    game = Game(screen_width, screen_height)
    game_state = "PLAYING"

    # Botões de retry para game over e vitória
    retry_button = Button(
        x=screen_width//2 - 100, 
        y=screen_height//2 + 100, 
        width=200, 
        height=50, 
        text="Retry"
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Tratamento de eventos nas telas de game over e vitória
            if game_state in ["GAME_OVER", "WIN"]:
                if retry_button.handle_event(event):
                    # Reinicia o jogo
                    game.reset_game()
                    game_state = "PLAYING"

        screen.fill((30, 30, 30))

        if game_state == "PLAYING":
            game_state = game.run(screen)
        elif game_state == "GAME_OVER":
            # Tela de Game Over
            game_over_text = pygame.font.Font(None, 74).render('GAME OVER', True, (255, 0, 0))
            score_text = pygame.font.Font(None, 36).render(f'Score: {game.score}', True, (255, 255, 255))
            
            screen.blit(game_over_text, (screen_width//2 - game_over_text.get_width()//2, screen_height//2 - 100))
            screen.blit(score_text, (screen_width//2 - score_text.get_width()//2, screen_height//2 - 30))
            
            retry_button.draw(screen)

        elif game_state == "WIN":
            # Tela de Vitória
            win_text = pygame.font.Font(None, 74).render('VOCÊ VENCEU!', True, (0, 255, 0))
            score_text = pygame.font.Font(None, 36).render(f'Score Final: {game.score}', True, (255, 255, 255))
            
            screen.blit(win_text, (screen_width//2 - win_text.get_width()//2, screen_height//2 - 100))
            screen.blit(score_text, (screen_width//2 - score_text.get_width()//2, screen_height//2 - 30))
            
            retry_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()