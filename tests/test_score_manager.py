import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from unittest.mock import patch, Mock
from score_manager import ScoreManager


@pytest.fixture
def score_manager():
    """Фікстура для створення менеджера очок з мокованим pygame"""
    with patch('score_manager.pygame.font.Font'):
        sm = ScoreManager()
    return sm


class TestScoreManagerAdd:
    """Тести для додавання очків"""

    def test_add_single_points(self, score_manager):
        """add повинен додати очки до score"""
        score_manager.add(10)
        assert score_manager.score == 10

    def test_add_multiple_times(self, score_manager):
        """Багаторазове додавання очків повинно накопичуватися"""
        score_manager.add(10)
        score_manager.add(20)
        score_manager.add(30)
        assert score_manager.score == 60

    @pytest.mark.parametrize("points", [1, 5, 10, 50, 100, 500])
    def test_add_various_points(self, score_manager, points):
        """Параметризований тест для додавання різних кількостей очків"""
        score_manager.add(points)
        assert score_manager.score == points

    def test_add_zero_points(self, score_manager):
        """Додавання 0 очків не повинно змінювати score"""
        initial_score = score_manager.score
        score_manager.add(0)
        assert score_manager.score == initial_score

    def test_add_negative_points(self, score_manager):
        """Додавання від'ємних очків повинно зменшити score"""
        score_manager.add(100)
        score_manager.add(-30)
        assert score_manager.score == 70

    def test_add_updates_high_score_when_exceeds(self, score_manager):
        """add повинен оновити high_score, якщо score його перевищує"""
        score_manager.add(50)
        assert score_manager.high_score == 50

    def test_add_updates_high_score_multiple_times(self, score_manager):
        """high_score повинен оновлюватися при кожному новому максимумі"""
        score_manager.add(30)
        assert score_manager.high_score == 30
        score_manager.add(40)
        assert score_manager.high_score == 70
        # Скидаємо score, щоб додати менше чим high_score
        score_manager.reset()
        score_manager.add(20)
        assert score_manager.high_score == 70  # не змінюється

    def test_add_does_not_lower_high_score(self, score_manager):
        """Додавання очків не повинно знижувати high_score"""
        score_manager.add(100)
        initial_high_score = score_manager.high_score
        score_manager.add(-50)
        assert score_manager.high_score == initial_high_score

    @pytest.mark.parametrize("add_sequence,expected_score,expected_high_score", [
        ([10, 20, 30], 60, 60),
        ([50, -20, 30], 60, 60),
        ([100], 100, 100),
        ([50, 100, 20], 170, 170),
        ([30, 30, 30], 90, 90),
    ])
    def test_add_parametrized_sequences(self, score_manager, add_sequence, expected_score, expected_high_score):
        """Параметризований тест для послідовностей додавання"""
        for points in add_sequence:
            score_manager.add(points)
        assert score_manager.score == expected_score
        assert score_manager.high_score == expected_high_score


class TestScoreManagerReset:
    """Тести для скидання очок"""

    def test_reset_basic(self, score_manager):
        """reset повинен встановити score на 0"""
        score_manager.add(100)
        score_manager.reset()
        assert score_manager.score == 0

    def test_reset_does_not_affect_high_score(self, score_manager):
        """reset не повинен змінювати high_score"""
        score_manager.add(100)
        score_manager.reset()
        assert score_manager.high_score == 100

    def test_reset_after_multiple_adds(self, score_manager):
        """reset повинен скинути score після багатьох додавань"""
        score_manager.add(30)
        score_manager.add(40)
        score_manager.add(50)
        score_manager.reset()
        assert score_manager.score == 0

    def test_reset_allows_score_to_exceed_high_score_again(self, score_manager):
        """Після reset можна знову набрати більше за high_score"""
        score_manager.add(50)
        score_manager.reset()
        score_manager.add(100)
        assert score_manager.score == 100
        assert score_manager.high_score == 100

    def test_reset_multiple_times(self, score_manager):
        """reset можна викликати кілька разів"""
        score_manager.add(50)
        score_manager.reset()
        score_manager.add(30)
        score_manager.reset()
        score_manager.add(80)
        score_manager.reset()
        assert score_manager.score == 0
        assert score_manager.high_score == 80