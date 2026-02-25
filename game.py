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
        self.ball = None # створюється в init_objects()
        self.platform = None # створюється в init_objects()
        self.brick_manager = None # створюється в init_objects()
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
        #TODO: перевірка платформи
        #TODO: перевірка блоків
        #TODO: оновити score
        #TODO: перевірити програш
        #TODO: перевірити перемогу
        pass


    def draw(self) -> None:
        self.screen.fill((0,0,0))

        if self.brick_manager is not None:
            self.brick_manager.draw(self.screen) # намалювати блоки

        if self.platform is not None:
            self.platform.draw(self.screen) # намалювати платформу

        if self.ball is not None:
            self.ball.draw(self.screen) # намалювати м'яч

        self.draw_ui() # намалювати UI(рахунок, пауза, перемога, програш)
        pygame.display.flip()   # показуємо кадр на екрані


    def toggle_pause(self) -> None:
        # змінюємо стан паузи на протилежний
        self.is_paused = not self.is_paused


    def restart(self) -> None:
        if self.ball is None or self.platform is None or self.brick_manager is None:
            return

        self.score = 0 # скинути score
        # скинути стани
        self.is_game_over = False
        self.is_win = False
        self.is_paused = False

        self.ball.reset() # reset ball
        self.platform.reset() # reset platform
        self.brick_manager.reset() # reset bricks


    def check_wall_collisions(self) -> None:
        if self.ball is None:
            return

        # чи ліва точка м’яча торкнулась лівого краю екрана
        if self.ball.x - self.ball.radius < 0:
            self.ball.bounce_x() # Бо удар був по горизонталі → міняємо напрям X.
            self.ball.x = self.ball.radius

        # чи права точка м’яча торкнулась правого краю екрана
        if self.ball.x + self.ball.radius >= self.width:
            self.ball.bounce_x() # Бо удар був по горизонталі → міняємо напрям X.
            self.ball.x = self.width - self.ball.radius

        # чи верх м’яча торкнувся верхньої межі екрана
        if self.ball.y - self.ball.radius <= 0:
            self.ball.bounce_y() # Бо удар був по вертикалі → міняємо напрям Y
            self.ball.y = self.ball.radius


    def check_paddle_collision(self) -> None:
        if self.ball is None or self.platform is None:
            return

        ball_rect = self.ball.get_rect()
        platform_rect = self.platform.get_rect()

        if ball_rect.colliderect(platform_rect):
            if self.ball.dy > 0:
                self.ball.bounce_y() # bounce: якщо зіткнення сталося, потрібно змінити напрям руху м’яча.
                self.ball.y = self.platform.y - self.ball.radius # після зіткнення скоригувати позицію м'яча, щоб не було повторного зіткнення




    def draw_ui(self) -> None:
        # score
        score_text = self.font.render(f"Score: {self.score}", True, (0, 255, 0))
        self.screen.blit(score_text, (10, 10))

        # pause
        if self.is_paused:
            pause_text = self.font.render("PAUSED", True, (255, 0, 0))
            self.screen.blit(pause_text, (self.width // 2 - 60, self.height // 2))

        # game over
        if self.is_game_over:
            over_text = self.font.render("GAME OVER", True, (255, 0, 0))
            self.screen.blit(over_text, (self.width // 2 - 90, self.height // 2))

        # win
        if self.is_win:
            win_text = self.font.render("YOU WIN!", True, (0, 255, 0))
            self.screen.blit(win_text, (self.width // 2 - 80, self.height // 2))


    def init_objects(self) -> None:
        # початкові координати, розміри та швидкості
        platform_width = 120
        platform_height = 15
        platform_speed = 8

        ball_radius = 10
        ball_dx = 4
        ball_dy = -4

        rows = 5
        cols = 10
        gap = 6
        start_x = 40
        start_y = 60

        # створюємо платформу
        platform_x = (self.width - platform_width) // 2

        # Y робимо так, щоб платформа була по центру
        platform_y = self.height - 40

        self.platform = platform.Platform(platform_x, platform_y, platform_height, platform_width, platform_speed)

        # створюємо м'яч
        ball_x = platform_x + platform_width // 2
        ball_y = platform_y - ball_radius - 2

        self.ball = ball.Ball(ball_x, ball_y, ball_radius, ball_dx, ball_dy)

        # створюємо brick manager
        self.brick_manager = brick_manager.BrickManager(rows, cols, start_y, start_x, gap)

        # створюємо рівень(список блоків)
        self.brick_manager.create_level()
