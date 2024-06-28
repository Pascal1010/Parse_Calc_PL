import sys

import pygame
from visual_tree_node import VisualNode


class VisualTool:
    def __init__(self, tree):
        # General Settings

        pygame.init()
        self.WIDTH = 1080
        self.HEIGHT = 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.display = pygame.Surface((self.WIDTH, max(self.HEIGHT, 100 * self.count_depth(tree))))
        pygame.display.set_caption("Parse Tree")
        self.clock = pygame.time.Clock()
        # Set up tree generation
        self.tree = tree
        self.nodes = []

        # Move the camera around the display
        self.scroll = [0, 0]
        self.camera_x = 0
        self.camera_y = 0
        # left, right, up, down
        self.movement = [False, False, False, False]

    def draw(self, node, x, y, level, gap):
        if node.root:
            my_node = VisualNode(node.root, self.display, x, y)
            my_node.draw_node()
            next_level_gap = gap // 2
            if node.left:
                left_x = x - gap
                left_y = y + 100
                pygame.draw.aaline(self.display, (0, 0, 0), (x - 10, y + 5), (left_x - 10, left_y - 10))
                self.draw(node.left, left_x, left_y, level + 1, next_level_gap)

            if node.right:
                right_x = x + gap
                right_y = y + 100
                pygame.draw.aaline(self.display, (0, 0, 0), (x - 10, y + 5), (right_x - 10, right_y - 10))
                self.draw(node.right, right_x, right_y, level + 1, next_level_gap)

    def count_depth(self, node):
        if node is None:
            return 0
        else:
            l_depth = self.count_depth(node.left)
            r_depth = self.count_depth(node.right)
            if l_depth > r_depth:
                return l_depth + 1
            else:
                return r_depth + 1
    def run(self):
        while True:
            self.display.fill((180, 180, 180))
            self.scroll[0] = (self.movement[1] - self.movement[0]) * 7
            self.scroll[1] = (self.movement[3] - self.movement[2]) * 7
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            self.camera_x += render_scroll[0]
            self.camera_y += render_scroll[1]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False

            initial_gap = 800 // 4
            self.draw(self.tree, self.WIDTH // 2, 50, 0, initial_gap)
            self.screen.blit(self.display, (0, 0), (self.camera_x, self.camera_y, self.WIDTH, self.HEIGHT))
            pygame.display.update()
            self.clock.tick(60)
