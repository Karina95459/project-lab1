import pygame

class ScoreManager:
    def __init__(self):
        # TODO: створити змінну score = 0
        # TODO: створити змінну high_score = 0
        # TODO: створити font = pygame.font.Font(None, 36)
        pass

    def add(self, points: int) -> None:
        # TODO: додати значення points до score
        # TODO: якщо score більше ніж high_score — записати score в high_score
        pass

    def reset(self) -> None:
        # TODO: скинути score = 0
        pass

    def draw(self, screen: pygame.Surface) -> None:
        # TODO: за допомогою font.render створити текстовий об'єкт score_text з написом "Score: {self.score}" зеленим кольором
        # TODO: відобразити його на екрані через screen.blit з координатами (10, 10)
        # TODO: за допомогою font.render створити текстовий об'єкт high_text з написом "Best: {self.high_score}" жовтим кольором
        # TODO: відобразити його на екрані через screen.blit з координатами (10, 40)
        pass