"""
Módulo de pruebas para la clase Colors del módulo bit8tools.colors.

Este módulo contiene pruebas unitarias para verificar el correcto funcionamiento
de las funciones de la clase Colors utilizando pytest.

Funciones:
- test_colorize_red: Prueba la función colorize con el color rojo.
- test_colorize_invalid_color: Prueba la función colorize con un color inválido.
- test_bold: Prueba la función bold.
- test_underline: Prueba la función underline.
- test_validate_color_valid: Prueba la función validate_color con un color válido.
- test_validate_color_invalid: Prueba la función validate_color con un color inválido.
- test_colorize_green: Prueba la función colorize con el color verde.
- test_colorize_blue: Prueba la función colorize con el color azul.
- test_colorize_combined_styles: Prueba la combinación de estilos bold y underline con color.
"""

import pytest
from src.bit8tools.colors import Colors


def test_colorize_red():
    """Prueba la función colorize con el color rojo."""
    assert Colors.colorize("test", Colors.RED) == "\033[91mtest\033[0m"


def test_colorize_invalid_color():
    """Prueba la función colorize con un color inválido."""
    assert Colors.colorize("test", "invalid_color") == "\033[0mtest\033[0m"


def test_bold():
    """Prueba la función bold."""
    assert Colors.bold("test") == "\033[1mtest\033[0m"


def test_underline():
    """Prueba la función underline."""
    assert Colors.underline("test") == "\033[4mtest\033[0m"


def test_validate_color_valid():
    """Prueba la función validate_color con un color válido."""
    assert Colors.validate_color(Colors.GREEN) == Colors.GREEN


def test_validate_color_invalid():
    """Prueba la función validate_color con un color inválido."""
    assert Colors.validate_color("invalid_color") == Colors.DEFAULT


def test_colorize_green():
    """Prueba la función colorize con el color verde."""
    assert Colors.colorize("test", Colors.GREEN) == "\033[92mtest\033[0m"


def test_colorize_blue():
    """Prueba la función colorize con el color azul."""
    assert Colors.colorize("test", Colors.BLUE) == "\033[94mtest\033[0m"


def test_colorize_combined_styles():
    """Prueba la combinación de estilos bold y underline con color."""
    combined_text = Colors.colorize(Colors.bold(
        Colors.underline("test")), Colors.MAGENTA)
    assert combined_text == "\033[95m\033[1m\033[4mtest\033[0m\033[0m\033[0m"


def test_colorize_yellow():
    """Prueba la función colorize con el color amarillo."""
    assert Colors.colorize("test", Colors.YELLOW) == "\033[93mtest\033[0m"


def test_colorize_cyan():
    """Prueba la función colorize con el color cian."""
    assert Colors.colorize("test", Colors.CYAN) == "\033[96mtest\033[0m"


def test_colorize_white():
    """Prueba la función colorize con el color blanco."""
    assert Colors.colorize("test", Colors.WHITE) == "\033[97mtest\033[0m"


if __name__ == "__main__":
    pytest.main()
