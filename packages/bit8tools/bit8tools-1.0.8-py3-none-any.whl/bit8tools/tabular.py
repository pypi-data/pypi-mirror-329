"""
Módulo que contiene la clase Tabular para generar tablas en la consola a partir de 
listas de diccionarios.

Contenido
---------
- Clase Tabular: contiene métodos para generar y formatear tablas en la consola.
"""
from textwrap import wrap
from .output import Output


class Tabular:
    """
    Clase que contiene métodos para generar y formatear tablas en la consola a partir de
    listas de diccionarios.
    """
    MIN_COLUMN_WIDTH = 10

    @staticmethod
    def tabulate(data: list, title: str = "", max_width: int = 0):
        """
        Genera una tabla en la consola a partir de una lista de diccionarios,
        ajustando el contenido al ancho disponible.

        Args:
            data (list): Lista de diccionarios con los datos para la tabla.
            title (str, optional): Título opcional para la tabla.
            max_width (int, optional): Ancho máximo para la tabla. Si no se especifica,
                                     se usa el ancho de la consola.
        """
        if not data:
            print("No hay datos para mostrar.")
            return

        # Configurar el ancho máximo
        max_width = max_width or Output.get_console_size()[0]

        header = Tabular._get_header(data[0])
        initial_widths = Tabular._get_initial_widths(data)
        adjusted_widths = Tabular._adjust_column_widths(
            initial_widths, max_width)

        if title:
            total_width = sum(adjusted_widths.values()) + \
                3 * (len(header) - 1) + 4
            print("\n" + title.center(total_width))

        Tabular._generate_header(header, adjusted_widths)
        for row in data:
            Tabular._print_row(row, adjusted_widths)

        Tabular._print_separator(len(header), adjusted_widths.values())

    @staticmethod
    def _get_header(row: dict):
        """
        Obtiene los encabezados de la tabla desde las claves del diccionario.

        Args:
            row (dict): El diccionario de donde se obtendrán las claves.

        Returns:
            list: Lista con los nombres de las columnas.
        """
        return list(row.keys())

    @staticmethod
    def _get_initial_widths(data: list):
        """
        Calcula los anchos iniciales de las columnas basados en el contenido.

        Args:
            data (list): Lista de diccionarios con los datos.

        Returns:
            dict: Diccionario con los anchos iniciales de cada columna.
        """
        columns = data[0].keys()
        column_widths = {}

        for column in columns:
            max_value_length = max(
                len(str(row.get(column, "")))
                for row in data
            )
            column_widths[column] = max(len(column), max_value_length)

        return column_widths

    @staticmethod
    def _adjust_column_widths(initial_widths: dict, max_width: int):
        """
        Ajusta los anchos de las columnas para que quepan en el ancho disponible.

        Args:
            initial_widths (dict): Diccionario con los anchos iniciales.
            max_width (int): Ancho máximo disponible.

        Returns:
            dict: Diccionario con los anchos ajustados.
        """
        num_columns = len(initial_widths)
        available_width = max_width - \
            (3 * num_columns + 1)  # Espacio para bordes
        total_initial_width = sum(initial_widths.values())

        if total_initial_width <= available_width:
            return initial_widths

        # Calcular el factor de reducción
        reduction_factor = available_width / total_initial_width
        adjusted_widths = {}

        # Aplicar el factor de reducción manteniendo un ancho mínimo
        remaining_width = available_width
        remaining_columns = num_columns

        for column, width in initial_widths.items():
            if remaining_columns == 1:
                # Última columna: usar el espacio restante
                adjusted_width = remaining_width
            else:
                # Calcular el ancho proporcional
                adjusted_width = max(
                    Tabular.MIN_COLUMN_WIDTH,
                    int(width * reduction_factor)
                )

            adjusted_widths[column] = adjusted_width
            remaining_width -= adjusted_width
            remaining_columns -= 1

        return adjusted_widths

    @staticmethod
    def _generate_header(header: list, widths: dict):
        """
        Genera el encabezado de la tabla.

        Args:
            header (list): Lista con los nombres de las columnas.
            widths (dict): Diccionario con los anchos de las columnas.
        """
        Tabular._print_separator(len(header), list(widths.values()))
        header_dict = {col: col for col in header}
        Tabular._print_row(header_dict, widths, is_header=True)
        Tabular._print_separator(len(header), list(widths.values()))

    @staticmethod
    def _print_separator(columns_count: int, widths: list):
        """
        Imprime la línea de separación entre las filas.

        Args:
            columns_count (int): Número de columnas.
            widths (list): Lista con los anchos de las columnas.
        """
        total_row_length = sum(widths) + 3 * (columns_count - 1)
        print(f"+-{'-' * total_row_length}-+")

    @staticmethod
    def _print_row(row: dict, columns_width: dict, is_header: bool = False):
        """
        Imprime una fila de la tabla, ajustando el contenido si es necesario.

        Args:
            row (dict): Diccionario con los datos de la fila.
            columns_width (dict): Diccionario con los anchos de las columnas.
            is_header (bool, optional): Indica si es una fila de encabezado.
        """
        # Preparar el contenido dividido para cada columna
        wrapped_content = {}
        for key in columns_width.keys():
            if is_header:
                value = key.upper()
            else:
                value = row.get(key, "")
                value = str(value) if value is not None else ""

            # Dividir el contenido si es más largo que el ancho de la columna
            wrapped_content[key] = wrap(value, columns_width[key])
            if not wrapped_content[key]:  # Si está vacío después de wrap
                wrapped_content[key] = [""]

        # Encontrar el número máximo de líneas necesarias
        max_lines = max(len(lines) for lines in wrapped_content.values())

        # Imprimir cada línea
        for line_num in range(max_lines):
            print("|", end="")
            for key, width in columns_width.items():
                # Obtener la línea actual o espacios en blanco si no hay más contenido
                if line_num < len(wrapped_content[key]):
                    value = wrapped_content[key][line_num]
                else:
                    value = ""
                print(f" {value:<{width}} |", end="")
            print()
