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
        # TODO: змінити х відповідно до dx
        # TODO: змінити y відповідно до dy
        pass

    # цей метод малює м'яч на екрані
    def draw(self, screen: pygame.Surface) -> None:
        # TODO: намалювати коло pygame.draw.circle
        # TODO: використати координати x, y
        # TODO: використати radius
        pass

    # метод відскоку по горизонталі, викликається коли: коли м’яч б’ється
    # об ліву/праву стіну коли б’ється об блок (з боку)
    def bounce_x(self) -> None:
        # TODO: змінити напрям руху по Х
        # TODO: інвертувати dx
        pass

    # метод відскоку по вертикалі, Коли викликається: при ударі об платформу
    # при ударі об блок при ударі об верхню стіну
    def bounce_y(self) -> None:
        # TODO: змінити напрям руху по Y
        # TODO: інвертувати dy
        pass

    # повертає прямокутник м’яча(використовуємо саме прямокутник для перевірки
    # зіткнення, бо y pygame так буде зручно) для перевірки зіткнень.
    def get_rect(self) -> pygame.Rect:
        # TODO: створити pygame.Rect для м’яча
        # TODO: розмір rect = radius * 2
        # TODO: Rect має покривати м’яч (x, y як центр)
        # TODO: використовується для перевірки колізій
        # TODO: повернути Rect
        pass

    # якщо м’яч нижче екрану - програш
    def is_out_of_bounds(self, screen_height: int) -> bool:
        # TODO: перевірити чи м’яч нижче екрану
        # TODO: перевірити вихід за нижню межу з урахуванням radius
        # TODO: інакше False
        # TODO: повернути True/False
        pass

    # рестарт для м'яча у грі
    def reset(self) -> None:
        # TODO: повернути м’яч у стартову позицію
        pass
