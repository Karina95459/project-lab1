import pytest
import pygame
from unittest.mock import MagicMock
from brick_manager import BrickManager

pygame.init()


# ===== ФІКСТУРИ =====
@pytest.fixture
def manager():
    # створюємо BrickManager з 3 рядками і 4 колонками
    # і одразу викликаємо create_level() щоб заповнити список блоків
    bm = BrickManager(rows=3, cols=4, start_y=60, start_x=40, gap=6)
    bm.create_level()
    return bm


# ===== МАРКЕРИ =====
# всі тести у цьому файлі отримують мітку brick_manager
# запустити тільки їх: pytest -m brick_manager
pytestmark = pytest.mark.brick_manager


# ===== ТЕСТИ =====
def test_create_level_count(manager):
    # перевіряємо що після create_level кількість блоків = rows * cols
    # у нашому випадку 3 * 4 = 12
    assert len(manager.bricks) == 3 * 4


# ===== ПАРАМЕТРИЗАЦІЯ =====
# перевіряємо create_level для різних розмірів поля
# pytest запустить цей тест тричі з різними rows і cols
@pytest.mark.parametrize("rows, cols", [
    (1, 1),   # мінімальне поле — 1 блок
    (3, 4),   # середнє поле — 12 блоків
    (5, 11),  # повне поле як у грі — 55 блоків
])
def test_create_level_parametrized(rows, cols):
    # створюємо менеджер з переданими розмірами
    bm = BrickManager(rows=rows, cols=cols, start_y=60, start_x=40, gap=6)
    bm.create_level()
    # перевіряємо що кількість блоків відповідає rows * cols
    assert len(bm.bricks) == rows * cols


def test_all_destroyed_false(manager):
    # на початку жоден блок не знищений
    # тому all_destroyed() має повертати False
    assert manager.all_destroyed() is False


def test_all_destroyed_true(manager):
    # знищуємо всі блоки вручну
    for brick in manager.bricks:
        brick.destroy()
    # тепер all_destroyed() має повертати True
    assert manager.all_destroyed() is True


def test_reset(manager):
    # знищуємо всі блоки
    for brick in manager.bricks:
        brick.destroy()
    # викликаємо reset() — він має створити нові блоки
    manager.reset()
    # перевіряємо що блоки знову не знищені
    assert manager.all_destroyed() is False
    # і що їх кількість знову правильна
    assert len(manager.bricks) == 3 * 4


# ===== МОКУВАННЯ =====
# мокування — підміняємо реальний об'єкт фейковим
# нам не треба створювати справжній Ball з pygame
# MagicMock() створює об'єкт який може імітувати будь який метод
# ми самі кажемо що має повертати get_rect()
def test_check_collision_no_hit(manager):
    # створюємо фейковий м'яч
    mock_ball = MagicMock()
    # кажемо що get_rect() повертає прямокутник далеко від всіх блоків
    mock_ball.get_rect.return_value = pygame.Rect(9999, 9999, 10, 10)
    # перевіряємо що score = 0 бо зіткнення не було
    score = manager.check_collision(mock_ball)
    assert score == 0


def test_check_collision_hit(manager):
    # беремо перший блок щоб знати його точні координати
    first_brick = manager.bricks[0]
    # створюємо фейковий м'яч
    mock_ball = MagicMock()
    # кажемо що get_rect() повертає прямокутник точно на першому блоці
    mock_ball.get_rect.return_value = pygame.Rect(first_brick.x, first_brick.y, 10, 10)
    # перевіряємо що score = 10 бо один блок знищено
    score = manager.check_collision(mock_ball)
    assert score == 10
    # і що блок справді знищений
    assert first_brick.is_destroyed is True
