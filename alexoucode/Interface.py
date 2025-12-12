import pygame 

# initialiser pygame
pygame.init()

# gestion des Images Par Seconde
ips = pygame.time.Clock()
ips.tick(20)

# quelques couleurs prédéfinies
bleu = (0, 0, 255)
rouge = (255, 0, 0)
vert = (0, 255, 0)
noir = (0, 0, 0)
blanc = (255, 255, 255)

# initialiser le module display
pygame.display.init() 

# mettre une icône pour la fenêtre
icon_home = pygame.image.load('assets/icon_home.ico')
pygame.display.set_icon(icon_home)

# mettre un intitulé à la fenêtre
pygame.display.set_caption("⋊ Space Invader ⋉")

# initialiser une fenêtre ou un écran pour display
ecran = pygame.display.set_mode( 
    size=(0, 0),
    flags=pygame.FULLSCREEN | pygame.RESIZABLE | pygame.SHOWN, #créer une fenêtre en plein écran, pouvant être redimentionée et elle est affichée en mode visible
    depth=0, 
    display=0, 
    vsync=1 # avoir la syncronisation verticale
    )

# mettre en couleur affichée de base le noir
ecran.fill(noir)

while True:     
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    ecran.fill(blanc)
         
    pygame.display.update()
    