import pygame

class Platform:
    def __init__(self, x: int, y: int,height: int, width: int, speed: int):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.speed = speed
        self.start_x = x
        self.start_y = y

    def move_right(self) -> None:
        # TODO: збільшити x на speed
        # TODO: викликається при натиснутій клавіші “Right/D”
        # TODO: після руху викликати clamp()
        pass

    def move_left(self) -> None:
        # TODO: зменшити x на speed
        # TODO: викликається при натиснутій клавіші “Left/A”
        # TODO: після руху викликати clamp()
        pass

    def draw(self, screen: pygame.Surface) -> None:
        # TODO: намалювати прямокутник pygame.draw.rect
        # TODO: використати x, y, width, height
        # TODO: колір платформи задати константою або полем
        pass

    # використовується для колізій з м’ячем
    def get_rect(self) -> pygame.Rect:
        # TODO: повернути pygame.Rect з (x, y, width, height)
        # TODO: використовується для колізій з м’ячем
        pass

    def clamp(self, screen_width: int) -> None:
        # TODO: якщо x < 0 - зробити x = 0
        # TODO: якщо x + width > screen_width -> x = screen_width - width
        # TODO: викликати після move_left/move_right
        pass

    def reset(self) -> None:
        # TODO: повернути платформу у стартову позицію
        # TODO: self.x = start_x
        # TODO: self.y = start_y
        pass

