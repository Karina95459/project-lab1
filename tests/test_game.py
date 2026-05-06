import pytest

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