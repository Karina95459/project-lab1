"""
Тести для класу ScoreManager (Breakout/Arkanoid гра).

Використані інструменти pytest:
  - fixtures        : manager
  - parametrization : test_add_parametrized
  - mocking         : pygame.font.Font, font.render (unittest.mock.patch)
  - markers         : @pytest.mark.scoring, @pytest.mark.rendering
"""

import pytest
from unittest.mock import MagicMock, patch
from score_manager import ScoreManager


# ---------------------------------------------------------------------------
# Маркери
# ---------------------------------------------------------------------------
def pytest_configure(config):
    config.addinivalue_line("markers", "scoring: тести підрахунку очок")
    config.addinivalue_line("markers", "rendering: тести відмалювання")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def manager():
    """ScoreManager із мокнутим шрифтом (без ініціалізації pygame)."""
    with patch("score_manager.pygame.font.Font"):
        return ScoreManager()