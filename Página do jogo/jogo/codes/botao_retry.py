import pygame

class Button:
    def __init__(self, x, y, width, height, text, font_size=36, 
                 text_color=(255,255,255), button_color=(0,128,0), 
                 hover_color=(0,200,0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, screen):
        # Escolhe a cor baseado em hover
        current_color = self.hover_color if self.is_hovered else self.button_color
        
        # Desenha o botão
        pygame.draw.rect(screen, current_color, self.rect)
        pygame.draw.rect(screen, (255,255,255), self.rect, 2)  # Borda branca
        
        # Renderiza o texto
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        # Verifica se o mouse está sobre o botão
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        
        # Verifica se o botão foi clicado
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False