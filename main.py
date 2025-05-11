import pygame
import random
import time
import sys
import ctypes
from timeit import timeit
from numpy import rint
import os
import clock
import time as tm

pygame.init()

# Constantes
GRID_SIZE = 10
GRID_WIDTH = 10
GRID_HEIGHT = 20
CANDY_SIZE = 30
TIPOS_CARAMELOS = ['rojo', 'verde', 'azul', 'amarillo', 'arcoiris']
FALLBACK_COLORS = {
    'rojo': (255, 0, 0),
    'verde': (0, 255, 0),
    'azul': (0, 0, 255),
    'amarillo': (255, 255, 0),
    'arcoiris': (255, 0, 255)
}

# Clases
class Time:
    def __init__(self):
        self.time_module = tm

    def get_time(self):
        return self.time_module.strftime("%Y-%m-%d %H:%M:%S", self.time_module.localtime())

class MyTime:
    def __init__(self):
        local_time = time.localtime()
        self.formatted_time = time.strftime("%Y a o %m mes %d d a %H hora %M minuto %S segundo", local_time)

    def parse_time_str(self, str_time):
        """
        Parse a string representing the time using the format %Y-%m-%d %H:%M:%S
        and return the corresponding time object.

        Args:
            str_time (str): the string to parse

        Returns:
            time.struct_time: the parsed time

        Raises:
            ValueError: if str_time is None or empty
            TypeError: if str_time is not a string
            ValueError: if str_time does not match the expected format
        """
        if str_time is None or not str_time:
            raise ValueError("str_time can't be None or empty")
        if not isinstance(str_time, str):
            raise TypeError("str_time must be a string")

        try:
            parsed_time = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError(f"str_time '{str_time}' does not match the expected format '%Y-%m-%d %H:%M:%S'")

        return parsed_time

    def measure_time_interval(self, pause_time: float) -> float:
        """
        Measure the time difference between the current time and a time after
        waiting for a certain amount of time.

        Args:
            pause_time: The amount of time to wait.

        Returns:
            The time difference.

        Raises:
            ValueError: If pause_time is None or negative.
        """
        if pause_time is None:
            raise ValueError("pause_time cannot be None")
        if pause_time < 0:
            raise ValueError("pause_time must be a positive number")

        start_time = time.time()
        try:
            time.sleep(pause_time)
        except KeyboardInterrupt:
            sys.exit(0)
        end_time = time.time()
        time_difference = end_time - start_time
        return time_difference


class Clock:
    def __init__(self):
        self.timestamp = time.perf_counter()
        self.cpu_time = time.process_time()
        self.local_time = time.localtime()
        self.formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", self.local_time)

class Caramelo:
    def __init__(self, tipo, x, y):
        self.tipo = tipo
        self.image = load_image(f'{tipo}.png')
        self.rect = self.image.get_rect(topleft=(x, y))

    def dibujar(self, pantalla):
        if self.image is not None:
            pantalla.blit(self.image, self.rect)

class Coin:
    def __init__(self, x, y):
        # The image is not optional, so let's check if it was loaded correctly
        self.image = load_image('coin.png')
        if self.image is None:
            raise ValueError('La imagen "coin.png" no se pudo cargar')
        self.rect = self.image.get_rect(topleft=(x, y))

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)

class SuperPiluka:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image('superpiluka.png')
        if self.image is not None:
            self.image = pygame.transform.scale(self.image, (CANDY_SIZE, CANDY_SIZE))

    def dibujar(self, pantalla):
        if self.image is not None and pantalla is not None:
            pantalla.blit(self.image, (self.x, self.y))

class Enemy:
    def __init__(self, x, y):
        """Constructor de la clase Enemy.

        Args:
            x (int): La posición x del enemigo.
            y (int): La posición y del enemigo.

        Raises:
            ValueError: Si la imagen "enemy.png" no se pudo cargar.
        """
        self.x = x
        self.y = y
        self.image = load_image('enemy.png')
        if self.image is None:
            raise ValueError('La imagen "enemy.png" no se pudo cargar')

    def dibujar(self, pantalla):
        if pantalla is not None:
            pantalla.blit(self.image, (self.x, self.y))

class Jugador:
    def __init__(self) -> None:
        """Constructor de la clase Jugador."""
        self.coins = 0

    def add_coin(self) -> None:
        """Add a coin to the player."""
        if not hasattr(self, 'coins'):
            raise AttributeError('Player has no coins attribute')
        if not isinstance(self.coins, int):
            raise TypeError('Player coins attribute must be an int')
        self.coins += 1

class Nivel:
    def __init__(self, number: int, goal: str) -> None:
        """
        Nivel constructor.

        Args:
            number (int): Level number.
            goal (str): Level goal.

        Raises:
            TypeError: If number is not an int.
            TypeError: If goal is not a str.
        """
        if not isinstance(number, int):
            raise TypeError("Level number must be an int")
        if not isinstance(goal, str):
            raise TypeError("Level goal must be a str")
        self.number = number
        self.goal = goal

def load_image(filename: str) -> pygame.Surface:
    """
    Load an image from the 'assets' directory.

    Args:
        filename (str): The name of the image file.

    Returns:
        pygame.Surface: The loaded image.

    Raises:
        ValueError: If filename is None or empty.
    """
    if not filename:
        raise ValueError("filename cannot be None or empty")

    image_path = os.path.join("assets", filename)
    try:
        return pygame.image.load(image_path)
    except pygame.error:
        # Create a white rectangle if the image could not be loaded
        image = pygame.Surface((CANDY_SIZE, CANDY_SIZE))
        image.fill((255, 255, 255))
        return image
    

def cargar_niveles():
    return [Nivel(1, 'Alcanza 1000 puntos'), Nivel(2, 'Recoge 5 monedas')]

def jugar_nivel(nivel: Nivel) -> None:
    """Jugar un nivel.

    Args:
        nivel (Nivel): El nivel a jugar.
    """
    global nivel_actual
    if nivel is None:
        raise ValueError("Nivel no puede ser nulo")
    print(f"Jugando nivel {nivel.numero}: {nivel.objetivo}")

def verificar_combinacion(caramelos):
    combinaciones = []
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if x < GRID_WIDTH - 2 and caramelos[y][x] is not None and caramelos[y][x + 1] is not None and caramelos[y][x + 2] is not None:
                try:
                    if caramelos[y][x].tipo == caramelos[y][x + 1].tipo == caramelos[y][x + 2].tipo:
                        combinaciones.append((x, y))
                        combinaciones.append((x + y))
                except AttributeError:
                    # Ignore if any of the candies are None
                    pass
# ...

super_piluka = SuperPiluka()
try:
    super_piluka.image = load_image('superpiluka.png')
except pygame.error as e:
    print(f"Error loading superpiluka image: {e}")

enemy = Enemy(500, 100)
try:
    enemy.image = load_image('enemy.png')
except pygame.error as e:
    print(f"Error loading enemy image: {e}")

# ...

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pantalla.fill((255, 255, 255))  # Fill the screen with white
    super_piluka.dibujar(pantalla)
    enemy.dibujar(pantalla)
    tablero.dibujar(pantalla)

    pygame.display.flip()  # Update the display
    pygame.time.Clock().tick(60)  # Limit the frame rate to 60 FPS
    
pygame.quit()