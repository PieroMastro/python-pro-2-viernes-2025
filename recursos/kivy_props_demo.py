from kivy.app import App
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class Contador(BoxLayout):
    clicks = NumericProperty(0)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 30

        self.texto_contador = Label(
            text=f'Clicks: {self.clicks}', font_size='30sp')
        self.aumentar_contador = Button(
            text=f'Incrementar!', font_size='30sp', background_color=(0, 1, 0, 1), size_hint=(0.3, 0.5))
        self.disminuir_contador = Button(
            text=f'Disminuir!', font_size='30sp', background_color=(1, 0, 0, 1), size_hint=(0.3, 0.5))
        self.aumentar_contador.on_press = self.incrementar
        self.disminuir_contador.on_press = self.disminuir

        fila = BoxLayout(spacing=30)
        fila.add_widget(self.aumentar_contador)
        fila.add_widget(self.disminuir_contador)

        self.add_widget(self.texto_contador)
        self.add_widget(fila)

        self.bind(clicks=self.actualizar_contador)

    def incrementar(self):
        self.clicks += 1
        self.texto_contador.font_size += 1

    def disminuir(self):
        self.clicks -= 1
        self.texto_contador.font_size -= 1

    def actualizar_contador(self, instance, value):
        self.texto_contador.text = f'Clicks: {value}'


class MyApp(App):
    def build(self):
        return Contador()


MyApp().run()
