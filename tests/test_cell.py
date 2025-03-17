import pytest
import pygame
from cell import Cell  # Імпорт класу з cell.py

@pytest.fixture
def cell():
    """Fixture для створення об'єкта клітинки."""
    return Cell(0, 0, 32, 32, (0, 0, 0))  # Припустимо, що (0, 0) — це координати, а 32 — це розмір клітинки

def test_cell_coordinates(cell):
    """Тестуємо координати клітинки."""
    assert cell.abs_x == 0
    assert cell.abs_y == 0