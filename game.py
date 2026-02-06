import pygame
import ball
import platform
import brick_manager

# Game відповідає за головний цикл гри
# викликає Ball, Platform, BrickManager
# не містить їх логіки

class Game:
    def __init__(self, width: int, height: int, fps: int ):
        # TODO: тут буде pygame.init()
        self.width = width
        self.height = height
        self.fps = fps
        self.screen = None   #TODO: створити screen через pygame.display
        self.clock = None #TODO створити clock
        self.ball = None #TODO: створюється в init_objects()
        self.platform = None #TODO: створюється в init_objects()
        self.brick_manager = None #TODO створюється в init_objects()
        self.is_running = True
        self.is_paused = False
        self.is_game_over = False
        self.is_win = False
        self.score = 0
        self.font = None #TODO створити font
        #TODO:в кінці init викликати init_objects

    def run(self) -> None:
        #TODO: головний цикл гри
        #TODO: виклик handle_events
        #TODO: виклик update
        #TODO: виклик draw
        #TODO: clock.tick(self.fps)
        pass

    def handle_events(self) -> None:
        #TODO: обробка pygame events
        #TODO: вихід з гри
        #TODO: рух платформи
        #TODO: pause
        #TODO: restart
        pass

    def update(self) -> None:
        #TODO: рух м'яча
        #TODO: перевірка стін
        #TODO:перевірка платформи
        #TODO: перевірка блоків
        #TODO: оновити score
        #TODO: перевірити програш
        #TODO: перевірити перемогу
        pass

    def draw(self) -> None:
        #TODO: очистити екран
        #TODO: намалювати блоки
        #TODO: намалювати платформу
        #TODO: намалювати м'яч
        #TODO: намалювати UI
        #TODO: pygame.display.flip()
        pass

    def toggle_pause(self) -> None:
        #TODO: змінити is_paused
        pass

    def restart(self) -> None:
        #TODO: скинути score
        #TODO: reset ball
        #TODO: reset platform
        #TODO: reset bricks
        #TODO: скинути стани
        pass

    def check_wall_collisions(self) -> None:
        #TODO: ліва/права стіна
        #TODO: верхня стіна
        #TODO: bounce
        pass

    def check_paddle_collision(self) -> None:
        #TODO: ball rect vs platform rect
        #TODO: bounce: якщо зіткнення сталося, потрібно змінити напрям руху м’яча.
        #TODO: після зіткнення скоригувати позицію м'яча, щоб не було повторного зіткнення
        pass

    def draw_ui(self) -> None:
        #TODO: score text
        #TODO: pause text
        #TODO: game over
        #TODO: win
        pass

    def init_objects(self) -> None:
        #TODO: встановити стартові координати і швидкості
        #TODO: створити ball
        #TODO: створити platform
        #TODO: створити brick_manager
        #TODO: створити level
        pass







