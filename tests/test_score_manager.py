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


class TestScoreManagerDraw:
    """Тести для методу draw ScoreManager"""

    def test_draw_renders_score_text(self, score_manager):
        """draw повинен рендерити текст score"""
        score_manager.score = 100
        mock_screen = Mock()
        with patch.object(score_manager.font, 'render') as mock_render:
            mock_render.return_value = Mock()
            score_manager.draw(mock_screen)
            assert mock_render.called

    def test_draw_renders_high_score_text(self, score_manager):
        """draw повинен рендерити текст high_score"""
        score_manager.high_score = 250
        mock_screen = Mock()
        with patch.object(score_manager.font, 'render') as mock_render:
            mock_render.return_value = Mock()
            score_manager.draw(mock_screen)
            assert mock_render.call_count >= 2

    def test_draw_calls_blit_twice(self, score_manager):
        """draw повинен викликати blit два рази (для score та high_score)"""
        mock_screen = Mock()
        with patch.object(score_manager.font, 'render') as mock_render:
            mock_render.return_value = Mock()
            score_manager.draw(mock_screen)
            assert mock_screen.blit.call_count == 2

    def test_draw_blit_positions(self, score_manager):
        """draw повинен вмістити текст на позиціях (10, 10) та (10, 40)"""
        mock_screen = Mock()
        with patch.object(score_manager.font, 'render') as mock_render:
            mock_render.return_value = Mock()
            score_manager.draw(mock_screen)
            calls = mock_screen.blit.call_args_list
            assert len(calls) == 2
            assert calls[0][0][1] == (10, 10)
            assert calls[1][0][1] == (10, 40)

    @pytest.mark.parametrize("score,high_score", [
        (0, 0),
        (50, 50),
        (100, 200),
        (500, 1000),
        (999, 1234),
    ])
    def test_draw_with_various_scores(self, score_manager, score, high_score):
        """Параметризований тест для draw з різними значеннями очок"""
        score_manager.score = score
        score_manager.high_score = high_score
        mock_screen = Mock()
        with patch.object(score_manager.font, 'render') as mock_render:
            mock_render.return_value = Mock()
            score_manager.draw(mock_screen)
            assert mock_screen.blit.call_count == 2

    def test_draw_score_text_content(self, score_manager):
        """draw повинен рендерити правильний текст для score"""
        score_manager.score = 42
        mock_screen = Mock()
        with patch.object(score_manager.font, 'render') as mock_render:
            mock_render.return_value = Mock()
            score_manager.draw(mock_screen)
            calls = mock_render.call_args_list
            score_text = calls[0][0][0]
            assert "Score:" in score_text
            assert "42" in score_text

    def test_draw_high_score_text_content(self, score_manager):
        """draw повинен рендерити правильний текст для high_score"""
        score_manager.high_score = 999
        mock_screen = Mock()
        with patch.object(score_manager.font, 'render') as mock_render:
            mock_render.return_value = Mock()
            score_manager.draw(mock_screen)
            calls = mock_render.call_args_list
            high_score_text = calls[1][0][0]
            assert "Best:" in high_score_text
            assert "999" in high_score_text

    def test_draw_render_color_score(self, score_manager):
        """draw повинен рендерити score зеленим кольором (0, 255, 0)"""
        mock_screen = Mock()
        with patch.object(score_manager.font, 'render') as mock_render:
            mock_render.return_value = Mock()
            score_manager.draw(mock_screen)
            calls = mock_render.call_args_list
            score_color = calls[0][0][2]
            assert score_color == (0, 255, 0)

    def test_draw_render_color_high_score(self, score_manager):
        """draw повинен рендерити high_score жовтим кольором (200, 200, 0)"""
        mock_screen = Mock()
        with patch.object(score_manager.font, 'render') as mock_render:
            mock_render.return_value = Mock()
            score_manager.draw(mock_screen)
            calls = mock_render.call_args_list
            high_score_color = calls[1][0][2]
            assert high_score_color == (200, 200, 0)

    def test_draw_does_not_modify_state(self, score_manager):
        """draw не повинен змінювати стан ScoreManager"""
        score_manager.score = 100
        score_manager.high_score = 200
        original_score = score_manager.score
        original_high_score = score_manager.high_score

        mock_screen = Mock()
        with patch.object(score_manager.font, 'render') as mock_render:
            mock_render.return_value = Mock()
            score_manager.draw(mock_screen)

        assert score_manager.score == original_score
        assert score_manager.high_score == original_high_score