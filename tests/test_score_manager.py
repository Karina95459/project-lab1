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

# ---------------------------------------------------------------------------
# Тести ініціалізації
# ---------------------------------------------------------------------------
class TestInit:
    def test_initial_score(self, manager):
        assert manager.score == 0

    def test_initial_high_score(self, manager):
        assert manager.high_score == 0

    def test_font_created(self):
        """Перевіряємо, що шрифт створюється з правильними параметрами."""
        with patch("score_manager.pygame.font.Font") as mock_font:
            ScoreManager()
            mock_font.assert_called_once_with(None, 36)

# ---------------------------------------------------------------------------
# Тести add
# ---------------------------------------------------------------------------
@pytest.mark.scoring
class TestAdd:
    def test_add_increases_score(self, manager):
        manager.add(10)
        assert manager.score == 10

    def test_add_multiple(self, manager):
        manager.add(10)
        manager.add(5)
        assert manager.score == 15

    def test_add_updates_high_score(self, manager):
        manager.add(50)
        assert manager.high_score == 50


@pytest.mark.scoring
@pytest.mark.parametrize("points,expected", [
    (10, 10),
    (0, 0),
    (100, 100),
    (1, 1),
])
def test_add_parametrized(manager, points, expected):
    manager.add(points)
    assert manager.score == expected