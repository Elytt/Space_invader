import pygame
from Elyttcode.Invaders import *#import des Invaders

# --- CONFIGURATION GLOBALE ---

LARGEUR, HAUTEUR = 800, 600 #taille de la fenètre
VITESSE_JOUEUR = 5  #Valeur qui pourra être modifiée 
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
VERT_MORT = (94, 229, 77)
NB_VIE = 3
SCORE = 0
GAME_OVER = False

# ---------- CONFIGURATION DES ASSETS ----------
    # images
vaisseau = pygame.image.load("assets/vaisseau.png")         # charger l'image du vaisseau
bg = pygame.image.load('assets/fond-ecran_accueil.png')  # charger l'image du fond d'écran
bg = pygame.transform.scale(bg, (LARGEUR, HAUTEUR))         # adapter la taille du fond d'éecran à celle de la taille de la fenêtre
vie_liste = [pygame.image.load("assets/vie_0.png"), pygame.image.load("assets/vie_1.png"), pygame.image.load("assets/vie_2.png"), pygame.image.load("assets/vie_3.png")] 
# charger les images du niveau de vie 0, 1, 2 et 3 


def initialiser_jeu(titre="⋊ Space Invader ⋉", l=LARGEUR, h=HAUTEUR, icon_home=pygame.image.load('assets/icon_home.ico')):
    """
    Initialise la bibliothèque Pygame, crée la fenêtre, lui met une description et une icône
    Arguments: titre (str), l (int), h (int), icon_home (Surface)
    Retour: tuple (ecran, horloge)
    """
    global SON_MORT, police_mort, police_mort_score
    
    pygame.init()
    ecran = pygame.display.set_mode((l, h))
    
    pygame.display.set_caption(titre)
    pygame.display.set_icon(icon_home)
        # musique
    pygame.mixer.music.load("assets/musique.mp3")               # charger le fichier audio de la musique
    pygame.mixer.music.play(-1)                                 # jouer la musique et la jouer indéfiniment 
    SON_MORT = pygame.mixer.Sound("assets/son_mort.mp3")        # charger le son de mort du vaisseau
        # police
    police_titre = pygame.font.Font("assets/police_pixels.ttf", 72) #(chemin, taille)
    police_bouton = pygame.font.Font("assets/police_pixels.ttf", 36)
    police_mort = pygame.font.Font("assets/police_pixels.ttf", 150)
    police_mort_score = pygame.font.Font("assets/police_pixels.ttf", 75)
    
    
    horloge = pygame.time.Clock()
    return ecran, horloge


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
        return (self.rect.x, self.rect.y)


def update_projectiles(projectiles, invaders):
    """
    Met à jour tous les projectiles :
    - déplacement
    - collision
    - suppression si nécessaire
    """
    global SCORE
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
                    invader.kill()
                    SCORE += 1

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
    delai_tir = 400  # 4s00 millisecondes entre chaque tir

    if touches[pygame.K_SPACE]:
        if maintenant - dernier_tir > delai_tir:
            # On centre le tir sur le joueur
            x = position_depart[0] + 22 # Ajustement pour être au milieu du vaisseau
            y = position_depart[1]
            
            nouveau_projectile = Projectile((x, y), 12, -1)
            liste_projectiles.append(nouveau_projectile)
            return maintenant # On renvoie l'heure du tir pour mettre à jour le chrono entre tirs
            
    return dernier_tir # Si on a pas tiré on renvoie l'ancien chrono 


#------- COLLISIONS --------


def collision(projectile, invader):
    """
    Vérifie si le projectile touche un invader
    Ici on renvoie True si une collition es détecté avec l'invader et sinon False
    """
    return projectile.rect.colliderect(invader.rect)




#---------- LANCEMENT DU JEU ----------

def main():
    global NB_VIE, SCORE, GAME_OVER, vie_liste # pour pouvoir accéder aux deucx variables en dehors de la fonction main()
    """
    Lance le jeu
    Pas d'arguments
    """
    ecran, horloge = initialiser_jeu()
    joueur = creer_joueur()

    liste_projectiles = []
    projectiles_ennemis = []
    all_invaders = generate_invaders(3, 10)


    dernier_tir = 0

    en_cours = True

    while en_cours:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:   # si on appuie sur la croix pour fermer la fenêtre
                en_cours = False    # sortir de la boucle du jeu et donc le fermer
            if event.type == pygame.KEYDOWN:    # si on appuie sur une touche
                if event.key == pygame.K_ESCAPE:    # Si cette touche est "Esc"
                    en_cours = False

        if GAME_OVER == True :
            ecran.fill(VERT_MORT)
            
            text_mort = police_mort.render('GAME OVER !!!!', False, ROUGE)
            text_mort_score = police_mort_score.render(f'Ton score est de : {SCORE * 500}', False, BLANC)
            
            ecran.blit(text_mort, (180,200))
            ecran.blit(text_mort_score, (180,300))
            pygame.display.flip()
            horloge.tick(60)
            continue

# --- Tir des Invaders ---
        for invader in all_invaders:
            if hasattr(invader, 'shoot') and invader.shoot(chance=1000):
                nouveau_tir = Projectile(invader.rect.midbottom, 3, 1)
                projectiles_ennemis.append(nouveau_tir)
        all_invaders.update()       # Fait bouger les aliens individuellement
        move_invaders(all_invaders) # Gère le rebond sur les murs et la descente
                

# --- Mise à jour des projectiles ennemis ---

        for p_ennemi in projectiles_ennemis:
            p_ennemi.deplacer()
            # Vérifier si le joueur est touché
            if p_ennemi.rect.colliderect(joueur):
                print("Attention : Le vaisseau a été abimé !")
                NB_VIE -= 1
                time.sleep(0.1)
                p_ennemi.actif = False
                break

# Nettoyage des projectiles ennemis hors écran
        projectiles_ennemis[:] = [p for p in projectiles_ennemis if p.actif]
        #end nettoyage

        touches = pygame.key.get_pressed()
        gerer_deplacement_joueur(joueur, touches)

        dernier_tir = tirer_projectile(touches, (joueur.x, joueur.y), liste_projectiles, dernier_tir)

        update_projectiles(liste_projectiles, all_invaders) #On met à jour les projectiles (déplacement)

        ecran.blit(bg, (0, 0)) # afficher l'image du fond d'écran
        
        ecran.blit(
            pygame.transform.scale(vie_liste[NB_VIE], (75, 75)), # afficher les images de vie; en x = 75 et y = 75
            (5, 0)
            )
        
        ecran.blit(vaisseau, joueur) # On affiche l'image du vaisseau sur le joueur
        all_invaders.draw(ecran)    # Dessine les aliens sur l'écran

        
        for proj in liste_projectiles: #on dessine les projectiles 
                pygame.draw.rect(ecran, (255, 255, 0), proj.rect)
        for p_ennemi in projectiles_ennemis:
            pygame.draw.rect(ecran, (255, 0, 0), p_ennemi.rect)

        if (NB_VIE <= 0 or check_lose_condition(all_invaders)) and not GAME_OVER :
            GAME_OVER = True
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(SON_MORT, 0)

        if check_win_condition(all_invaders):
            ecran.fill(VERT) # Un beau vert pour la victoire
            text_victoire = police_mort.render('VICTOIRE !', False, BLANC)
            ecran.blit(text_victoire, (200, 250))
            pygame.display.flip()
            pygame.time.wait(3000) # Attendre 3 secondes avant de fermer
            en_cours = False
            

        pygame.display.flip()
        horloge.tick(60)


    pygame.quit()

if __name__ == "__main__":
    main()
