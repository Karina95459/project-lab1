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


def test_check_paddle_collision_bounces_when_ball_hits_paddle(game):
    game.ball.bounce_y = mock.MagicMock()

    ball_rect = mock.MagicMock()
    ball_rect.colliderect.return_value = True

    game.ball.get_rect = mock.MagicMock(return_value=ball_rect)
    game.platform.get_rect = mock.MagicMock(return_value=mock.MagicMock())

    game.ball.dy = 5

    game.check_paddle_collision()

    game.ball.bounce_y.assert_called_once()
    assert game.ball.y == game.platform.y - game.ball.radius


def test_check_paddle_collision_does_not_bounce_when_ball_moves_up(game):
    game.ball.bounce_y = mock.MagicMock()

    ball_rect = mock.MagicMock()
    ball_rect.colliderect.return_value = True

    game.ball.get_rect = mock.MagicMock(return_value=ball_rect)
    game.platform.get_rect = mock.MagicMock(return_value=mock.MagicMock())

    game.ball.dy = -5

    game.check_paddle_collision()

    game.ball.bounce_y.assert_not_called()


def test_check_paddle_collision_does_not_bounce_without_collision(game):
    game.ball.bounce_y = mock.MagicMock()

    ball_rect = mock.MagicMock()
    ball_rect.colliderect.return_value = False

    game.ball.get_rect = mock.MagicMock(return_value=ball_rect)
    game.platform.get_rect = mock.MagicMock(return_value=mock.MagicMock())

    game.ball.dy = 5

    game.check_paddle_collision()

    game.ball.bounce_y.assert_not_called()


def test_init_objects_creates_game_objects(game):
    assert game.ball is not None
    assert game.platform is not None
    assert game.brick_manager is not None


def test_init_objects_sets_start_positions(game):
    expected_platform_x = (game.width - 100) // 2
    expected_platform_y = game.height - 40

    assert game.platform.x == expected_platform_x
    assert game.platform.y == expected_platform_y
    assert game.ball.y == game.platform.y - game.ball.radius - 2


def test_update_calls_required_methods(game):
    game.ball.move = mock.MagicMock()
    game.ball.accelerate = mock.MagicMock()
    game.check_wall_collisions = mock.MagicMock()
    game.check_paddle_collision = mock.MagicMock()
    game.brick_manager.check_collision = mock.MagicMock(return_value=0)
    game.score_manager.add = mock.MagicMock()
    game.ball.is_out_of_bounds = mock.MagicMock(return_value=False)
    game.brick_manager.all_destroyed = mock.MagicMock(return_value=False)

    game.update()

    game.ball.move.assert_called_once()
    game.ball.accelerate.assert_called_once()
    game.check_wall_collisions.assert_called_once()
    game.check_paddle_collision.assert_called_once()
    game.brick_manager.check_collision.assert_called_once_with(game.ball)
    game.score_manager.add.assert_called_once_with(0)


def test_update_sets_game_over_when_ball_out_of_bounds(game):
    game.ball.is_out_of_bounds = mock.MagicMock(return_value=True)
    game.brick_manager.all_destroyed = mock.MagicMock(return_value=False)

    game.update()

    assert game.is_game_over is True
    assert game.is_win is False


def test_update_sets_win_when_all_bricks_destroyed(game):
    game.ball.is_out_of_bounds = mock.MagicMock(return_value=False)
    game.brick_manager.all_destroyed = mock.MagicMock(return_value=True)

    game.update()

    assert game.is_win is True
    assert game.is_game_over is False


@pytest.mark.parametrize(
    "is_game_over, is_win",
    [
        (True, False),
        (False, True),
    ]
)
def test_update_returns_when_game_finished(game, is_game_over, is_win):
    game.is_game_over = is_game_over
    game.is_win = is_win
    game.ball.move = mock.MagicMock()

    game.update()

    game.ball.move.assert_not_called()