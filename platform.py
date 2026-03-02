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
        self.color = (255, 255, 255)  # Білий колір

    def move_right(self) -> None:
        # збільшити x на speed
        self.x += self.speed


    def move_left(self) -> None:
        # зменшити x на speed
        self.x -= self.speed


    def draw(self, screen: pygame.Surface) -> None:
        #  намалювати прямокутник pygame.draw.rect
        # використати x, y, width, height
        # колір платформи задати константою або полем
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


    # використовується для колізій з м’ячем
    def get_rect(self) -> pygame.Rect:
        # повернути pygame.Rect з (x, y, width, height)
        # використовується для колізій з м’ячем
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def clamp(self, screen_width: int) -> None:
        #  якщо x < 0 - зробити x = 0
        if self.x < 0:
            self.x = 0
        #  якщо x + width > screen_width -> x = screen_width - width
        if self.x + self.width > screen_width:
            self.x = screen_width - self.width
        #  викликати після move_left/move_right


    def reset(self) -> None:
        # повернути платформу у стартову позицію
        # self.x = start_x
        # self.y = start_y
        self.x = self.start_x
        self.y = self.start_y
        