"""
Este módulo contiene las clases Input, Output, Colors y Alignment, que son las
encargadas de manejar la entrada de datos, la salida de texto con colores y la
alineación del texto.
"""
from .alignment import Alignment
from .colors import Colors
from .input import Input
from .output import Output
from .tabular import Tabular

__all__ = ['Alignment', 'Colors', 'Input', 'Output', 'Tabular']
