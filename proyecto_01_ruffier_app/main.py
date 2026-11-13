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
from ruffier import ruffier_index, check_int
from timer import Counter

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
        age = check_int(self.age_input.text)

        if age < 7 or age == False or not name:
            age = 7
            self.age_input.text = str(age)
        else:
            self.manager.current = "pulse1"


class PulseScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        instructions = Label(text=TXT_TEST1)
        self.counter_label = Counter(15)
        pulse_1_text = Label(text="Ingresar el resultado:", halign="right")
        self.pulse_1_input = TextInput(text="0", multiline=False)
        self.pulse_1_input.disabled = True

        input_line = BoxLayout(size_hint=(0.8, None), height="30sp")
        input_line.add_widget(pulse_1_text)
        input_line.add_widget(self.pulse_1_input)

        self.button = Button(
            text="Iniciar Toma", size_hint=(0.3, 0.4), pos_hint={"center_x": 0.5}
        )
        self.button.on_press = self.on_press_button

        main_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        main_layout.add_widget(instructions)
        main_layout.add_widget(self.counter_label)
        main_layout.add_widget(input_line)
        main_layout.add_widget(self.button)

        self.add_widget(main_layout)

        self.counter_label.bind(done=self.finish_register)

    def on_press_button(self):
        if self.button.text == "Iniciar Toma":
            self.counter_label.start()
            self.button.disabled = True
            self.button.text = 'Midiendo pulso...'
        elif self.button.text == "Continuar":
            self.next()

    def finish_register(self, instance, valor):
        if valor:
            self.pulse_1_input.disabled = False
            self.button.text = "Continuar"
            self.button.disabled = False

    def next(self):
        global pulse_1

        pulse_1 = int(self.pulse_1_input.text)

        if pulse_1 < 8 or pulse_1 == False:
            pulse_1 = 0
            self.pulse_1_input.text = str(pulse_1)
        else:
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

        # Variable para llevar el control estricto de la fase actual
        # Fases: 1 = 2da toma (15s), 2 = Descanso (30s), 3 = 3ra toma (15s)
        self.phase = 1

        instructions = Label(text=TXT_TEST3)

        pulse_2_text = Label(text="Resultado (Pulse 2):", halign="right")
        self.pulse_2_input = TextInput(text="0", multiline=False)
        self.pulse_2_input.disabled = True

        self.counter_label = Counter(15)

        pulse_3_text = Label(
            text="Resultado después de descanso (Pulse 3):", halign="right")
        self.pulse_3_input = TextInput(text="0", multiline=False)
        self.pulse_3_input.disabled = True

        self.button = Button(
            text="Iniciar 2da Toma (15s)",
            size_hint=(0.3, 0.2),
            pos_hint={"center_x": 0.5}
        )
        self.button.on_press = self.on_press_button

        input_line_1 = BoxLayout(size_hint=(0.8, None), height="30sp")
        input_line_1.add_widget(pulse_2_text)
        input_line_1.add_widget(self.pulse_2_input)

        input_line_2 = BoxLayout(size_hint=(0.8, None), height="30sp")
        input_line_2.add_widget(pulse_3_text)
        input_line_2.add_widget(self.pulse_3_input)

        main_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        main_layout.add_widget(instructions)
        main_layout.add_widget(self.counter_label)
        main_layout.add_widget(input_line_1)
        main_layout.add_widget(input_line_2)
        main_layout.add_widget(self.button)

        self.add_widget(main_layout)

        self.counter_label.bind(done=self.handle_timer_finish)

    def on_press_button(self):
        current_text = self.button.text

        if current_text == "Iniciar 2da Toma (15s)":
            self.phase = 1
            self.counter_label.restart(15)
            self.counter_label.start()
            self.button.disabled = True
            self.button.text = "Midiendo 2da toma..."

        elif current_text == "Iniciar Descanso (30s)":
            global pulse_2
            pulse_2 = check_int(self.pulse_2_input.text)
            if pulse_2 < 8 or pulse_2 is False:
                pulse_2 = 0
                self.pulse_2_input.text = str(pulse_2)
                return

            self.pulse_2_input.disabled = True
            self.phase = 2  # cambiamos al siguiente estado
            # reiniciamos y establecemos el nuevo timer
            self.counter_label.restart(30)
            self.counter_label.start()
            self.button.disabled = True
            self.button.text = "Descansando..."

        elif current_text == "Iniciar Última Toma (15s)":
            self.phase = 3
            self.counter_label.restart(15)
            self.counter_label.start()
            self.button.disabled = True
            self.button.text = "Midiendo 3ra toma..."

        elif current_text == "Finalizar":
            self.next()

    def handle_timer_finish(self, instance, valor):
        if valor:
            if self.phase == 1:
                # fin de la 2da toma: habilitamos el input 2 y pedimos iniciar descanso
                self.pulse_2_input.disabled = False
                self.button.text = "Iniciar Descanso (30s)"
                self.button.disabled = False
            elif self.phase == 2:
                # Fin del descanso: habilitamos el botón para los últimos 15s
                self.button.text = "Iniciar Última Toma (15s)"
                self.button.disabled = False
            elif self.phase == 3:
                # Fin de la 3ra toma
                self.pulse_3_input.disabled = False
                self.button.text = "Finalizar"
                self.button.disabled = False

    def next(self):
        global pulse_3
        pulse_3 = check_int(self.pulse_3_input.text)

        if pulse_3 < 8 or pulse_3 is False:
            pulse_3 = 0
            self.pulse_3_input.text = str(pulse_3)
        else:
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
