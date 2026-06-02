"""
Тести для класу Ball (Breakout/Arkanoid гра).

Використані інструменти pytest:
  - fixtures        : ball, fast_ball, boundary_ball
  - parametrization : test_bounce_x_parametrized, test_bounce_y_parametrized,
                      test_is_out_of_bounds_parametrized
  - mocking         : test_draw_calls_pygame (unittest.mock.patch)
  - markers         : @pytest.mark.movement, @pytest.mark.collision,
                      @pytest.mark.rendering, @pytest.mark.slow
"""

import pytest
from unittest.mock import MagicMock, patch
from ball import Ball


# ---------------------------------------------------------------------------
# Маркери
# ---------------------------------------------------------------------------
def pytest_configure(config):
    config.addinivalue_line("markers", "movement: тести руху м'яча")
    config.addinivalue_line("markers", "collision: тести зіткнень і відскоків")
    config.addinivalue_line("markers", "rendering: тести відмалювання")
    config.addinivalue_line("markers", "slow: повільні/ітеративні тести")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def ball():
    """Стандартний м'яч по центру екрану."""
    return Ball(x=400, y=300, radius=10, dx=5, dy=-5)


@pytest.fixture
def fast_ball():
    """М'яч із великою швидкістю для тестів межових умов."""
    return Ball(x=100, y=100, radius=8, dx=15, dy=15)


@pytest.fixture
def boundary_ball():
    """М'яч поблизу нижньої межі екрану (height=600)."""
    # y=595 → нижній край = 595+10 = 605 > 600 → out of bounds
    return Ball(x=200, y=595, radius=10, dx=3, dy=3)


# ---------------------------------------------------------------------------
# Тести ініціалізації
# ---------------------------------------------------------------------------
class TestInit:
    def test_initial_position(self, ball):
        assert ball.x == 400
        assert ball.y == 300

    def test_initial_velocity(self, ball):
        assert ball.dx == 5
        assert ball.dy == -5

    def test_start_position_saved(self, ball):
        assert ball.start_x == 400
        assert ball.start_y == 300

    def test_start_velocity_saved(self, ball):
        assert ball.start_dx == 5
        assert ball.start_dy == -5

    def test_default_speed_multiplier(self, ball):
        assert ball.speed_multiplier == 1.0

    def test_radius_stored(self, ball):
        assert ball.radius == 10


# ---------------------------------------------------------------------------
# Тести руху
# ---------------------------------------------------------------------------
@pytest.mark.movement
class TestMove:
    def test_move_changes_x(self, ball):
        ball.move()
        assert ball.x == 405  # 400 + int(5 * 1.0)

    def test_move_changes_y(self, ball):
        ball.move()
        assert ball.y == 295  # 300 + int(-5 * 1.0)

    def test_move_multiple_steps(self, ball):
        for _ in range(3):
            ball.move()
        assert ball.x == 415
        assert ball.y == 285

    def test_move_with_speed_multiplier(self, ball):
        ball.speed_multiplier = 2.0
        ball.move()
        assert ball.x == 410  # 400 + int(5 * 2.0)
        assert ball.y == 290  # 300 + int(-5 * 2.0)

    def test_move_fast_ball(self, fast_ball):
        fast_ball.move()
        assert fast_ball.x == 115
        assert fast_ball.y == 115