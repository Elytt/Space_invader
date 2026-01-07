class Projectile:
    """
    Cette classe représente un projectile (ex: une comète, une balle, un laser).
    """

    def __init__(self, position, vitesse, direction):
        """
    position  : tuple (x, y) → position de départ
        vitesse   : int → vitesse de déplacement
        direction : tuple (dx, dy) → direction du projectile
        """
        self.x, self.y = position
        self.vitesse = vitesse
        self.dx, self.dy = direction
        self.actif = True  # Le projectile est actif tant qu'il n'a pas touché quelque chose

    def deplacer(self):
        """
        Déplace le projectile selon sa direction et sa vitesse
        """
        self.x += self.dx * self.vitesse
        self.y += self.dy * self.vitesse

    def position_actuelle(self):
        """
        Retourne la position actuelle du projectile
        """
        return (self.x, self.y)


def tirer_projectile(position_depart):
    """
    Crée un projectile qui monte vers le haut de l'écran
    """
    vitesse = 1
    direction = (0, -1)  # Vers le haut
    return Projectile(position_depart, vitesse, direction)

def collision(projectile, invader):
    """
    Vérifie si le projectile touche un invader
    Ici on compare simplement les positions (logique simple)
    """
    if projectile.position_actuelle() == invader.position:
        return True
    return False
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
