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
from runner import Runner
from sits import Sits

# VARIABLES GLOBALES
name = ""
age = 7
pulse_1, pulse_2, pulse_3 = 0, 0, 0


class IntroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        instructions = Label(
            text=TXT_INSTRUCTIONS,
            halign="center",
            text_size=(400, None)
        )

        name_text = Label(text="Ingrese su nombre:", halign="right")
        age_text = Label(text="Ingrese su edad:", halign="right")

        self.name_input = TextInput(multiline=False)
        self.age_input = TextInput(text="7", multiline=False)

        self.button = Button(
            text="Inicio", size_hint=(0.3, 0.2), pos_hint={"center_x": 0.5}
        )
        self.button.on_press = self.next

        input_line_1 = BoxLayout(size_hint=(0.8, None), height="30sp")
        input_line_2 = BoxLayout(size_hint=(0.8, None), height="30sp")

        input_line_1.add_widget(name_text)
        input_line_1.add_widget(self.name_input)

        input_line_2.add_widget(age_text)
        input_line_2.add_widget(self.age_input)

        main_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        main_layout.add_widget(instructions)
        main_layout.add_widget(input_line_1)
        main_layout.add_widget(input_line_2)
        main_layout.add_widget(self.button)

        self.add_widget(main_layout)

    def next(self):
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

        pulse_1 = check_int(self.pulse_1_input.text)

        if pulse_1 < 8 or pulse_1 == False:
            pulse_1 = 0
            self.pulse_1_input.text = str(pulse_1)
        else:
            self.manager.current = "sits"


class CheckSits(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        total_sentadillas = 30

        instructions = Label(
            text=TXT_SITS,
            halign="center",
            size_hint=(1, 0.2)
        )
        instructions.bind(size=lambda s, w: setattr(s, 'text_size', s.size))

        # 1. Instanciamos el contador de texto (Sits)
        self.contador_label = Sits(
            total=total_sentadillas,
            font_size="20sp",
            size_hint=(1, 0.1)
        )

        # 2. Instanciamos el botón animado (Runner)
        self.runner_widget = Runner(
            total=total_sentadillas,
            steptime=1.5,
            size_hint=(1, 0.5)
        )

        # 3. enlace de la propiedad value de Runner con el metodo de Sits
        self.runner_widget.bind(value=self.contador_label.actualizar_contador)
        # 4. enlace del estado 'finished' para habilitar el avance al terminar
        self.runner_widget.bind(finished=self.verificar_terminado)

        self.button = Button(
            text="Iniciar Sentadillas",
            size_hint=(0.5, 0.15),
            pos_hint={"center_x": 0.5},
            background_normal="",
            background_color=(0.2, 0.7, 0.4, 1)
        )
        self.button.on_press = self.on_press_button

        main_layout = BoxLayout(orientation="vertical", padding=15, spacing=10)
        main_layout.add_widget(instructions)
        main_layout.add_widget(self.contador_label)
        main_layout.add_widget(self.runner_widget)
        main_layout.add_widget(self.button)

        self.add_widget(main_layout)

    def on_press_button(self):
        if self.button.text == "Iniciar Sentadillas":
            self.button.disabled = True
            self.button.text = "Prueba en curso..."
            self.runner_widget.start()
        elif self.button.text == "Continuar":
            self.next()

    def verificar_terminado(self, instance, valor):
        """Se activa automáticamente cuando el Runner termina todas las repeticiones."""
        if valor:
            self.button.text = "Continuar"
            self.button.disabled = False
            self.button.background_color = (0.2, 0.7, 0.4, 1)

    def next(self):
        self.manager.current = "pulse2"


class PulseScr2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
            self.phase = 2
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
                self.pulse_2_input.disabled = False
                self.button.text = "Iniciar Descanso (30s)"
                self.button.disabled = False
            elif self.phase == 2:
                self.button.text = "Iniciar Última Toma (15s)"
                self.button.disabled = False
            elif self.phase == 3:
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
