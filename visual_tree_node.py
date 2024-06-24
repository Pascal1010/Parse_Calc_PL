import pygame


class VisualNode:
    def __init__(self, node, surf, x, y):
        self.node = node
        self.surf = surf
        self.x = x
        self.y = y
        self.node_font = pygame.font.Font('freesansbold.ttf', 15)
        self.node_size = self.node_font.size(f'{self.node}')
        self.node_text = self.node_font.render(f'{self.node}', True, (0, 0, 0))
        self.rect = pygame.rect.Rect((self.x - 10, self.y - 10), (int(0.80 * max(self.node_size)), int(0.80 * max(self.node_size))))
        self.pad_rect = self.rect.inflate(20, 20)

    def draw_node(self):
        if self.node.isdigit():
            circle = pygame.draw.circle(self.surf, (10, 150, 255), (self.x - 10, self.y - 10), int(0.80 * max(self.node_size)))
            self.surf.blit(self.node_text, self.node_text.get_rect(center=circle.center))
        else:
            circle = pygame.draw.circle(self.surf, (255, 20, 30), (self.x - 10, self.y - 10), max(self.node_size))
            self.surf.blit(self.node_text, self.node_text.get_rect(center=circle.center))

