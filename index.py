import pygame
import random
import sys
import math

pygame.init()
pygame.mixer.init()

# Música de fondo (asegúrate de que el archivo existe)
try:
    pygame.mixer.music.load("musica.mp3")  # Cambia el nombre si es necesario
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Repite infinitamente
except:
    print("⚠️ No se pudo cargar el archivo de música.")

# Pantalla completa
info = pygame.display.Info()
ANCHO, ALTO = info.current_w, info.current_h
PANTALLA = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
pygame.display.set_caption("Cascada de Amor Musical")

# Fuente
FUENTE = pygame.font.SysFont("Arial", 30, bold=True)
FUENTE_GRANDE = pygame.font.SysFont("Arial", 70, bold=True)
FONDO = (0, 0, 0)

# Mensajes
MENSAJES = [
    "TE AMO"
]

def color_aleatorio():
    return (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

def mensaje_aleatorio():
    return random.choice(MENSAJES)

class Letra:
    def __init__(self):
        self.texto_original = mensaje_aleatorio()
        self.color = color_aleatorio()
        self.surface = FUENTE.render(self.texto_original, True, self.color)
        self.x = random.randint(0, ANCHO - 100)
        self.y = random.randint(-ALTO, 0)
        self.velocidad = random.uniform(1.5, 4.5)
        self.amplitud = random.uniform(10, 30)
        self.frecuencia = random.uniform(0.005, 0.02)
        self.fase = random.uniform(0, 2 * math.pi)
        self.activa = True
        self.alpha = 255

    def cambiar_mensaje_y_color(self):
        self.texto_original = mensaje_aleatorio()
        self.color = color_aleatorio()
        self.surface = FUENTE.render(self.texto_original, True, self.color)

    def mover(self):
        if self.activa:
            self.y += self.velocidad
            self.x_offset = self.amplitud * math.sin(self.frecuencia * self.y + self.fase)
            if self.y > ALTO - 100:
                self.alpha = max(0, self.alpha - 5)
                if self.alpha == 0:
                    self.activa = False

    def dibujar(self):
        if self.activa:
            temp_surface = self.surface.copy()
            temp_surface.set_alpha(self.alpha)
            PANTALLA.blit(temp_surface, (self.x + self.x_offset, self.y))

class Particula:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.vida = random.randint(20, 40)
        self.radio = random.randint(2, 4)
        self.color = color

    def mover(self):
        self.x += self.vx
        self.y += self.vy
        self.vida -= 1

    def dibujar(self):
        if self.vida > 0:
            pygame.draw.circle(PANTALLA, self.color, (int(self.x), int(self.y)), self.radio)

letras = [Letra() for _ in range(30)]
particulas = []
mostrar_te_adoro = False
reloj = pygame.time.Clock()

# Bucle principal
while True:
    PANTALLA.fill(FONDO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            for letra in letras:
                if letra.activa:
                    letra.cambiar_mensaje_y_color()
                    for _ in range(10):
                        particulas.append(Particula(letra.x + 50, letra.y + 20, letra.color))
                    letra.activa = False
            mostrar_te_adoro = True
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    if random.randint(1, 5) == 1:
        letras.append(Letra())

    for letra in letras:
        letra.mover()
        letra.dibujar()

    for p in particulas:
        p.mover()
        p.dibujar()

    particulas = [p for p in particulas if p.vida > 0]
    letras = [l for l in letras if l.y < ALTO + 100 and l.activa]

    if mostrar_te_adoro:
        texto_grande = FUENTE_GRANDE.render(random.choice(MENSAJES), True, color_aleatorio())
        rect = texto_grande.get_rect(center=(ANCHO // 2, ALTO // 2))
        PANTALLA.blit(texto_grande, rect)

    pygame.display.flip()
    reloj.tick(60)
