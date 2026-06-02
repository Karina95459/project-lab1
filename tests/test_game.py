import pytest
from unittest import mock

from game import Game

@pytest.fixture
def game():
    return Game(800,600,60)

@pytest.mark.parametrize(
    "initial_state, expected_state",
    [
        (False, True),
        (True, False),
    ]
)

def test_toggle_pause(game, initial_state, expected_state):
    game.is_paused = initial_state
    game.toggle_pause()
    assert game.is_paused == expected_state

def test_restart_resets_game_states(game):
    game.is_paused = True
    game.is_win = True
    game.is_game_over = True

    game.restart()

    assert game.is_paused is False
    assert game.is_win is False
    assert game.is_game_over is False


def test_restart_calls_reset_methods(game):
    game.ball.reset = mock.MagicMock()
    game.platform.reset = mock.MagicMock()
    game.brick_manager.reset = mock.MagicMock()
    game.score_manager.reset = mock.MagicMock()

    game.restart()

    game.ball.reset.assert_called_once()
    game.platform.reset.assert_called_once()
    game.brick_manager.reset.assert_called_once()
    game.score_manager.reset.assert_called_once()