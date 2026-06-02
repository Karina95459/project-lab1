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