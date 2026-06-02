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
