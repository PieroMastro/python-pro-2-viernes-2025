# MODULO PARA EL TEMPORIZADOR DINAMICO

from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.properties import NumericProperty, BooleanProperty


class Counter(Label):
    done = BooleanProperty(False)
    current = NumericProperty(0)

    def __init__(self, total, **kwargs):
        super().__init__(**kwargs)
        self.total = total  # duracion del temporizador
        self.text = f'Segundos transcurridos: {self.current}'
        self._event = None

    def start(self):
        if self._event:
            self._event.cancel()

        self._event = Clock.schedule_interval(self.counter, 1)

    def counter(self, dt):
        if self.current <= self.total:
            self.current += 1
            self.text = f'Segundos transcurridos: {self.current}'

        if self.current >= self.total:
            self.done = True
            return False

    def restart(self, total):
        """Reinicia el contador con un nuevo número de segundos y lo prepara."""
        if self._event:
            self._event.cancel()

        self.total = total
        self.current = 0
        self.done = False
        self.text = f'Segundos transcurridos: {self.current}'
