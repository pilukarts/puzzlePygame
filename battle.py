import sys
import pygame
import os
import random

from main import CANDY_SIZE


# Inicializa Pygame
pygame.init()

# Define la pantalla del juego
pantalla = pygame.display.set_mode((800, 600))

# Define la función load_image
def load_image(filename: str) -> pygame.Surface:
    """Carga una imagen de forma rápida y eficiente.

    Args:
        filename (str): El nombre del archivo de la imagen.

    Returns:
        pygame.Surface: La imagen cargada.
    """
    # Utiliza el cacheo de Pygame para evitar cargar la imagen varias veces
    image = pygame.image.load('assets/' + filename)
    image = image.convert_alpha()
    return image

# Define la clase base Sprite
class Sprite(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pygame.Surface) -> None:
        """Constructor de la clase Sprite.

        Args:
            x (int): La posición x del sprite.
            y (int): La posición y del sprite.
            image (pygame.Surface): La imagen del sprite.
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def dibujar(self, pantalla: pygame.Surface) -> None:
        """Dibuja el sprite en la pantalla.

        Args:
            pantalla (pygame.Surface): La pantalla donde dibujar.
        """
        pantalla.blit(self.image, self.rect)

# Define las clases que heredan de Sprite
class Caramelo(Sprite):
    def __init__(self, x: int, y: int) -> None:
        """Constructor de la clase Caramelo.

        Args:
            x (int): La posición x del caramelo.
            y (int): La posición y del caramelo.

        """
        image = load_image('caramelo.png')
        super().__init__(x, y, image)

    def ocurre_colision(self, otro: pygame.sprite.Sprite) -> bool:
        """Verifica si ocurre una colisión entre este caramelo y otro sprite.

        Args:
            otro (pygame.sprite.Sprite): El otro sprite con el que se verifica la colisión.

        Returns:
            bool: True si ocurre una colisión, False en caso contrario.
        """
        return self.rect.colliderect(otro.rect)

class Coin(Sprite):
    def __init__(self, x, y):
        """Constructor de la clase Coin.

        Args:
            x (int): La posición x de la moneda.
            y (int): La posición y de la moneda.
        """
        image = load_image('coin.png')
        super().__init__(x, y, image)

class SuperPiluka(Sprite):
    def __init__(self, x, y):
        # Llama al constructor de la clase base (Sprite)
        super().__init__(x, y, load_image('superpiluka.png'))

    def dibujar(self, pantalla):
        # Llama al método dibujar de la clase base (Sprite)
        super().dibujar(pantalla)

class Enemy(Sprite):
    def __init__(self, x, y, speed=8):
        """Constructor de la clase Enemy.

        Args:
            x (int): La posición x del enemigo.
            y (int): La posición y del enemigo.
            speed (int, optional): La velocidad del enemigo. Defaults to 8.
        """
        super().__init__(x, y, load_image('enemy.png'))
        self.speed = speed

    def update(self):
        """Mueve el enemigo en el eje x.

        Si el enemigo llega al borde de la pantalla, cambia de dirección.
        """
        self.x += self.speed
        if self.x > 800 - self.image.get_width() or self.x < 0:
            self.speed *= -1


# Define el bucle principal del juego
while True:
    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Dibuja los sprites
    pantalla.fill((255, 255, 255))
    caramelo = Caramelo(100, 100)
    caramelo.dibujar(pantalla)
    coin = Coin(200, 200)
    coin.dibujar(pantalla)
    super_piluka = SuperPiluka(300, 300)
    super_piluka.dibujar(pantalla)
    enemy = Enemy(400, 400)
    enemy.dibujar(pantalla)

    # Actualiza la pantalla
    pygame.display.flip()
    pygame.time.Clock().tick(60)