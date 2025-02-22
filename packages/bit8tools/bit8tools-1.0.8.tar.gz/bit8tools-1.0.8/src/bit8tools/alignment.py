"""
Módulo con las alineaciones posibles.
"""


class Alignment:
    """Clase con las alineaciones posibles."""
    LEFT = 'left'
    CENTER = 'center'
    RIGHT = 'right'

    @staticmethod
    def validate_alignment(alignment: str) -> str:
        """Valida la alineación proporcionada.

        Args:
            alignment (str): Alineación a validar.

        Returns:
            str: Alineación validada.
        """
        valid_alignments = [Alignment.LEFT, Alignment.CENTER, Alignment.RIGHT]
        return alignment if alignment in valid_alignments else Alignment.LEFT
