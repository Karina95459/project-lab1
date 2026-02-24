import pygame

class Ball:
    def __init__(self, x: int, y: int, radius: int, dx: int, dy: int):
        self.x = x # зберегти поточну позицію м'яча
        self.y = y #  зберегти поточну позицію м'яча
        # стартова позиція = початкові x, y
        self.start_x = x  # запам'ятали старт
        self.start_y = y
        self.radius = radius # зберегти радіус
        self.dx = dx # зберегти швидкість руху
        self.dy = dy # зберегти швидкість руху

    # метод руху м’яча, що він робить: змінює координати кожен кадр, використовує dx і dy
    def move(self) -> None:
        # Змінюємо х відповідно до dx (додаємо швидкість по горизонталі)
        self.x += self.dx

        # Змінюємо y відповідно до dy (додаємо швидкість по вертикалі)
        self.y += self.dy

    # цей метод малює м'яч на екрані
    def draw(self, screen: pygame.Surface) -> None:
        # Визначаємо колір (RGB формат).
        color = (255, 255, 255)

        # Синтаксис
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)

    # метод відскоку по горизонталі, викликається коли: коли м’яч б’ється
    # об ліву/праву стіну коли б’ється об блок (з боку)
    def bounce_x(self) -> None:
        # Змінюємо напрям руху по Х, інвертуючи dx
        self.dx = -self.dx

    # метод відскоку по вертикалі, Коли викликається: при ударі об платформу
    # при ударі об блок при ударі об верхню стіну
    def bounce_y(self) -> None:
        # Змінюємо напрям руху по Y, інвертуючи dy
        self.dy = -self.dy

    # повертає прямокутник м’яча(використовуємо саме прямокутник для перевірки
    # зіткнення, бо y pygame так буде зручно) для перевірки зіткнень.
    def get_rect(self) -> pygame.Rect:
        # Обчислюємо сторону квадрата (діаметр м'яча)
        side = self.radius * 2

        rect = pygame.Rect(self.x - self.radius, self.y - self.radius, side, side)

        return rect

    # якщо м’яч нижче екрану - програш
    def is_out_of_bounds(self, screen_height: int) -> bool:
        if self.y - self.radius > screen_height:
            return True

        # Якщо умова вище не справдилася, м'яч ще в грі
        return False

    # рестарт для м'яча у грі
    def reset(self) -> None:
        # TODO: повернути м’яч у стартову позицію
        pass
