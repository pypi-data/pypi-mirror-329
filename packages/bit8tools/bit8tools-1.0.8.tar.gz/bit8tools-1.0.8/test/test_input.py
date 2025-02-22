"""
Módulo de pruebas para la clase Input en bit8tools.

Este módulo contiene funciones de pytest para probar las funcionalidades de la clase Input.
"""

from src.bit8tools.input import Input
from src.bit8tools.colors import Colors


def test_text(monkeypatch):
    """
    Prueba el método text de la clase Input.
    """
    monkeypatch.setattr('builtins.input', lambda _: "entrada de prueba")
    resultado = Input.text("Ingrese algo: ", Colors.RED, Colors.GREEN)
    assert resultado == "entrada de prueba"


def test_int_number(monkeypatch):
    """
    Prueba el método int_number de la clase Input.
    """
    monkeypatch.setattr('builtins.input', lambda _: "5")
    resultado = Input.int_number(
        "Ingrese un número: ", Colors.RED, Colors.GREEN, 1, 10)
    assert resultado == 5


def test_float_number(monkeypatch):
    """
    Prueba el método float_number de la clase Input.
    """
    monkeypatch.setattr('builtins.input', lambda _: "5.5")
    resultado = Input.float_number(
        "Ingrese un número flotante: ", Colors.RED, Colors.GREEN, 1.0, 10.0)
    assert resultado == 5.5


def test_yes_no(monkeypatch):
    """
    Prueba el método yes_no de la clase Input.
    """
    monkeypatch.setattr('builtins.input', lambda _: "s")
    resultado = Input.yes_no(
        "¿Está de acuerdo? (s/n): ", Colors.RED, Colors.GREEN)
    assert resultado is True

    monkeypatch.setattr('builtins.input', lambda _: "n")
    resultado = Input.yes_no(
        "¿Está de acuerdo? (s/n): ", Colors.RED, Colors.GREEN)
    assert resultado is False


def test_email(monkeypatch):
    """
    Prueba el método email de la clase Input.
    """
    monkeypatch.setattr('builtins.input', lambda _: "prueba@example.com")
    resultado = Input.email("Ingrese su email: ", Colors.RED, Colors.GREEN)
    assert resultado == "prueba@example.com"


def test_date(monkeypatch):
    """
    Prueba el método date de la clase Input.
    """
    monkeypatch.setattr('builtins.input', lambda _: "01/01/2020")
    resultado = Input.date(
        "Ingrese una fecha (dd/mm/yyyy): ", Colors.RED, Colors.GREEN)
    assert resultado == "01/01/2020"


def test_password(monkeypatch):
    """
    Prueba el método password de la clase Input.
    """
    monkeypatch.setattr('getpass.getpass', lambda _: "Contraseña1")
    resultado = Input.password(
        "Ingrese su contraseña: ", Colors.RED, Colors.GREEN)
    assert resultado == "Contraseña1"


def test_menu(monkeypatch):
    """
    Prueba el método menu de la clase Input.
    """
    monkeypatch.setattr('builtins.input', lambda _: "1")
    resultado = Input.menu("Elija una opción:", [
                           "Opción 1", "Opción 2"], Colors.RED, Colors.GREEN)
    assert resultado == 1


def test_invalid_int_number(monkeypatch):
    """
    Prueba el manejo de entrada inválida en el método int_number de la clase Input.
    """
    inputs = iter(["abc", "15", "5"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    resultado = Input.int_number(
        "Ingrese un número: ", Colors.RED, Colors.GREEN, 1, 10)
    assert resultado == 5


def test_invalid_float_number(monkeypatch):
    """
    Prueba el manejo de entrada inválida en el método float_number de la clase Input.
    """
    inputs = iter(["abc", "15.5", "5.5"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    resultado = Input.float_number(
        "Ingrese un número flotante: ", Colors.RED, Colors.GREEN, 1.0, 10.0)
    assert resultado == 5.5


def test_invalid_email(monkeypatch):
    """
    Prueba el manejo de entrada inválida en el método email de la clase Input.
    """
    inputs = iter(["prueba@", "prueba@example", "prueba@example.com"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    resultado = Input.email("Ingrese su email: ", Colors.RED, Colors.GREEN)
    assert resultado == "prueba@example.com"


def test_invalid_date(monkeypatch):
    """
    Prueba el manejo de entrada inválida en el método date de la clase Input.
    """
    inputs = iter(["32/13/2020", "01-01-2020", "01/01/2020"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    resultado = Input.date(
        "Ingrese una fecha (dd/mm/yyyy): ", Colors.RED, Colors.GREEN)
    assert resultado == "01/01/2020"


def test_invalid_password(monkeypatch):
    """
    Prueba el manejo de entrada inválida en el método password de la clase Input.
    """
    inputs = iter(["short", "nouppercase1", "NOLOWERCASE1",
                  "NoDigits", "Contraseña1"])
    monkeypatch.setattr('getpass.getpass', lambda _: next(inputs))
    resultado = Input.password(
        "Ingrese su contraseña: ", Colors.RED, Colors.GREEN)
    assert resultado == "Contraseña1"
