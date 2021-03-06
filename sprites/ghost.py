import pygame
import random

from assets import GHOST_IMG
from settings import HEIGHT, TILESIZE, WIDTH

# Criando a classe dos fantasmas
class Ghost(pygame.sprite.Sprite):
    def __init__(self, assets, x, y, all_walls = []):
        pygame.sprite.Sprite.__init__(self)

        self.all_walls = all_walls

        self.image = assets[GHOST_IMG]
        self.rect = self.image.get_rect()
        self.dx = -1
        self.dy = 0
        self.x = x
        self.y = y

        self.last_move = pygame.time.get_ticks()
        self.move_ticks = 300
   
    # Definindo o movimento dos fantasmas
    def move(self):
        if (not self.is_time_to_move()):
            return
        
        self.last_move = pygame.time.get_ticks()
        
        if (self.can_keep_moving()):
            self.x += self.dx
            self.y += self.dy
        else:
            self.move_randomly()
        
    # Definindo o movimento randômico dos fantasmas
    def move_randomly(self):
        possible_moves = [
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, 0)
        ]

        available_moves = list(filter(self.can_move, possible_moves))

        # Impedindo que o fantasma volte o mesmo caminho que ele acabou de andar
        opposite_direction = (self.dx * -1, self.dy * -1)
        if (len(available_moves) > 1 and opposite_direction in available_moves):
            available_moves.remove(opposite_direction)

        if (len(available_moves) > 0):
            dx, dy = random.choice(available_moves)

            self.dx = dx
            self.dy = dy

            self.x = self.x + self.dx
            self.y = self.y + self.dy
        
    # Criando um timer para saber já é hora de mover
    def is_time_to_move(self):
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_move

        return elapsed_ticks >= self.move_ticks

    # Update dos fantasmas
    def update(self):
        self.move()
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        
    # Definindo a chance do fantasma seguir reto quando houver um caminho adjacente
    def can_keep_moving(self):
        chance = random.random()

        return self.can_move((self.dx, self.dy)) and chance > 0.75

    # Verifica se há uma parede à frente e se o movimento respeita os limites da tela
    def can_move(self, offset):
        return self.is_free_space(offset) and self.is_in_bounds(offset)
    
    # Verificando se há uma parede à frente
    def is_free_space(self, offset):
        dx, dy = offset
        
        for wall in self.all_walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return False
        
        return True
    
    # Verificando se o movimento respeita os limites da tela
    def is_in_bounds(self, offset):
        dx, dy = offset

        final_x = self.x + dx
        final_y = self.y + dy

        return final_x > 0 and final_x < WIDTH and final_y > 0 and final_y < HEIGHT