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

    def draw(self, screen: pygame.Surface) -> None:
        score_text = self.font.render(f"Score: {self.score}", True, (0, 255, 0))
        high_text = self.font.render(f"Best: {self.high_score}", True, (200, 200, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(high_text, (10, 40))