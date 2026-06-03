"""
Тести для класу Platform (Breakout/Arkanoid гра).

Використані інструменти pytest:
  - fixtures        : platform, edge_platform
  - parametrization : test_clamp_parametrized
  - mocking         : test_draw_calls_rect (unittest.mock.patch)
  - markers         : @pytest.mark.movement, @pytest.mark.collision,
                      @pytest.mark.rendering
"""

import pytest
from unittest.mock import MagicMock, patch
from paddle import Platform


# ---------------------------------------------------------------------------
# Маркери
# ---------------------------------------------------------------------------
def pytest_configure(config):
    config.addinivalue_line("markers", "movement: тести руху платформи")
    config.addinivalue_line("markers", "collision: тести меж і колізій")
    config.addinivalue_line("markers", "rendering: тести відмалювання")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def platform():
    """Стандартна платформа в нижній частині екрану."""
    return Platform(x=350, y=550, height=20, width=100, speed=10)


@pytest.fixture
def edge_platform():
    """Платформа біля лівого краю екрану."""
    return Platform(x=0, y=550, height=20, width=100, speed=15)


# ---------------------------------------------------------------------------
# Тести ініціалізації
# ---------------------------------------------------------------------------
class TestInit:
    def test_initial_position(self, platform):
        assert platform.x == 350
        assert platform.y == 550

    def test_size_stored(self, platform):
        assert platform.width == 100
        assert platform.height == 20

    def test_start_position_saved(self, platform):
        assert platform.start_x == 350
        assert platform.start_y == 550


# ---------------------------------------------------------------------------
# Тести руху
# ---------------------------------------------------------------------------
@pytest.mark.movement
class TestMove:
    def test_move_right(self, platform):
        platform.move_right()
        assert platform.x == 360  # 350 + 10

    def test_move_left(self, platform):
        platform.move_left()
        assert platform.x == 340  # 350 - 10

    def test_move_right_multiple(self, platform):
        for _ in range(3):
            platform.move_right()
        assert platform.x == 380  # 350 + 30

    def test_move_does_not_change_y(self, platform):
        platform.move_right()
        platform.move_left()
        assert platform.y == 550

      
# ---------------------------------------------------------------------------
# Тести clamp — параметризація
# ---------------------------------------------------------------------------
@pytest.mark.collision
@pytest.mark.parametrize("x,screen_width,expected", [
    (-50, 800, 0),     # вилазить за лівий край → 0
    (-1, 800, 0),      # трохи за лівим краєм → 0
    (750, 800, 700),   # 750 + 100 = 850 > 800 → 700
    (800, 800, 700),   # повністю за правим краєм → 700
    (350, 800, 350),   # в межах → не змінюється
])
def test_clamp_parametrized(x, screen_width, expected):
    p = Platform(x=x, y=0, height=20, width=100, speed=10)
    p.clamp(screen_width)
    assert p.x == expected


@pytest.mark.collision
class TestClamp:
    def test_clamp_after_move_left(self, edge_platform):
        # edge_platform на x=0, рух вліво виводить за межі
        edge_platform.move_left()
        edge_platform.clamp(800)
        assert edge_platform.x == 0

    def test_clamp_keeps_valid_position(self, platform):
        platform.clamp(800)
        assert platform.x == 350  # було в межах — лишилось як є


# ---------------------------------------------------------------------------
# Тести get_rect
# ---------------------------------------------------------------------------
@pytest.mark.collision
class TestGetRect:
    def test_rect_position(self, platform):
        rect = platform.get_rect()
        assert rect.x == 350
        assert rect.y == 550

    def test_rect_size(self, platform):
        rect = platform.get_rect()
        assert rect.width == 100
        assert rect.height == 20

    def test_rect_type(self, platform):
        import pygame
        assert isinstance(platform.get_rect(), pygame.Rect)

      
# ---------------------------------------------------------------------------
# Тести draw — mocking
# ---------------------------------------------------------------------------
@pytest.mark.rendering
class TestDraw:
    @patch("paddle.pygame.draw.rect")
    def test_draw_calls_rect(self, mock_rect, platform):
        """Перевіряємо, що draw() викликає pygame.draw.rect з правильними аргументами."""
        mock_screen = MagicMock()
        platform.draw(mock_screen)
        mock_rect.assert_called_once_with(
            mock_screen,
            platform.color,
            (platform.x, platform.y, platform.width, platform.height),
        )

    @patch("paddle.pygame.draw.rect")
    def test_draw_called_once(self, mock_rect, platform):
        mock_screen = MagicMock()
        platform.draw(mock_screen)
        assert mock_rect.call_count == 1

    @patch("paddle.pygame.draw.rect")
    def test_draw_position_after_move(self, mock_rect, platform):
        """Після move_right() малюємо на новій позиції."""
        platform.move_right()
        mock_screen = MagicMock()
        platform.draw(mock_screen)
        _, args, _ = mock_rect.mock_calls[0]
        rect_tuple = args[2]
        assert rect_tuple == (platform.x, platform.y, platform.width, platform.height)


# ---------------------------------------------------------------------------
# Тести reset
# ---------------------------------------------------------------------------
class TestReset:
    def test_reset_restores_position(self, platform):
        platform.move_right()
        platform.move_right()
        platform.reset()
        assert platform.x == 350
        assert platform.y == 550

    def test_reset_after_move_left(self, platform):
        platform.move_left()
        platform.reset()
        assert platform.x == 350

    def test_reset_idempotent(self, platform):
        platform.reset()
        platform.reset()
        assert platform.x == 350
        assert platform.y == 550
      
