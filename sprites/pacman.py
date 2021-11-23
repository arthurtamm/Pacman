import pygame

from settings import WIDTH, HEIGHT, TILESIZE

class Pacman(pygame.sprite.Sprite):
    def __init__(self, img, x, y, all_walls = []):
        pygame.sprite.Sprite.__init__(self)

        self.all_walls = all_walls
        self.original_image = img
        self.image = img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        
        self.dx = 1
        self.dy = 0

    def move(self, dx=0, dy=0):
        if self.is_free_space(dx, dy) and self.is_in_bounds((dx, dy)):
            self.dx = dx
            self.dy = dy

            self.x += self.dx
            self.y += self.dy

    def is_free_space(self, dx=0, dy=0):
        for wall in self.all_walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return False
        
        return True

    def is_in_bounds(self, offset):
        dx, dy = offset

        final_x = self.x + dx
        final_y = self.y + dy

        return final_x > 0 and final_x < WIDTH and final_y > 0 and final_y < HEIGHT

    def update(self):
        self.adjust_image()

        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def adjust_image(self):        
        current_direction = (self.dx, self.dy)

        if (current_direction == (0, -1)):
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif (current_direction == (1, 0)):
            self.image = self.original_image
        elif (current_direction == (0, 1)):
            self.image = pygame.transform.rotate(self.original_image, -90)
        else:
            self.image = pygame.transform.flip(self.original_image, True, False)