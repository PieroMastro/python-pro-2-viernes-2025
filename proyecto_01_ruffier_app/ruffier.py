# LOGICA DE NUESTRA APP

def ruffier_index(pulse_1: int, pulse_2: int, pulse_3: int) -> float:
    index = (4 * (pulse_1 + pulse_2 + pulse_3) - 200) / 10
    return index
