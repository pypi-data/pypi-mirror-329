# bit8tools

Biblioteca Python moderna para crear interfaces CLI elegantes con colores, validación de entrada y componentes estilizados, inspirada en la era de los 8 bits 🎮✨

## 🚀 Características

### Input
Clase para manejo de entrada de datos con validación:
- `text()`: Entrada de texto
- `int_number()`: Entrada y validación de números enteros
- `float_number()`: Entrada y validación de números decimales
- `yes_no()`: Entrada de opciones sí/no
- `date()`: Entrada y validación de fechas
- `email()`: Entrada y validación de correos electrónicos
- `password()`: Entrada de contraseñas
- `menu()`: Entrada de selección de menú

### Output
Clase para mostrar información formateada:
- `print()`: Impresión con colores
- `show_warning()`: Muestra mensajes de advertencia
- `show_error()`: Muestra mensajes de error
- `confirm()`: Muestra mensajes de confirmación
- `clear()`: Limpia la pantalla
- `press_enter_to_continue()`: Pausa hasta que se presione Enter
- `set_locale()`: Configura la localización
- `format_currency()`: Formatea números como moneda
- `print_title()`: Imprime un título con formato
- `show_progress_bar()`: Muestra una barra de progreso

### Colors
Clase base para manejo de colores en terminal:
- Códigos de color para texto
- Códigos de color para fondos
- Utilidades de formateo

### Alignment
Clase para manejo de alineación de texto:
- `LEFT`: Alineación a la izquierda
- `CENTER`: Alineación centrada
- `RIGHT`: Alineación a la derecha

### Tabular
Clase para manejo de tablas en terminal:
- `tabulate()`: Genera una tabla con los datos proporcionados

## 📦 Instalación

```bash
pip install bit8tools
```

## 🎮 Ejemplo de Uso

```python
from bit8tools import Input, Output, Colors, Alignment, Tabular

# Entrada de datos
nombre = Input.text("Ingrese su nombre:", Colors.GREEN, Colors.BLUE)
edad = Input.int_number("Ingrese su edad:", Colors.GREEN, Colors.BLUE, 0, 120)
peso = Input.float_number("Ingrese su peso:", Colors.GREEN, Colors.BLUE, 50, 150)
continuar = Input.yes_no("¿Deseas continuar? (si/no):", Colors.GREEN, Colors.BLUE)

# Salida formateada
Output.print(nombre, Colors.WHITE)
Output.print(edad, Colors.WHITE)
Output.print(peso, Colors.WHITE)
Output.print(continuar, Colors.WHITE)

Output.show_warning("Esto es un mensaje de advertencia.")
Output.show_error("Esto es un mensaje de error.")
Output.confirm("Esto es un mensaje de confirmación.")
Output.clear()
Output.print("Esto es un mensaje de limpieza.", Colors.RED)
Output.set_locale("es_AR")
Output.print(f"Mi sueldo es de {Output.format_currency(367000)}", Colors.GREEN)

# Alineación de texto
Output.print("Texto alineado a la izquierda")
Output.print("Texto centrado", color=Colors.BLUE, alignment=Alignment.CENTER)
Output.print("Texto alineado a la derecha", alignment=Alignment.RIGHT)

# Datos de ejemplo para la tabla
data = [
    {
        "nombre": "Juan Carlos González",
        "descripción": "Este es un texto muy largo que necesitará ser dividido",
        "ciudad": "Madrid"
    },
    {
        "nombre": "María",
        "descripción": "Texto corto",
        "ciudad": "Barcelona"
    }
]

# Usar el método estático directamente
Tabular.tabulate(data, title="Lista de Usuarios")

# O especificar un ancho máximo
Tabular.tabulate(data, title="Lista de Usuarios", max_width=80)

# Barra de progreso
total_iterations = 100
for i in range(total_iterations + 1):
    Output.show_progress_bar(i, total_iterations)
    time.sleep(0.1)
```

## 🛠️ Requisitos
- Python 3.8 o superior

## 📜 Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🤝 Contribuir
Las contribuciones son bienvenidas. Por favor, siéntete libre de:
- Reportar bugs
- Sugerir nuevas funcionalidades
- Enviar pull requests
