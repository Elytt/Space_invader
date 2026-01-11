import pygame

# ================== CONFIG ==================

LARGEUR, HAUTEUR = 800, 600
NOIR = (0, 0, 0)
VERT = (0, 255, 0)
JAUNE = (255, 255, 0)

VITESSE_JOUEUR = 5

INVADER_SIZE = (30, 30)
INVADER_COLORS = {
    1: (0, 255, 0),
    2: (255, 255, 0),
    3: (255, 0, 0),
}

# ================== INITIALISATION ==================

def initialiser_jeu():
    pygame.init()
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Space Invaders")
    horloge = pygame.time.Clock()
    return ecran, horloge

# ================== PROJECTILE ==================

class Projectile:
    def __init__(self, position, vitesse, direction):
        self.rect = pygame.Rect(position[0], position[1], 5, 10)
        self.vitesse = vitesse
        self.direction = direction
        self.actif = True

    def deplacer(self):
        self.rect.y += self.direction * self.vitesse
        if self.rect.bottom < 0 or self.rect.top > HAUTEUR:
            self.actif = False

# ================== INVADER ==================

class Invader:
    def __init__(self, life, position):
        self.life = life
        self.image = pygame.Surface(INVADER_SIZE)
        self.image.fill(INVADER_COLORS[life])
        self.rect = self.image.get_rect(topleft=position)
        self.direction = 1
        self.speed = 1

    def deplacer(self):
        self.rect.x += self.speed * self.direction

# ================== JOUEUR ==================

def creer_joueur():
    return pygame.Rect(LARGEUR // 2 - 20, HAUTEUR - 50, 40, 30)

def gerer_deplacement_joueur(joueur, touches):
    if touches[pygame.K_LEFT] and joueur.left > 0:
        joueur.x -= VITESSE_JOUEUR
    if touches[pygame.K_RIGHT] and joueur.right < LARGEUR:
        joueur.x += VITESSE_JOUEUR

# ================== INVADERS ==================

def generer_invaders(lignes, colonnes):
    invaders = []
    for row in range(lignes):
        for col in range(colonnes):
            life = (row % 3) + 1
            x = 60 + col * 50
            y = 50 + row * 50
            invaders.append(Invader(life, (x, y)))
    return invaders

# ================== COLLISIONS ==================

def collision_projectile_invader(projectile, invader):
    return projectile.rect.colliderect(invader.rect)

# ================== TIR ==================

def tirer_projectile(joueur, projectiles, dernier_tir):
    maintenant = pygame.time.get_ticks()
    if maintenant - dernier_tir > 400:
        x = joueur.centerx
        y = joueur.top
        projectiles.append(Projectile((x, y), 8, -1))
        return maintenant
    return dernier_tir

# ================== MAIN ==================

def main():
    ecran, horloge = initialiser_jeu()

    joueur = creer_joueur()
    projectiles = []
    invaders = generer_invaders(4, 10)

    dernier_tir = 0
    running = True

    while running:
        horloge.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        touches = pygame.key.get_pressed()
        gerer_deplacement_joueur(joueur, touches)

        if touches[pygame.K_SPACE]:
            dernier_tir = tirer_projectile(joueur, projectiles, dernier_tir)

        # Déplacement projectiles
        for p in projectiles:
            p.deplacer()

        # Collision projectile ↔ invader
        for projectile in projectiles:
            for invader in invaders[:]:
                if collision_projectile_invader(projectile, invader):
                    projectile.actif = False
                    invader.life -= 1
                    invader.image.fill(INVADER_COLORS.get(invader.life, (0, 0, 0)))
                    if invader.life <= 0:
                        invaders.remove(invader)
                    break

        projectiles = [p for p in projectiles if p.actif]

        # Déplacement invaders
        for invader in invaders:
            invader.deplacer()
            if invader.rect.right >= LARGEUR or invader.rect.left <= 0:
                invader.direction *= -1
                invader.rect.y += 10

        # AFFICHAGE
        ecran.fill(NOIR)
        pygame.draw.rect(ecran, VERT, joueur)

        for p in projectiles:
            pygame.draw.rect(ecran, JAUNE, p.rect)

        for invader in invaders:
            ecran.blit(invader.image, invader.rect)

        pygame.display.flip()

    pygame.quit()

# ================== LANCEMENT ==================

if __name__ == "__main__":
    main()
