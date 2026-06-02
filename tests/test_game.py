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


def test_check_wall_collision_left_wall(game):
    game.ball.bounce_x = mock.MagicMock()
    game.ball.x = 5

    game.check_wall_collisions()

    game.ball.bounce_x.assert_called_once()
    assert game.ball.x == game.ball.radius


def test_check_wall_collision_right_wall(game):
    game.ball.bounce_x = mock.MagicMock()
    game.ball.x = game.width - 5

    game.check_wall_collisions()

    game.ball.bounce_x.assert_called_once()
    assert game.ball.x == game.width - game.ball.radius


def test_check_wall_collision_top_wall(game):
    game.ball.bounce_y = mock.MagicMock()
    game.ball.y = 5

    game.check_wall_collisions()

    game.ball.bounce_y.assert_called_once()
    assert game.ball.y == game.ball.radius


def test_check_wall_collision_no_collision(game):
    game.ball.bounce_x = mock.MagicMock()
    game.ball.bounce_y = mock.MagicMock()

    original_x = game.ball.x
    original_y = game.ball.y

    game.check_wall_collisions()

    game.ball.bounce_x.assert_not_called()
    game.ball.bounce_y.assert_not_called()
    assert game.ball.x == original_x
    assert game.ball.y == original_y