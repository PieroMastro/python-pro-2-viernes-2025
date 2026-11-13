from kivy.app import App
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.core.window import Window

Window.clearcolor = (0.12, 0.15, 0.22, 1)  # Fondo oscuro


class BotonAnimado(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.text = "Click para animar!"
        self.font_size = "18sp"
        self.size_hint = (None, None)
        self.size = (220, '60sp')
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.background_normal = ''
        self.background_color = (0.2, 0.7, 0.4, 1)


class MyApp(App):
    def build(self):
        return BotonAnimado()


MyApp().run()
