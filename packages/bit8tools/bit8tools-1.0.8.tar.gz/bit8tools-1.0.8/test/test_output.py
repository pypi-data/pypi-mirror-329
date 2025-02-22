"""
Pruebas unitarias para el módulo Output
"""

import locale
import os
from src.bit8tools.output import Output
from src.bit8tools.colors import Colors


def test_clear(monkeypatch):
    """Test para la función clear."""
    monkeypatch.setattr('os.system', lambda x: None)
    Output.clear()
    # Expected output: Console is cleared


def test_get_console_size(monkeypatch):
    """Test para la función get_console_size."""
    monkeypatch.setattr('os.get_terminal_size',
                        lambda: os.terminal_size((80, 24)))
    size = Output.get_console_size()
    assert isinstance(size, tuple)
    assert len(size) == 2


def test_show_warning(monkeypatch):
    """Test para la función show_warning."""
    monkeypatch.setattr('builtins.input', lambda _: 's')
    assert Output.show_warning("This is a warning message") is True
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    assert Output.show_warning("This is a warning message") is False


def test_confirm(monkeypatch):
    """Test para la función confirm."""
    monkeypatch.setattr('builtins.input', lambda _: 's')
    assert Output.confirm("Are you sure?") is True
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    assert Output.confirm("Are you sure?") is False


def test_typewriter_effect(monkeypatch, capsys):
    """Test para el efecto de escritura."""
    monkeypatch.setattr('time.sleep', lambda _: None)
    Output.typewriter_effect("Typing effect")
    captured = capsys.readouterr()
    assert "Typing effect" in captured.out


def test_set_locale():
    """Test para la función set_locale."""
    Output.set_locale('en_US.UTF-8')
    assert locale.getlocale() == ('en_US', 'UTF-8')


def test_format_int():
    """Test para la función format_int."""
    assert Output.format_int(1000) == '1,000'


def test_format_float():
    """Test para la función format_float."""
    assert Output.format_float(1234.56) == '1,234.56'


def test_format_currency():
    """Test para la función format_currency."""
    assert Output.format_currency(1234.56) == '$1,234.56'


def test_format_percentage():
    """Test para la función format_percentage."""
    assert Output.format_percentage(99.99) == '99.99%'


def test_format_date():
    """Test para la función format_date."""
    locale.setlocale(locale.LC_TIME, "es_AR.UTF-8")  # Simula locale argentino
    assert Output.format_date('2023-10-01') == '1/10/2023\n'  # Depende del locale

def test_print_title(capsys):
    """Test para la función print_title."""
    Output.print_title("Title", color=Colors.DEFAULT, underline="-")
    captured = capsys.readouterr()
    assert "Title" in captured.out
    assert "-----" in captured.out
