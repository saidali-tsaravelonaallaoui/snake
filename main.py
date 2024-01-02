# Created Date: Tuesday, December 19th 2023, 11:21:01 AM
# Author: Said Ali Tsaravelona Allaoui
# -----
# Last Modified: Thursday, December 21th 2023, 10:20:01 AM
# Modified By: Said Ali Tsaravelona Allaoui
# ------------------------------------

import pygame
from pygame.locals import *
import time
import random


TAILLE = 40
BACKGROUND_COLOR = (100,165,67)

class Pomme:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.pomme = pygame.image.load("ressource/pomme.jpg").convert() # Importation de l'image de la tete
        self.x = TAILLE*3
        self.y = TAILLE*3
    # Affichage de la pomme    
    def draw(self):
        self.parent_screen.blit(self.pomme,(self.x,self.y)) # Position de la tete
        pygame.display.flip()
        
    # Position aleatoire de la pomme    
    def move(self):
        self.x = random.randint(1,24)*TAILLE
        self.y = random.randint(1,19)*TAILLE
        
class Snake:
    def __init__(self, parent_screen, longueur):
        self.parent_screen = parent_screen
        self.tete = pygame.image.load("ressource/tete.jpg").convert() # Importation de l'image de la tete
        self.direction = "down"
        
        self.longueur = longueur
        self.x = [TAILLE]*longueur
        self.y = [TAILLE]*longueur
        
     # Ajout de la longueur du serpent   
    def ajt_longueur(self):
        self.longueur+=1
        self.x.append(-1)
        self.y.append(-1)
        
    # Mouvement du serpent    
    def move_up(self):
        if self.direction != "down":
            self.direction = "up"

    def move_down(self):
        if self.direction != "up":
            self.direction = "down"

    def move_left(self):
        if self.direction != "right":
            self.direction = "left"

    def move_right(self):
        if self.direction != "left":
            self.direction = "right"
        
    # Affichage du serpent    
    def draw(self):
        self.parent_screen.fill((BACKGROUND_COLOR))
        for i in range(self.longueur):
            self.parent_screen.blit(self.tete,(self.x[i],self.y[i])) # Position de la tete
        pygame.display.flip()
        
    # Deplacement du serpent    
    def moving(self):
        for i in range(self.longueur-1,0,-1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "left":
            self.x[0] -= TAILLE
            if self.x[0] < 0:  # Si la tête dépasse à gauche
                self.x[0] = 1000 - TAILLE  # Réapparition à droite

        if self.direction == "right":
            self.x[0] += TAILLE
            if self.x[0] >= 1000:  # Si la tête dépasse à droite
                self.x[0] = 0  # Réapparition à gauche

        if self.direction == "up":
            self.y[0] -= TAILLE
            if self.y[0] < 0:  # Si la tête dépasse en haut
                self.y[0] = 800 - TAILLE  # Réapparition en bas

        if self.direction == "down":
            self.y[0] += TAILLE
            if self.y[0] >= 800:  # Si la tête dépasse en bas
                self.y[0] = 0  # Réapparition en haut

        self.draw()

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game by SAID ALI TSARAVELONA ALLAOUI")
        
        pygame.mixer.init()
        self.ecran = pygame.display.set_mode((1000, 800)) # Taille de la fenetre
        self.ecran.fill((18,52,26)) # Couleur de fond de la fenetre
        self.snake = Snake (self.ecran, 1)
        self.snake.draw()
        self.pomme = Pomme (self.ecran)
        self.pomme.draw()
    
    def collusion(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + TAILLE:
            if y1 >= y2 and y1 < y2 + TAILLE:
                return True
        return False
    
    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"ressource/{sound}.mp3") # Importation du son
        pygame.mixer.Sound.play(sound)
    
   # Fonction du jeu     
    def play(self):
        self.snake.moving()
        self.pomme.draw()
        self.affiche_score()
        
        pygame.display.flip()
        
        # Collusion avec la pomme
        if self.collusion(self.snake.x[0], self.snake.y[0], self.pomme.x, self.pomme.y):
            self.play_sound("ding")
            self.snake.ajt_longueur() # Ajout de la longueur du serpent
            self.pomme.move() # Position aleatoire de la pomme
            
        # Collusion avec lui meme
        for i in range(3,self.snake.longueur):
            if self.collusion(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]): 
                self.play_sound("crash")
                raise "Game Over" 
        
    def affiche_game_over(self): # Affichage du game over
        self.ecran.fill(BACKGROUND_COLOR) 
        font = pygame.font.SysFont('arial',30) 
        ligne1 = font.render(f"Fin de la partie ! Votre score est de {self.snake.longueur}", True, (255, 255, 255)) 
        self.ecran.blit(ligne1, (300,350))
        ligne2 = font.render("Pour rejouer appuyer sur la touche Espace, ou la touche Echap pour Quitter", True, (255, 255, 255))
        self.ecran.blit(ligne2, (80,400))
        pygame.display.flip()
        
        
    def affiche_score(self): # Affichage du score
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score : {self.snake.longueur}", True, (255, 255, 255))
        self.ecran.blit(score, (800,10))
        
    def run(self):
        run = True
        pause = False
        while run:
            for event in pygame.event.get():
                if event.type == KEYDOWN: 
                    if event.key == K_ESCAPE: 
                        run = False 
                        
                    if event.key == K_SPACE:
                        pause = False
                        self.snake = Snake(self.ecran, 1)
                        self.pomme = Pomme(self.ecran)
                    
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                            
                        if event.key == K_DOWN:
                            self.snake.move_down()
                            
                        if event.key == K_LEFT:
                            self.snake.move_left()
                            
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        
                elif event.type == QUIT:
                    run = False
            
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.affiche_game_over()
                pause = True
            
            time.sleep(0.1) # Vitesse du serpent

if __name__ == "__main__":
    game = Game()
    game.run()