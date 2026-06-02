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