import pygame

# Brick — один блок у грі.
# Використовується BrickManager для створення рівня.
class Brick:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_destroyed = False

    def get_rect(self) -> pygame.Rect:
        # Створюємо об'єкт Rect, використовуючи поточні координати та розміри об'єкта
        rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Повертаємо його для подальшої перевірки collision
        return rect

    def draw(self, screen: pygame.Surface) -> None:
        # TODO: малювати тільки якщо is_destroyed == False
        # TODO: намалювати прямокутник pygame.draw.rect
        # TODO: використати x, y, width, height
        # TODO: колір блоку задати константою або полем
        pass

    def destroy(self) -> None:
        # TODO: встановити is_destroyed = True
        # TODO: викликається при зіткненні з м'ячем
        pass