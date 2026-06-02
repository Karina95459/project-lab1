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
