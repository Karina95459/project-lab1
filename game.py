import pygame
import ball
import platform
import brick_manager

# Game відповідає за головний цикл гри
# викликає Ball, Platform, BrickManager
# не містить їх логіки

class Game:
    def __init__(self, width: int, height: int, fps: int ):
        pygame.init()
        self.width = width
        self.height = height
        self.fps = fps
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ball = None #TODO: створюється в init_objects()
        self.platform = None #TODO: створюється в init_objects()
        self.brick_manager = None #TODO створюється в init_objects()
        self.is_running = True
        self.is_paused = False
        self.is_game_over = False
        self.is_win = False
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.init_objects()

# головний цикл гри
    def run(self) -> None:

        while self.is_running:
            self.handle_events()

            if not self.is_paused and not self.is_game_over and not self.is_win:
                self.update()

            self.draw()
            self.clock.tick(self.fps)

    def handle_events(self) -> None:

        for event in pygame.event.get():

            # беремо всі події, що накопичились
            if event.type == pygame.QUIT: # якщо натиснули Х закриваємо вікно
                self.is_running = False

            # обробка натискань клавіш
            if event.type == pygame.KEYDOWN:

                # esc - вихід
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False

                # рестарт
                if event.key == pygame.K_r:
                    self.restart()

                #перевіряємо чи це р
                if event.key == pygame.K_p:
                 # викликаємо перемикач паузи
                    self.toggle_pause()

        if self.platform is None:
            return

        if self.is_paused or self.is_game_over or self.is_win:
            return

        keys = pygame.key.get_pressed()

        # завдяки яким клавішам платформа рухається вліво
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.platform.move_left()

        # завдяки яким клавішам платформа рухається вправо
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.platform.move_right()

        #використовуємо метод з класу platform для того, щоб платформа не виходила за межі
        self.platform.clamp(self.width)



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
        self.screen.fill((0,0,0)) # заливаємо фон чорним
        pygame.display.flip()   # показуємо кадр на екрані


    def toggle_pause(self) -> None:

        # змінюємо стан паузи на протилежний
        self.is_paused = not self.is_paused


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







