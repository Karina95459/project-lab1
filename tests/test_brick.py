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

def test_destroy(red_brick):
    # викликаємо destroy() і перевіряємо що is_destroyed стало True
    red_brick.destroy()
    assert red_brick.is_destroyed == True

def test_already_destroyed(destroyed_brick):
    # перевіряємо фікстуру destroyed_brick — вона вже має бути знищена
    assert destroyed_brick.is_destroyed == True

# ===== ПАРАМЕТРИЗАЦІЯ =====
# параметризація — запускає один тест кілька разів з різними даними
@pytest.mark.parametrize("x, y, width, height", [
    (0, 0, 60, 20),      # стандартний блок у лівому куті
    (100, 200, 80, 30),  # блок з іншими координатами і розміром
    (50, 50, 60, 20),    # блок десь посередині
])
def test_get_rect(x, y, width, height):
    # створюємо блок з переданими координатами
    b = Brick(x, y, width, height, (255, 0, 0))
    # отримуємо його прямокутник
    rect = b.get_rect()
    # перевіряємо що прямокутник має правильні координати і розміри
    assert rect.x == x
    assert rect.y == y
    assert rect.width == width
    assert rect.height == height