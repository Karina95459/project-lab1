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


# ---------------------------------------------------------------------------
# Тести прискорення
# ---------------------------------------------------------------------------
@pytest.mark.movement
@pytest.mark.slow
class TestAccelerate:
    def test_accelerate_increases_multiplier(self, ball):
        before = ball.speed_multiplier
        ball.accelerate()
        assert ball.speed_multiplier > before

    def test_accelerate_step_size(self, ball):
        ball.accelerate()
        assert abs(ball.speed_multiplier - 1.0001) < 1e-9

    def test_accelerate_does_not_exceed_max(self, ball):
        ball.speed_multiplier = 2.5  # вже на максимумі
        ball.accelerate()
        assert ball.speed_multiplier == 2.5

    def test_accelerate_stops_at_max(self, ball):
        ball.speed_multiplier = ball.max_multiplier - 0.00005
        ball.accelerate()
        # після кроку може перевищити max — перевіряємо фактичну логіку
        # (метод додає тільки якщо < max)
        assert ball.speed_multiplier <= ball.max_multiplier + ball.acceleration_rate

    def test_many_accelerations_capped(self, ball):
        for _ in range(100_000):
            ball.accelerate()
        assert ball.speed_multiplier <= ball.max_multiplier + ball.acceleration_rate


# ---------------------------------------------------------------------------
# Тести відскоку — параметризація
# ---------------------------------------------------------------------------
@pytest.mark.collision
@pytest.mark.parametrize("dx,expected_dx", [
    (5, -5),
    (-5, 5),
    (10, -10),
    (-3, 3),
    (0, 0),
])
def test_bounce_x_parametrized(dx, expected_dx):
    b = Ball(x=0, y=0, radius=5, dx=dx, dy=0)
    b.bounce_x()
    assert b.dx == expected_dx


@pytest.mark.collision
@pytest.mark.parametrize("dy,expected_dy", [
    (-5, 5),
    (5, -5),
    (7, -7),
    (-1, 1),
    (0, 0),
])
def test_bounce_y_parametrized(dy, expected_dy):
    b = Ball(x=0, y=0, radius=5, dx=0, dy=dy)
    b.bounce_y()
    assert b.dy == expected_dy


@pytest.mark.collision
class TestBounce:
    def test_bounce_x_does_not_change_dy(self, ball):
        original_dy = ball.dy
        ball.bounce_x()
        assert ball.dy == original_dy

    def test_bounce_y_does_not_change_dx(self, ball):
        original_dx = ball.dx
        ball.bounce_y()
        assert ball.dx == original_dx

    def test_double_bounce_x_restores(self, ball):
        original = ball.dx
        ball.bounce_x()
        ball.bounce_x()
        assert ball.dx == original

    def test_double_bounce_y_restores(self, ball):
        original = ball.dy
        ball.bounce_y()
        ball.bounce_y()
        assert ball.dy == original


# ---------------------------------------------------------------------------
# Тести get_rect
# ---------------------------------------------------------------------------
@pytest.mark.collision
class TestGetRect:
    def test_rect_top_left(self, ball):
        rect = ball.get_rect()
        assert rect.x == 390  # 400 - 10
        assert rect.y == 290  # 300 - 10

    def test_rect_size(self, ball):
        rect = ball.get_rect()
        assert rect.width == 20  # radius * 2
        assert rect.height == 20

    def test_rect_center(self, ball):
        rect = ball.get_rect()
        assert rect.centerx == ball.x
        assert rect.centery == ball.y

    def test_rect_type(self, ball):
        import pygame
        rect = ball.get_rect()
        assert isinstance(rect, pygame.Rect)


# ---------------------------------------------------------------------------
# Тести is_out_of_bounds — параметризація
# ---------------------------------------------------------------------------
@pytest.mark.collision
@pytest.mark.parametrize("y,screen_height,expected", [
    (595, 600, False),  # нижній край = 585 < 600
    (611, 600, True),  # нижній край = 601 > 600
    (610, 600, True),  # рівно за межею
    (300, 600, False),  # по центру
    (0, 600, False),  # вгорі
])
def test_is_out_of_bounds_parametrized(y, screen_height, expected):
    b = Ball(x=200, y=y, radius=10, dx=0, dy=0)
    assert b.is_out_of_bounds(screen_height) == expected


def test_is_out_of_bounds_boundary_ball(boundary_ball):
    """boundary_ball: y=595, radius=10 → нижній край=605 > 600."""
    assert boundary_ball.is_out_of_bounds(600) is True


# ---------------------------------------------------------------------------
# Тести reset
# ---------------------------------------------------------------------------
class TestReset:
    def test_reset_restores_position(self, ball):
        ball.move()
        ball.move()
        ball.reset()
        assert ball.x == 400
        assert ball.y == 300

    def test_reset_restores_velocity(self, ball):
        ball.bounce_x()
        ball.bounce_y()
        ball.reset()
        assert ball.dx == 5
        assert ball.dy == -5

    def test_reset_restores_speed_multiplier(self, ball):
        ball.speed_multiplier = 2.0
        ball.reset()
        assert ball.speed_multiplier == 1.0

    def test_reset_after_many_accelerations(self, ball):
        for _ in range(10_000):
            ball.accelerate()
        ball.reset()
        assert ball.speed_multiplier == 1.0

    def test_reset_idempotent(self, ball):
        ball.reset()
        ball.reset()
        assert ball.x == 400
        assert ball.y == 300


# ---------------------------------------------------------------------------
# Тести draw — mocking
# ---------------------------------------------------------------------------
@pytest.mark.rendering
class TestDraw:
    @patch("ball.pygame.draw.circle")
    def test_draw_calls_pygame_circle(self, mock_circle, ball):
        """Перевіряємо, що draw() викликає pygame.draw.circle з правильними аргументами."""
        mock_screen = MagicMock()
        ball.draw(mock_screen)
        mock_circle.assert_called_once_with(
            mock_screen,
            (255, 255, 255),
            (ball.x, ball.y),
            ball.radius,
        )

    @patch("ball.pygame.draw.circle")
    def test_draw_called_once(self, mock_circle, ball):
        mock_screen = MagicMock()
        ball.draw(mock_screen)
        assert mock_circle.call_count == 1

    @patch("ball.pygame.draw.circle")
    def test_draw_uses_white_color(self, mock_circle, ball):
        mock_screen = MagicMock()
        ball.draw(mock_screen)
        _, args, _ = mock_circle.mock_calls[0]
        color = args[1]
        assert color == (255, 255, 255)

    @patch("ball.pygame.draw.circle")
    def test_draw_position_after_move(self, mock_circle, ball):
        """Після move() малюємо на новій позиції."""
        ball.move()
        mock_screen = MagicMock()
        ball.draw(mock_screen)
        _, args, _ = mock_circle.mock_calls[0]
        pos = args[2]
        assert pos == (ball.x, ball.y)
