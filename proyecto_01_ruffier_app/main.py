from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput

from instructions import (
    TXT_INSTRUCTIONS,
    TXT_TEST1,
    TXT_TEST2,
    TXT_TEST3,
    TXT_SITS,
)
from ruffier import ruffier_index

# VARIABLES GLOBALES
name = ""
age = 7
pulse_1, pulse_2, pulse_3 = 0, 0, 0


class IntroScreen(Screen):
    """Pantalla de bienvenida e ingreso de datos del usuario (Nombre y Edad).

    Esta clase hereda de Screen (de ScreenManager) y representa la primera
    vista
    que interactúa con el alumno/paciente al abrir la aplicación móvil.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 1. Creación de componentes visuales (Widgets individuales)
        # Etiqueta que muestra las instrucciones iniciales importadas desde el módulo instructions
        instructions = Label(
            text=TXT_INSTRUCTIONS,
            halign="center",
            text_size=(400, None)
        )

        # Etiquetas descriptivas para alinear junto a los campos de texto
        name_text = Label(text="Ingrese su nombre:", halign="right")
        age_text = Label(text="Ingrese su edad:", halign="right")

        # Campos de entrada de texto interactivos (multiline=False evita saltos de línea)
        self.name_input = TextInput(multiline=False)
        self.age_input = TextInput(text="7", multiline=False)

        # Botón de acción principal para avanzar a la siguiente pantalla
        self.button = Button(
            text="Inicio", size_hint=(0.3, 0.2), pos_hint={"center_x": 0.5}
        )
        # Vinculación del evento de presión del botón con el método de transición
        self.button.on_press = self.next

        # 2. Layouts horizontales, texto / input
        input_line_1 = BoxLayout(size_hint=(0.8, None), height="30sp")
        input_line_2 = BoxLayout(size_hint=(0.8, None), height="30sp")

        input_line_1.add_widget(name_text)
        input_line_1.add_widget(self.name_input)

        input_line_2.add_widget(age_text)
        input_line_2.add_widget(self.age_input)

        # 3. Configuración del layout primario (vertical) que apila todos los elementos
        main_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        main_layout.add_widget(instructions)
        main_layout.add_widget(input_line_1)
        main_layout.add_widget(input_line_2)
        main_layout.add_widget(self.button)

        # 4. Adición del layout contenedor principal a la pantalla actual
        self.add_widget(main_layout)

    def next(self):
        """Método de control para validar datos y cambiar de pantalla.

        Captura el nombre y la edad introducidos y los almacena en las variables
        globales.
        """
        global name, age

        name = self.name_input.text
        age = int(self.age_input.text)
        self.manager.current = "pulse1"


class PulseScr(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        instructions = Label(text=TXT_TEST1)
        input_line = BoxLayout(size_hint=(0.8, None), height="30sp")
        pulse_1_text = Label(text="Ingresar el resultado:", halign="right")
        self.pulse_1_input = TextInput(text="0", multiline=False)

        input_line.add_widget(pulse_1_text)
        input_line.add_widget(self.pulse_1_input)

        self.button = Button(
            text="Siguiente", size_hint=(0.3, 0.2), pos_hint={"center_x": 0.5}
        )
        self.button.on_press = self.next

        main_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        main_layout.add_widget(instructions)
        main_layout.add_widget(input_line)
        main_layout.add_widget(self.button)

        self.add_widget(main_layout)

    def next(self):
        global pulse_1

        pulse_1 = int(self.pulse_1_input.text)
        self.manager.current = "sits"


class CheckSits(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        instructions = Label(text=TXT_TEST2)
        self.button = Button(
            text="Siguiente", size_hint=(0.3, 0.2), pos_hint={"center_x": 0.5}
        )
        self.button.on_press = self.next

        main_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        main_layout.add_widget(instructions)
        main_layout.add_widget(self.button)

        self.add_widget(main_layout)

    def next(self):
        self.manager.current = "pulse2"


class PulseScr2(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        instructions = Label(text=TXT_TEST3)
        pulse_2_text = Label(text="Resultado:", halign="right")
        self.pulse_2_input = TextInput(text="0", multiline=False)
        pulse_3_text = Label(
            text="Resultado después de descanso:", halign="right"
        )
        self.pulse_3_input = TextInput(text="0", multiline=False)

        self.button = Button(
            text="Finalizar", size_hint=(0.3, 0.2), pos_hint={"center_x": 0.5}
        )
        self.button.on_press = self.next

        input_line_1 = BoxLayout(size_hint=(0.8, None), height="30sp")
        input_line_1.add_widget(pulse_2_text)
        input_line_1.add_widget(self.pulse_2_input)

        input_line_2 = BoxLayout(size_hint=(0.8, None), height="30sp")
        input_line_2.add_widget(pulse_3_text)
        input_line_2.add_widget(self.pulse_3_input)

        main_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        main_layout.add_widget(instructions)
        main_layout.add_widget(input_line_1)
        main_layout.add_widget(input_line_2)
        main_layout.add_widget(self.button)

        self.add_widget(main_layout)

    def next(self):
        global pulse_2, pulse_3

        pulse_2 = int(self.pulse_2_input.text)
        pulse_3 = int(self.pulse_3_input.text)
        self.manager.current = "result"


class Result(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.results = Label(text="")
        self.main_layout = BoxLayout(
            orientation="vertical", padding=10, spacing=10
        )
        self.main_layout.add_widget(self.results)
        self.add_widget(self.main_layout)
        self.on_enter = self.get_results

    def get_results(self):
        global name, pulse_1, pulse_2, pulse_3
        self.results.text = (
            f"{name}\nÍndice de Ruffier:"
            f" {ruffier_index(pulse_1, pulse_2, pulse_3)}"
        )


class RuffierApp(App):

    def build(self):
        scr_manager = ScreenManager()
        scr_manager.add_widget(IntroScreen(name="main"))
        scr_manager.add_widget(PulseScr(name="pulse1"))
        scr_manager.add_widget(CheckSits(name="sits"))
        scr_manager.add_widget(PulseScr2(name="pulse2"))
        scr_manager.add_widget(Result(name="result"))

        return scr_manager


if __name__ == "__main__":
    app = RuffierApp()
    app.run()
