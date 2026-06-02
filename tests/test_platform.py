import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from paddle import Platform


@pytest.fixture
def paddle():
    """Фікстура для створення платформи з базовими параметрами"""
    return Platform(x=100, y=500, height=20, width=100, speed=10)


@pytest.fixture
def paddle_params():
    """Фікстура для платформи з кастомними параметрами"""

    def _make_paddle(x=100, y=500, height=20, width=100, speed=10):
        return Platform(x=x, y=y, height=height, width=width, speed=speed)

    return _make_paddle


class TestPlatformMovement:
    """Тести для руху платформи (move_left, move_right)"""

    def test_move_right_increases_x(self, paddle):
        """Рух вправо має збільшити x на значення speed"""
        initial_x = paddle.x
        paddle.move_right()
        assert paddle.x == initial_x + paddle.speed

    def test_move_right_multiple_times(self, paddle):
        """Кілька рухів вправо мають накопичуватися"""
        initial_x = paddle.x
        paddle.move_right()
        paddle.move_right()
        paddle.move_right()
        assert paddle.x == initial_x + (paddle.speed * 3)

    @pytest.mark.parametrize("speed", [5, 10, 20, 50])
    def test_move_right_with_different_speeds(self, paddle_params, speed):
        """Перевірка руху вправо з різними значеннями speed"""
        p = paddle_params(speed=speed)
        initial_x = p.x
        p.move_right()
        assert p.x == initial_x + speed

    def test_move_left_decreases_x(self, paddle):
        """Рух вліво має зменшити x на значення speed"""
        initial_x = paddle.x
        paddle.move_left()
        assert paddle.x == initial_x - paddle.speed

    def test_move_left_multiple_times(self, paddle):
        """Кілька рухів вліво мають накопичуватися"""
        initial_x = paddle.x
        paddle.move_left()
        paddle.move_left()
        paddle.move_left()
        assert paddle.x == initial_x - (paddle.speed * 3)

    @pytest.mark.parametrize("speed", [5, 10, 20, 50])
    def test_move_left_with_different_speeds(self, paddle_params, speed):
        """Перевірка руху вліво з різними значеннями speed"""
        p = paddle_params(speed=speed)
        initial_x = p.x
        p.move_left()
        assert p.x == initial_x - speed

    def test_move_left_can_go_negative(self, paddle):
        """Рух вліво може дати від'ємні координати (без clamp)"""
        paddle.x = 5
        paddle.speed = 10
        paddle.move_left()
        assert paddle.x == -5


class TestPlatformClamp:
    """Тести для обмеження позиції платформи на екрані (clamp)"""

    def test_clamp_left_boundary(self, paddle):
        """Якщо x < 0, має бути встановлено x = 0"""
        paddle.x = -50
        paddle.clamp(800)
        assert paddle.x == 0

    def test_clamp_left_boundary_at_zero(self, paddle):
        """Якщо x = -1, має бути встановлено x = 0"""
        paddle.x = -1
        paddle.clamp(800)
        assert paddle.x == 0

    @pytest.mark.parametrize("x,screen_width,expected", [
        (-100, 800, 0),
        (-50, 800, 0),
        (-1, 800, 0),
        (0, 800, 0),
        (1, 800, 1),
    ])
    def test_clamp_left_boundary_parametrized(self, paddle_params, x, screen_width, expected):
        """Параметризований тест для лівої границі"""
        p = paddle_params(x=x)
        p.clamp(screen_width)
        assert p.x == expected

    def test_clamp_right_boundary(self, paddle):
        """Якщо x + width > screen_width, має бути x = screen_width - width"""
        paddle.x = 750
        paddle.width = 100
        paddle.clamp(800)
        assert paddle.x == 700  # 800 - 100

    def test_clamp_right_boundary_exact(self, paddle):
        """Якщо x + width = screen_width, позиція невинна змінюватися"""
        paddle.x = 700
        paddle.width = 100
        paddle.clamp(800)
        assert paddle.x == 700

    @pytest.mark.parametrize("x,width,screen_width,expected", [
        (750, 100, 800, 700),  # 750 + 100 = 850 > 800
        (701, 100, 800, 700),  # 701 + 100 = 801 > 800
        (700, 100, 800, 700),  # 700 + 100 = 800 (на границі)
        (699, 100, 800, 699),  # 699 + 100 = 799 < 800
        (975, 50, 1024, 974),   # 975 + 50 = 1025 > 1024 ✓
    ])
    def test_clamp_right_boundary_parametrized(self, paddle_params, x, width, screen_width, expected):
        """Параметризований тест для правої границі"""
        p = paddle_params(x=x, width=width)
        p.clamp(screen_width)
        assert p.x == expected

    def test_clamp_within_bounds(self, paddle):
        """Якщо позиція в межах екрану, не змінюється"""
        paddle.x = 400
        original_x = paddle.x
        paddle.clamp(800)
        assert paddle.x == original_x

    def test_clamp_does_not_affect_y(self, paddle):
        """Clamp не повинен змінювати y координату"""
        paddle.x = -50
        original_y = paddle.y
        paddle.clamp(800)
        assert paddle.y == original_y

    def test_clamp_after_move_left(self, paddle):
        """Clamp після move_left, коли платформа виходить за ліву границю"""
        paddle.x = 0
        paddle.speed = 50
        paddle.move_left()
        assert paddle.x == -50
        paddle.clamp(800)
        assert paddle.x == 0

    def test_clamp_after_move_right(self, paddle):
        """Clamp після move_right, коли платформа виходить за праву границю"""
        paddle.x = 790  # близько до границі
        paddle.width = 100
        paddle.speed = 50
        paddle.move_right()
        assert paddle.x == 840
        paddle.clamp(800)
        assert paddle.x == 700


class TestPlatformInit:
    """Тести для ініціалізації платформи"""

    def test_platform_init_basic(self, paddle):
        """Платформа має мати правильні початкові значення"""
        assert paddle.x == 100
        assert paddle.y == 500
        assert paddle.height == 20
        assert paddle.width == 100
        assert paddle.speed == 10

    def test_platform_init_start_positions(self, paddle):
        """start_x та start_y повинні зберегти початкові позиції"""
        assert paddle.start_x == 100
        assert paddle.start_y == 500

    def test_platform_init_color(self, paddle):
        """Колір платформи повинен бути білий (255, 255, 255)"""
        assert paddle.color == (255, 255, 255)

    @pytest.mark.parametrize("x,y,height,width,speed", [
        (0, 0, 10, 50, 5),
        (400, 300, 30, 150, 20),
        (1024, 720, 15, 80, 12),
        (50, 100, 25, 120, 15),
    ])
    def test_platform_init_parametrized(self, paddle_params, x, y, height, width, speed):
        """Параметризований тест для різних конфігурацій платформи"""
        p = paddle_params(x=x, y=y, height=height, width=width, speed=speed)
        assert p.x == x
        assert p.y == y
        assert p.height == height
        assert p.width == width
        assert p.speed == speed
        assert p.start_x == x
        assert p.start_y == y