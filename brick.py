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
        # Малюємо блок тільки якщо він ще не розбитий
        if not self.is_destroyed:
            brick_color = (255, 215, 0)

            # Малюємо прямокутник: (поверхня, колір, (x, y, w, h))
            pygame.draw.rect(screen, brick_color, (self.x, self.y, self.width, self.height))

            # Малюємо рамку, щоб блоки не зливалися (товщина 2 пікселя)
            pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2)

    def destroy(self) -> None:
        # TODO: встановити is_destroyed = True
        # TODO: викликається при зіткненні з м'ячем
        pass