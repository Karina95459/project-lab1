import pygame
import brick
import ball

class BrickManager:
    def __init__(self, rows: int, cols: int, start_y: int, start_x: int, gap: int):
        self.rows = rows
        self.cols = cols
        self.start_y = start_y
        self.start_x = start_x
        self.gap = gap
        self.bricks: list[brick.Brick] = []

    def create_level(self) -> None:
        # TODO: очистити список bricks
        # TODO: пройтись по rows і cols
        # TODO: обчислити позицію кожного блоку
        # TODO: створити Brick, додати створені Brick у self.bricks
        # TODO: додати Brick у список bricks
        pass

    def draw(self, screen: pygame.Surface) -> None:
        # TODO: пройтись по всіх bricks
        # TODO: викликати draw() у кожного блоку
        pass

    def check_collision(self, ball: ball.Ball) -> int:
        # TODO: пройтись по всіх bricks
        # TODO: пропустити знищені блоки
        # TODO: перевірити зіткнення ball.get_rect() з brick.get_rect()
        # TODO: якщо є зіткнення → викликати brick.destroy()
        # TODO: викликати ball.bounce_y() або bounce_x()
        # TODO:повернути кількість очок (int), які треба додати
        pass

    def all_destroyed(self) -> bool:
        # TODO: перевірити всі bricks
        # TODO: якщо всі знищені → повернути True
        # TODO: інакше False
        pass

    def reset(self) -> None:
        # TODO: очистити список bricks
        # TODO: викликати create_level()
        # TODO: використовується при restart
        pass
