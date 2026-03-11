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
        # TODO: додати start_dx і start_dy і зберегти у них початкові значення dx і dy
        # TODO: додати speed_multiplier = 1.0
        # TODO: додати max_multiplier = 2.5
        # TODO: додати acceleration_rate = 0.001

    # метод руху м’яча, що він робить: змінює координати кожен кадр, використовує dx і dy
    def move(self) -> None:
        # TODO: замість self.x += self.dx множити self.dx на speed_multiplier перед додаванням
        # TODO: те саме для self.y += self.dy
        # TODO: використати int() щоб округлити результат до цілого числа
        # Змінюємо х відповідно до dx (додаємо швидкість по горизонталі)
        self.x += self.dx

        # Змінюємо y відповідно до dy (додаємо швидкість по вертикалі)
        self.y += self.dy

    def accelerate(self) -> None:
        # TODO: якщо speed_multiplier < max_multiplier — збільшити на acceleration_rate
        pass

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
        # Повертаємо координати x та y до початкових значень
        self.x = self.start_x
        self.y = self.start_y
        # TODO: скинути speed_multiplier до 1.0
