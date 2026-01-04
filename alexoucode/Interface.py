import pygame 

# initialiser pygame
pygame.init()

# gestion des Images Par Seconde
ips = pygame.time.Clock()

# RESSOURCES

    # quelques couleurs prédéfinies
bleu = (0, 0, 255)
rouge = (255, 0, 0)
vert = (0, 255, 0)
noir = (0, 0, 0)
blanc = (255, 255, 255)
vert_mort = (94, 229, 77)
    # initialiser le module display
pygame.display.init()
    # dimensions de la fenêtre
longueur = 800
largeur = 600
    # mettre un intitulé à la fenêtre
pygame.display.set_caption("⋊ Space Invader ⋉")
    # mettre une icône pour la fenêtre
icon_home = pygame.image.load('../assets/icon_home.ico')
pygame.display.set_icon(icon_home)
    # mettre un fond
bg = pygame.image.load('../assets/fond-ecran_accueil.png')
bg = pygame.transform.scale(bg, (longueur, largeur))
    # variable qui permet de garder le jeu ouvert
running = True
    # musique
pygame.mixer.music.load("../assets/musique.mp3")
pygame.mixer.music.play(-1)
son_mort = pygame.mixer.Sound("../assets/son_mort.mp3")
    # police
police_titre = pygame.font.Font("../assets/police_pixels.ttf", 72) #(chemin, taille)
police_bouton = pygame.font.Font("../assets/police_pixels.ttf", 36)
police_normale = pygame.font.Font("../assets/police_pixels.ttf", 30)

# initialiser une fenêtre ou un écran pour display
ecran = pygame.display.set_mode( 
    size=(longueur, largeur),
    flags= pygame.SHOWN, #créer une fenêtre affichée en mode visible
    depth=0, 
    display=0, 
    vsync=1 # avoir la syncronisation verticale
    )


d = True
while running:     
    ecran.blit(bg, (0, 0)) # mettre l'image en fond d'écran de l'accueil

    for event in pygame.event.get():              
        if event.type == pygame.QUIT: # si on appuie sur la croix pour fermer la fenêtre
            running = False # on sort de la boucle
        if event.type == pygame.KEYDOWN: # si on appuie sur une touche
            if event.key == pygame.K_ESCAPE: # si on appuie sur la touche "Esc"
                running = False # on sort de la boucle
        if event.type == pygame.WINDOWMOVED: # si on bouge la fenêtre
            ecran.fill(vert)
    if d == True :
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(son_mort)
        ecran.fill(vert_mort)
        text_mort = police_normale.render('GAME OVER !!!!', False, rouge, (0, 0, 0))
        ecran.blit(text_mort, (0,0))
    ips.tick(60) # taux de rafraichissement de l'image à 60 images par secondes

    pygame.display.update()
pygame.quit() # on quitte pygame