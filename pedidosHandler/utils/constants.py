# Estados del pedido
PREPARANDO = "P"
COMPLETO = "C"
PAGADO = "G"
ESTADO_CHOICES = (
    (PREPARANDO, 'PREPARANDO'),
    (COMPLETO, 'COMPLETO'),
    (PAGADO, 'PAGADO'),
)
# Mesas
A1 = 'AI'
A2 = 'AD'
A3 = 'AT'
A4 = 'AM'
A5 = 'AE'
B1 = 'B1'
B2 = 'B2'
B3 = 'B3'
B4 = 'B4'
B5 = 'B5'
B6 = 'B6'
B7 = 'B7'
B8 = 'B8'
B9 = 'B9'
MESA_CHOICES = (
    (A1, 'Afuera puerta izquierda'),
    (A2, 'Afuera puerta derecha'),
    (A3, 'Afuera televisor'),
    (A4, 'Afuera meson'),
    (A5, 'Afuera extra1'),
    (B1, 'Adentro #1'),
    (B2, 'Adentro #2'),
    (B3, 'Adentro #3'),
    (B4, 'Adentro #4'),
    (B5, 'Adentro #5'),
    (B6, 'Adentro #6'),
    (B7, 'Adentro #7'),
    (B8, 'Adentro #8'),
    (B9, 'Adentro extra 1'),

)
