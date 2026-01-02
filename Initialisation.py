import pygame

# --- CONFIGURATION GLOBALE ---
LARGEUR, HAUTEUR = 800, 600 #taille de la fenètre
VITESSE_JOUEUR = 5  #Valeur qui pourra être modifiée 
NOIR = (0, 0, 0) #Couleur du fond

def initialiser_jeu(titre="Space Invaders", l=LARGEUR, h=HAUTEUR):
    """
    Initialise la bibliothèque Pygame et crée la fenêtre
    Arguments: titre (str), l (int), h (int)
    Retour: tuple (ecran, horloge)
    """
    pygame.init()
    ecran = pygame.display.set_mode((l, h))
    pygame.display.set_caption(titre)
    horloge = pygame.time.Clock()
    return ecran, horloge

def creer_joueur():
    """
    Crée le joueur (rectangle vert) et définit la position de départ du joueur
    Retour: pygame.Rect
    """
    joueur = pygame.Rect(LARGEUR // 2, HAUTEUR - 50, 40, 30) #Sprite à ajouter après mais pour l'instant c'est un rectangle :)
    return joueur

def gerer_deplacement_joueur(joueur, touches):
    """
    Modifie la position du joueur selon les touches pressées 
    Arguments: joueur (pygame.Rect), touches (pygame.key.get_pressed)
    """
    if touches[pygame.K_LEFT] and joueur.left > 0:
        joueur.x -= VITESSE_JOUEUR
    if touches[pygame.K_RIGHT] and joueur.right < LARGEUR:
        joueur.x += VITESSE_JOUEUR




def main():
    """
    Lance le jeu
    Pas d'arguments
    """
    ecran, horloge = initialiser_jeu()
    joueur = creer_joueur()
    en_cours = True

    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False

        touches = pygame.key.get_pressed()
        gerer_deplacement_joueur(joueur, touches)

        ecran.fill(NOIR)
        pygame.draw.rect(ecran, (0, 255, 0), joueur) # On dessine un rectangle vert
        pygame.display.flip()
        horloge.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()