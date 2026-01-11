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

# ---------- CONFIGURATION DES ASSETS ----------
vaisseau = pygame.image.load("assets/vaisseau.png")

#------------------ PROJECTILES ---------------

class Projectile:
    """
    Cette classe représente un projectile (ex: une comète, une balle, un laser).
    """

    def __init__(self, position, vitesse, direction):
        """
        position : tuple (x,y) → Défini où le projectif apparait
        vitesse   : int → vitesse de déplacement
        direction : int → direction du projectile (déplacement sur l'axe y)
        actif : bool → Voir si le projectif est présent ou non

        """
        # On crée un rectangle pour le projectile (5x10 pixels par exemple)
        self.rect = pygame.Rect(position[0], position[1], 5, 10)
        self.vitesse = vitesse
        self.direction = direction # -1 pour monter, 1 pour descendre
        self.actif = True


    def deplacer(self):
        """
        Déplace le projectile selon sa direction et sa vitesse
        """
        self.rect.y += (self.direction * self.vitesse)
        
        # Si le projectile sort de l'écran (en haut ou en bas), il devient inactif
        if self.rect.y < 0 or self.rect.y > HAUTEUR:
            self.actif = False


    def position_actuelle(self):
        """
        Retourne la position actuelle du projectile
        """
        return (self.x, self.y)


def update_projectiles(projectiles, invaders):
    """
    Met à jour tous les projectiles :
    - déplacement
    - collision
    - suppression si nécessaire
    """

    for projectile in projectiles:
        if not projectile.actif:
            continue

        # Déplacer le projectile
        projectile.deplacer()

        # Vérifier les collisions
        for invader in invaders:
            if collision(projectile, invader):
                invader.life -= 1
                projectile.actif = False

                print(f"💥 Invader touché ! Vie restante : {invader.life}")

                # Si l'invader n'a plus de vie
                if invader.life <= 0:
                    print("👾 Invader détruit !")
                    invaders.remove(invader)

                break

    # Supprimer les projectiles inactifs
    projectiles[:] = [p for p in projectiles if p.actif]




# ------------- JOUEUR --------

def creer_joueur():
    """
    Crée le joueur (rectangle vert) et définit la position de départ du joueur
    Retour: pygame.Rect
    """
    joueur = vaisseau.get_rect() # créer un rectangle qui correspond aux dimensions de l'image
    joueur.midbottom = (LARGEUR // 2, HAUTEUR - 30) # placer le joueur sur la moitié de l'écran en abscisse et à 30 px au dessus du bas de la fenêtre
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

def tirer_projectile(touches, position_depart, liste_projectiles, dernier_tir):
    """
    Crée un projectile si Espace est pressé et si le temps de recharge est passé
    """
    maintenant = pygame.time.get_ticks()
    delai_tir = 500  # 500 millisecondes entre chaque tir

    if touches[pygame.K_SPACE]:
        if maintenant - dernier_tir > delai_tir:
            # On centre le tir sur le joueur
            x = position_depart[0] + 22 # Ajustement pour être au milieu du vaisseau
            y = position_depart[1]
            
            nouveau_projectile = Projectile((x, y), 10, -1)
            liste_projectiles.append(nouveau_projectile)
            return maintenant # On renvoie l'heure du tir pour mettre à jour le chrono entre tirs
            
    return dernier_tir # Si on a pas tiré on renvoie l'ancien chrono 


#------- COLLISIONS --------


def collision(projectile, invader):
    """
    Vérifie si le projectile touche un invader
    Ici on compare simplement les positions (logique simple)
    """
    if projectile.position_actuelle() == invader.position:
        return True
    return False




#---------- LANCEMENT DU JEU ----------

def main():
    """
    Lance le jeu
    Pas d'arguments
    """
    ecran, horloge = initialiser_jeu()
    joueur = creer_joueur()

    liste_projectiles = []
    invaders = []

    dernier_tir = 0

    en_cours = True

    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False

        touches = pygame.key.get_pressed()
        gerer_deplacement_joueur(joueur, touches)

        dernier_tir = tirer_projectile(touches, (joueur.x, joueur.y), liste_projectiles, dernier_tir)

        update_projectiles(liste_projectiles, invaders) #On met à jour les projectiles (déplacement)


        ecran.fill(NOIR)

        ecran.blit(vaisseau, joueur) # On affiche l'image du vaisseau sur le joueur

        for proj in liste_projectiles: #on dessine les projectiles 
                pygame.draw.rect(ecran, (255, 255, 0), proj.rect)

        pygame.display.flip()
        horloge.tick(60)


    pygame.quit()

if __name__ == "__main__":
    main()

 