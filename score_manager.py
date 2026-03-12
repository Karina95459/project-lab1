import pygame

class ScoreManager:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.font = pygame.font.Font(None, 36)