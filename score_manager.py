import pygame

class ScoreManager:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.font = pygame.font.Font(None, 36)

    def add(self, points: int) -> None:
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score

    def reset(self) -> None:
        self.score = 0

