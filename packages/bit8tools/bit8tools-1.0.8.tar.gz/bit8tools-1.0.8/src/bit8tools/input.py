"""
Módulo que contiene las funciones para solicitar input al usuario con colores.

Contenido
---------
- Clase Input: contiene las funciones para solicitar input al usuario con colores.
"""
import getpass
import re
from .colors import Colors
from .output import Output


class Input:
    """
    Clase que contiene las funciones para solicitar input al usuario con colores.
    """
    @staticmethod
    def text(prompt: str, color_prompt: str = Colors.DEFAULT,
             color_input: str = Colors.DEFAULT) -> str:
        """
        Solicita un input al usuario mostrando el mensaje en un color y la respuesta en otro color.

        Args:
            prompt (str): El mensaje a mostrar al usuario.
            color_prompt: El color en el que se mostrará el mensaje.
            color_input: El color en el que se mostrará la respuesta del usuario.

        Returns: 
            str: La respuesta del usuario.
        """

        # Validar el color
        color_prompt = Colors.validate_color(color_prompt)
        color_input = Colors.validate_color(color_input)

        # Colorear el mensaje.
        message_colored = f"{color_prompt}{prompt}{color_input}"

        # Solicitar el input al usuario.
        user_input = input(message_colored)
        print(Colors.DEFAULT, end="")

        # Devolver la respuesta del usuario con el color por defecto.
        return f"{user_input}"

    @staticmethod
    def int_number(prompt: str, color_prompt: str = Colors.DEFAULT,
                   color_input: str = Colors.DEFAULT,
                   min_value: int = 0, max_value: int = 0) -> int:
        """
        Solicita un número entero al usuario mostrando el mensaje en un color y la respuesta en 
        otro color.

        Args:
            prompt (str): El mensaje a mostrar al usuario.
            color_prompt: El color en el que se mostrará el mensaje.
            color_input: El color en el que se mostrará la respuesta del usuario.

        Returns: 
            int: La respuesta del usuario.
        """

        # Validar el color
        color_prompt = Colors.validate_color(color_prompt)
        color_input = Colors.validate_color(color_input)

        # Colorear el mensaje.
        message_colored = f"{color_prompt}{prompt}{color_input}"

        # Validar el input.
        while True:
            # Solicitar el input al usuario.
            user_input = input(message_colored)
            print(Colors.DEFAULT, end="")
            # Validar el input.
            if user_input.isdigit():
                if not min_value is None and not max_value is None:
                    if int(user_input) < min_value or int(user_input) > max_value:
                        print(f"El valor debe estar entre {
                              min_value} y {max_value}.")
                        continue
                break
            print("El valor debe ser un número entero.")

        # Devolver la respuesta del usuario con el color por defecto.
        return int(user_input)

    @staticmethod
    def float_number(prompt: str, color_prompt: str = Colors.DEFAULT,
                     color_input: str = Colors.DEFAULT,
                     min_value: float = 0, max_value: float = 0) -> float:
        """
        Solicita un número flotante al usuario mostrando el mensaje en un color y la respuesta en 
        otro color.

        Args:
            prompt (str): El mensaje a mostrar al usuario.
            color_prompt: El color en el que se mostrará el mensaje.
            color_input: El color en el que se mostrará la respuesta del usuario.
            min_value: El valor mínimo permitido.
            max_value: El valor máximo permitido.

        Returns: 
            float: La respuesta del usuario.
        """

        # Validar el color
        color_prompt = Colors.validate_color(color_prompt)
        color_input = Colors.validate_color(color_input)

        # Colorear el mensaje.
        message_colored = f"{color_prompt}{prompt}{color_input}"

        # Validar el input.
        while True:
            # Solicitar el input al usuario.
            user_input = input(message_colored)
            print(Colors.DEFAULT, end="")
            try:
                # Convertir el input a float.
                user_input_float = float(user_input)
                # Validar el rango.
                if min_value <= user_input_float <= max_value:
                    return user_input_float
                else:
                    print(
                        f"El valor debe estar entre {min_value} y {max_value}.")
            except ValueError:
                print("El valor debe ser un número con decimales.")

    @staticmethod
    def yes_no(prompt: str, color_prompt: str, color_input: str) -> bool:
        """
        Solicita un booleano al usuario mostrando el mensaje en un color y la respuesta en 
        otro color.

        Args:
            prompt (str): El mensaje a mostrar al usuario.
            color_prompt: El color en el que se mostrará el mensaje.
            color_input: El color en el que se mostrará la respuesta del usuario.

        Returns: 
            bool: La respuesta del usuario.
        """

        # Validar el color
        color_prompt = Colors.validate_color(color_prompt)
        color_input = Colors.validate_color(color_input)

        # Colorear el mensaje.
        message_colored = f"{color_prompt}{prompt}{color_input}"

        while True:
            # Solicitar el input al usuario.
            user_input = input(message_colored).lower()
            print(Colors.DEFAULT, end="")

            # Validar el input.
            if user_input.lower() in ["s", "n", "y"]:
                if user_input.lower().startswith("s") or user_input.lower().startswith("y"):
                    return True
                return False
            print("Por favor ingrese 's', 'n' o 'y'.")

    @staticmethod
    def email(prompt: str, color_prompt: str, color_input: str) -> str:
        """
        Solicita un email al usuario mostrando el mensaje en un color y la respuesta en 
        otro color.

        Args:
            prompt (str): El mensaje a mostrar al usuario.
            color_prompt: El color en el que se mostrará el mensaje.
            color_input: El color en el que se mostrará la respuesta del usuario.

        Returns: 
            str: La respuesta del usuario.
        """

        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        # Validar el color
        color_prompt = Colors.validate_color(color_prompt)
        color_input = Colors.validate_color(color_input)

        # Colorear el mensaje.
        message_colored = f"{color_prompt}{prompt}{color_input}"

        # Solicitar el input al usuario.
        while True:
            user_input = input(message_colored)
            print(Colors.DEFAULT, end="")

            # Validar el input.
            if re.match(pattern, user_input):
                return user_input
            print("\nPor favor ingrese un email válido.")

    @staticmethod
    def date(prompt: str, color_prompt: str, color_input: str) -> str:
        """
        Solicita una fecha en formato dd/mm/yyyy al usuario mostrando el mensaje en un color y 
        la respuesta en otro color.

        Args:
            prompt (str): El mensaje a mostrar al usuario.
            color_prompt: El color en el que se mostrará el mensaje.
            color_input: El color en el que se mostrará la respuesta del usuario.

        Returns: 
            str: La respuesta del usuario.
        """

        pattern = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/([0-9]{4})$"

        # Validar el color
        color_prompt = Colors.validate_color(color_prompt)
        color_input = Colors.validate_color(color_input)

        # Colorear el mensaje.
        message_colored = f"{color_prompt}{prompt}{color_input}"

        # Solicitar el input al usuario.
        while True:
            user_input = input(message_colored)
            print(Colors.DEFAULT, end="")

            # Validar el input.
            if re.match(pattern, user_input):
                return user_input
            print("\nPor favor ingrese una fecha válida en formato " +
                  "dd/mm/yyyy (por ejemplo, 25/12/2025).")

    @staticmethod
    def password(prompt: str, color_prompt: str, color_input: str) -> str:
        """
        Solicita una contraseña al usuario y la valida para asegurarse de que cumple con los 
        siguientes requisitos:
          - Tiene al menos 8 caracteres
          - Tiene al menos un dígito
          - Tiene al menos una mayúscula
          - Tiene al menos una minúscula
        Mientras el usuario escribe la contraseña, se muestran asteriscos en lugar de los caracteres 
        ingresados.

        Args:
            prompt (str): El mensaje a mostrar al usuario.
            color_prompt: El color en el que se mostrará el mensaje.
            color_input: El color en el que se mostrará la respuesta del usuario.

        Returns: 
            str: La respuesta del usuario.
        """

        # Validar el color
        color_prompt = Colors.validate_color(color_prompt)
        color_input = Colors.validate_color(color_input)

        # Colorear el mensaje.
        message_colored = f"{color_prompt}{prompt}{color_input}"

        # Solicitar el input al usuario.
        while True:
            password = getpass.getpass(message_colored)
            print(Colors.DEFAULT, end="")

            # Validar el input.
            if len(password) < 8:
                print("La contraseña debe tener al menos 8 caracteres.")
                continue

            if not any(char.isdigit() for char in password):
                print("La contraseña debe tener al menos un dígito.")
                continue

            if not any(char.isupper() for char in password):
                print("La contraseña debe tener al menos una mayúscula.")
                continue

            if not any(char.islower() for char in password):
                print("La contraseña debe tener al menos una minúscula.")
                continue

            return password

    @staticmethod
    def menu(title: str, options: list, color_prompt: str, color_input: str) -> int:
        """
        Muestra un menú con las opciones especificadas y solicita al usuario que elija una opción.

        Args:
            title (str): El título del menú.
            options (list): Una lista de opciones a mostrar en el menú.
            color_prompt (str): El color en el que se mostrará el mensaje.
            color_input (str): El color en el que se mostrará la respuesta del usuario.

        Returns:
            int: La opción seleccionada por el usuario.
        """

        # Validar el color
        color_prompt = Colors.validate_color(color_prompt)
        color_input = Colors.validate_color(color_input)

        while True:
            Output.clear()
            Output.print_title(title, color_prompt, "=")

            for i, option in enumerate(options):
                Output.print(f"{i + 1} - {option}", color_prompt)

            # Solicitar al usuario que elija una opción
            choice = Input.text("\nElija una opción: ",
                                color_prompt, color_input)
            # Verifica que la opción sea válida
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                return int(choice)
            Output.show_error("\nOpción inválida, intente de nuevo.")
            Output.press_enter_to_continue()
