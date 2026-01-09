# _________           __                      ___________     ____________
#| ________|         / /          \  \ /  /  |_<__________|   |____________|
#| |_______         / /            \  /  /        |  |            |  |
#| ________|       / /               /  /         |  |            |  |
#| |_______       / /_______        /  /          |  |            |  |
#|_________|     /__________|      /__/           |__|            |__|

# Importation zone
import pygame

# --- Game Settings ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
INVADER_SIZE = (30, 30)
INVADER_COLORS = {
    1: (0, 255, 0),    # Green for life 1
    2: (255, 255, 0),  # Yellow for life 2
    3: (255, 0, 0),    # Red for life 3
}

# --- Invader Class ---
class Invader(pygame.sprite.Sprite):
    """Class to represent an invader."""
    
    def __init__(self, life, initial_position):
        super().__init__()
        self.life = life
        self.image = pygame.Surface(INVADER_SIZE)
        self.image.fill(INVADER_COLORS.get(life, (255, 255, 255)))  # Default to white
        self.rect = self.image.get_rect(topleft=initial_position)
        self.direction = 1  # 1 for right, -1 for left
        self.speed = 1

    def update(self):
        """Move the invader."""
        self.rect.x += self.speed * self.direction

# --- Functions ---
def generate_invaders(rows, cols, start_pos=(50, 50)):
    """Generates a grid of invaders recursively."""
    invaders = pygame.sprite.Group()

    def _generate(row, col):
        if row >= rows:
            return
        
        life = (row % 3) + 1
        x = start_pos[0] + col * (INVADER_SIZE[0] + 10)
        y = start_pos[1] + row * (INVADER_SIZE[1] + 10)
        
        invader = Invader(life, (x, y))
        invaders.add(invader)

        next_col = col + 1
        next_row = row
        if next_col >= cols:
            next_col = 0
            next_row += 1
        
        _generate(next_row, next_col)

    _generate(0, 0)
    return invaders

def move_invaders(invaders):
    """Moves the group of invaders and handles wall collision."""
    move_down = False

    for invader in invaders:
        if invader.rect.right > SCREEN_WIDTH - 50 or invader.rect.left < 50:
            move_down = True
            break
    
    if move_down:
        for invader in invaders:
            invader.direction *= -1
            invader.rect.y += INVADER_SIZE[1] + 5

def check_lose_condition(invaders):
    """Checks if any invader has reached the bottom of the screen."""
    for invader in invaders:
        if invader.rect.bottom >= SCREEN_HEIGHT:
            return True
    return False

# --- Main Game Loop ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders")

    all_invaders = generate_invaders(5, 10)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game state
        all_invaders.update()
        move_invaders(all_invaders)

        if check_lose_condition(all_invaders):
            print("You Lose!")
            running = False

        # Drawing
        screen.fill((0, 0, 0))  # Black background
        all_invaders.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()

