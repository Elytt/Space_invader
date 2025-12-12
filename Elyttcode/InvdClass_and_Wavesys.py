# _________           __                      ___________     ____________
#| ________|         / /          \  \ /  /  |___________|   |____________|
#| |_______         / /            \  /  /        |  |            |  |
#| ________|       / /               /  /         |  |            |  |
#| |_______       / /_______        /  /          |  |            |  |
#|_________|     /__________|      /__/           |__|            |__|
class Invaders:  # Create invader class
    def __init__(self, life, position):
        self.position = position
        self.life = life

    def __str__(self):
        return f"Invader at {self.position} with life {self.life}"

    @staticmethod
    def create_invader_grid(rows, cols):
        grid = []
        for row in range(rows):
            for col in range(cols):
                if row == 0:
                    life = 1  # Small Invader
                elif row == 1:
                    life = 2  # Medium Invader
                else:
                    life = 3  # Big Invader

                invader = Invaders(life, (row, col))
                grid.append(invader)
        return grid

class Wave:
    def __init__(self, invader_type, count, start_row=0):
        self.invader_type = invader_type
        self.count = count
        self.start_row = start_row  # Start position for the wave

    def create_invaders(self):
        invaders = []
        for i in range(self.count):
            position = (self.start_row, i)  # Unique position for each invader
            invader = Invaders(self.invader_type.life, position)
            invaders.append(invader)
        return invaders

class WaveSystem:
    def __init__(self):
        self.waves = []

    def add_wave(self, wave):
        self.waves.append(wave)

    def start_waves(self):
        for wave in self.waves:
            print(f"Starting wave of {wave.count} invaders!")
            invaders = wave.create_invaders()
            for invader in invaders:
                print(invader)  # Display or process each invader
            print("Wave completed.\n")


# Create invader types
small_invader = Invaders(1, (0, 0))
medium_invader = Invaders(2, (0, 0))
big_invader = Invaders(3, (0, 0))

# Initialize the wave system
wave_system = WaveSystem()

# Create and add waves
wave_system.add_wave(Wave(small_invader, count=10, start_row=0))
wave_system.add_wave(Wave(medium_invader, count=8, start_row=1))
wave_system.add_wave(Wave(big_invader, count=5, start_row=2))

# Start waves
wave_system.start_waves()
