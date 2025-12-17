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
# initialiser le module display
pygame.display.init()
# dimensions de la fenêtre
longueur = 800
largeur = 500
# mettre une icône pour la fenêtre
icon_home = pygame.image.load('../assets/icon_home.ico')
pygame.display.set_icon(icon_home)
# mettre un fond
bg = pygame.image.load('../assets/fond-ecran_accueil.png')
bg = pygame.transform.scale(bg, )
# variable qui permet de garder le jeu ouvert
running = True



# initialiser une fenêtre ou un écran pour display
ecran = pygame.display.set_mode( 
    size=(longueur, largeur),
    flags=pygame.RESIZABLE | pygame.SHOWN, #créer une fenêtre en plein écran et elle est affichée en mode visible
    depth=0, 
    display=0, 
    vsync=1 # avoir la syncronisation verticale
    )

running = True
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
    ips.tick(60) # taux de rafraichissement de l'image à 20 images par secondes

    pygame.display.update()
pygame.quit() # on quitte pygame
