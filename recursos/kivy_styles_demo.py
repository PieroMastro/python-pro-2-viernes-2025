from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

Window.clearcolor = (0.15, 0.15, 0.25, 1)
Window.size = (350, 500)


class StyledLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 30

        self.saludo_text = Label(
            text='Presiona un boton!',
            font_size=24,
            markup=True,
            color=(0.8, 0.8, 0, 1)
        )

        self.boton1 = Button(
            text='Click',
            size_hint=(1, 0.3),
            background_color=(0.2, 0.7, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        self.boton2 = Button(
            text='Click',
            size_hint=(1, 0.3),
            background_normal='',
            background_color=(0.2, 0.7, 0.4, 1),
            color=(1, 1, 1, 1)
        )

        self.add_widget(self.saludo_text)
        self.add_widget(self.boton1)
        self.add_widget(self.boton2)

        self.boton1.on_press = self.change_red
        self.boton2.on_press = self.change_blue

    def change_red(self):
        self.saludo_text.text = "¡Cambio a  [color=ff0000]ROJO[/color]!"
        self.boton1.background_color = (1, 0, 0, 1)  # Cambia a rojo
        self.boton2.background_color = (1, 0, 0, 1)

    def change_blue(self):
        self.saludo_text.text = "¡Cambio a  [color=0000ff]AZUL[/color]!"
        self.boton1.background_color = (0, 0, 1, 1)  # Cambia a azul
        self.boton2.background_color = (0, 0, 1, 1)


class MyApp(App):
    def build(self):
        return StyledLayout()


if __name__ == "__main__":
    MyApp().run()
