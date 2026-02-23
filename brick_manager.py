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
        # Очищуємо список, щоб при перезапуску не створювати нові блоки поверх старих
        self.bricks.clear()

        # Встановимо розмір одного блоку
        brick_width = 60
        brick_height = 20

        # Проходимося по рядках і колонках
        for row in range(self.rows):
            for col in range(self.cols):
                # Обчислюємо позицію (x, y) для кожного блоку
                # x = початковий x + (номер колонки * (ширина + відступ))
                # y = початковий y + (номер рядка * (висота + відступ))
                curr_x = self.start_x + col * (brick_width + self.gap)
                curr_y = self.start_y + row * (brick_height + self.gap)

                # Створюємо новий об'єкт Brick
                new_brick = brick.Brick(curr_x, curr_y, brick_width, brick_height)

                # Додаємо створений блок у список bricks
                self.bricks.append(new_brick)

    def draw(self, screen: pygame.Surface) -> None:
        # Проходимося циклом по кожній цеглині у нашому списку
        for bricks in self.bricks:
            # Викликаємо метод draw, який ми раніше написали в класі Brick
            bricks.draw(screen)

    def check_collision(self, ball: ball.Ball) -> int:
        total_score = 0

        # Проходимося по всіх блоках
        for brick in self.bricks:
            # Пропускаємо вже знищені блоки
            if not brick.is_destroyed:
                # Перевіряємо зіткнення м'яча з блоком
                if ball.get_rect().colliderect(brick.get_rect()):
                    # Якщо є зіткнення → знищуємо блок
                    brick.destroy()
                    # Змушуємо м'яч відскочити
                    ball.bounce_y()
                    # Нараховуємо очки за кожен збитий блок
                    total_score += 10
                    # Виходимо з циклу після першого зіткнення, щоб м'яч не збив дві цеглини за один кадр
                    break
        # Повертаємо загальну суму очок за цей крок
        return total_score

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
