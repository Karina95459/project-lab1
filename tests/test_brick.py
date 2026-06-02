import pytest
import pygame
from brick import Brick

pygame.init()

# ===== ФІКСТУРИ =====
# фікстура — це заготовка об'єкта яку pytest автоматично передає в тест
@pytest.fixture
def red_brick():
    # створюємо звичайний блок який ще не знищений
    return Brick(0, 0, 60, 20, (255, 0, 0))

@pytest.fixture
def destroyed_brick():
    # створюємо блок і одразу знищуємо його
    # використовується у тестах де треба перевірити вже знищений блок
    b = Brick(0, 0, 60, 20, (255, 0, 0))
    b.destroy()
    return b

# ===== МАРКЕРИ =====
# маркер — це мітка для групи тестів
pytestmark = pytest.mark.brick


# ===== ТЕСТИ =====
def test_brick_initial_state(red_brick):
    # перевіряємо що новий блок не знищений
    # red_brick — це наша фікстура, pytest передає її автоматично
    assert red_brick.is_destroyed == False

def test_brick_color(red_brick):
    # перевіряємо що колір зберігся правильно
    assert red_brick.color == (255, 0, 0)