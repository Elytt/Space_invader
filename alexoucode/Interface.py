import pygame 

# initialiser pygame
pygame.init()

# gestion des Images Par Seconde
ips = pygame.time.Clock()

# RESSOURCES

    # quelques couleurs prédéfinies
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
VERT_MORT = (94, 229, 77)
    # initialiser le module display
pygame.display.init()
    # dimensions de la fenêtre
LARGEUR = 800
HAUTEUR = 600
    # mettre un intitulé à la fenêtre
pygame.display.set_caption("⋊ Space Invader ⋉")
    # mettre une icône pour la fenêtre
icon_home = pygame.image.load('../assets/icon_home.ico')
pygame.display.set_icon(icon_home)
    # mettre un fond
bg = pygame.image.load('../assets/fond-ecran_accueil.png')
bg = pygame.transform.scale(bg, (LARGEUR, HAUTEUR))
    # image
vie_0 = pygame.image.load("../assets/vie_0.png")
vie_1 = pygame.image.load("../assets/vie_1.png")
vie_2 = pygame.image.load("../assets/vie_2.png")
vie_3 = pygame.image.load("../assets/vie_3.png")
vaisseau = pygame.image.load("../assets/vaisseau.png")
    # variable qui permet de garder le jeu ouvert
running = True
    # musique
pygame.mixer.music.load("../assets/musique.mp3")
pygame.mixer.music.play(-1) # jouer la musique indéfiniment
son_mort = pygame.mixer.Sound("../assets/son_mort.mp3")
    # police
police_titre = pygame.font.Font("../assets/police_pixels.ttf", 72) #(chemin, taille)
police_bouton = pygame.font.Font("../assets/police_pixels.ttf", 36)
police_mort = pygame.font.Font("../assets/police_pixels.ttf", 150)
police_mort_score = pygame.font.Font("../assets/police_pixels.ttf", 75)

# initialiser une fenêtre ou un écran pour display
ecran = pygame.display.set_mode( 
    size=(LARGEUR, HAUTEUR),
    flags= pygame.SHOWN, #créer une fenêtre affichée en mode visible
    depth=0, 
    display=0, 
    vsync=1 # avoir la syncronisation verticale
    )
INVADER_COLOR = 5
score = 15
nb_vie = 0 # nombre de vies de base

while running:     
    ecran.blit(bg, (0, 0)) # mettre l'image en fond d'écran de l'accueil

    for event in pygame.event.get():              
        if event.type == pygame.QUIT: # si on appuie sur la croix pour fermer la fenêtre
            running = False # on sort de la boucle
        if event.type == pygame.KEYDOWN: # si on appuie sur une touche
            if event.key == pygame.K_ESCAPE: # si on appuie sur la touche "Esc"
                running = False
    ecran.blit(
        pygame.transform.scale(pygame.image.load(f"../assets/vie_{nb_vie}.png"), (75, 75)),
        (5, 0)
        )
    if nb_vie <= 0 :
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(son_mort, 0)
        ecran.fill(VERT_MORT)
        text_mort = police_mort.render('GAME OVER !!!!', False, ROUGE)
        text_mort_score = police_mort_score.render(f'Ton score est de : {score * 500}', False, BLANC)
        ecran.blit(text_mort, (180,200))
        ecran.blit(text_mort_score, (180,300))
    if INVADER_COLOR <= 0 :
        score += 1
    ips.tick(60) # taux de rafraichissement de l'image à 60 images par secondes

    pygame.display.update()
pygame.quit() # on quitte pygame