import pygame
import random
from main import Enemy, load_image
from main import SuperPiluka
import sys
from main import Tablero
import os
import main

print(dir(main))

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


# Create instances of SuperPiluka, Enemy, and Tablero
super_piluka = SuperPiluka()
enemy = Enemy(500, 100)  # Pass x and y coordinates
tablero = Tablero()

# Create the game window
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Constantes
CANDY_SIZE = 30
CANDY_TYPES = ['rojo', 'verde', 'azul', 'amarillo', 'arcoiris']

# Create instances of SuperPiluka, Enemy, and Tablero
super_piluka = SuperPiluka()
enemy = Enemy(500, 100)  # Pass x and y coordinates
tablero = Tablero()

    # Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Draw everything
    screen.fill((255, 255, 255))  # Fill the screen with white
    super_piluka.dibujar(screen)
    enemy.dibujar(screen)
    tablero.dibujar(screen)

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Limit the frame rate to 60 FPS

# Clase Caramelo
class Caramelo:
    def __init__(self, tipo, x, y):
        self.tipo = tipo
        self.image = load_image(f'{tipo}.png')
        self.image = pygame.transform.scale(self.image, (CANDY_SIZE, CANDY_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)

# Clase SuperPiluka
class SuperPiluka:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image('superpiluka.png')
        self.image = pygame.transform.scale(self.image, (CANDY_SIZE, CANDY_SIZE))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    def dibujar(self, pantalla):
        """
        Dibuja la nave en la pantalla.
        """
        pantalla.blit(self.image, self.rect)

    def move(self, delta_x: int) -> None:
        """
        Move the spaceship by delta_x pixels to the right.
        """
        self.x += delta_x
        self.rect.topleft = (self.x, self.y)

    def saltar(self):
        """
        Mueve la nave hacia arriba 50 pixeles.
        """
        self.y -= 50
        self.rect.topleft = (self.x, self.y)

# Clase Enemy
class Enemy:
    def __init__(self, x=500, y=100):
        self.x = x
        self.y = y
        self.image = load_image('enemy.png')
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)

    def lanzar_golpe(self, super_piluka):
        # Lanzar un golpe hacia Super Piluka
        if self.rect.colliderect(super_piluka.rect):
            print("Super Piluka fue golpeado!")
        else:
            print("El golpe fall ")

# Clase Tablero
class Tablero:
    def __init__(self):
        # Initialize the Tablero class
        self.caramelos = []

    def generar_caramelos(self):
        for y in range(2):
            for x in range(10):
                tipo = random.choice(CANDY_TYPES)
                caramelo = Caramelo(tipo, x * CANDY_SIZE, y * CANDY_SIZE)
                self.caramelos.append(caramelo)

    def dibujar(self, pantalla):
        for caramelo in self.caramelos:
            caramelo.dibujar(pantalla)

# Crear Super Piluka, enemigo y tablero
super_piluka = SuperPiluka()
enemy = Enemy(500, 100)  # Replace with the desired x and y coordinates
tablero = Tablero()

# Dibujar Super Piluka, enemigo y tablero
pantalla = pygame.display.set_mode((600, 600))
super_piluka.dibujar(pantalla)
enemy.dibujar(pantalla)  # Corrected line
tablero.dibujar(pantalla)
pygame.display.flip()