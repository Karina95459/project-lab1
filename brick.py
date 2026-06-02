import pygame

# Brick — один блок у грі.
# Використовується BrickManager для створення рівня.
class Brick:
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

            # Малюємо прямокутник: (поверхня, колір, (x, y, w, h))

            pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2)

    def destroy(self) -> None:
        # Встановлюємо прапорець у True, щоб метод draw перестав малювати блок
        self.is_destroyed = True
