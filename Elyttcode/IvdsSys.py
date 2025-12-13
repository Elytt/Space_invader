# _________           __                      ___________     ____________
#| ________|         / /          \  \ /  /  |_<__________|   |____________|
#| |_______         / /            \  /  /        |  |            |  |
#| ________|       / /               /  /         |  |            |  |
#| |_______       / /_______        /  /          |  |            |  |
#|_________|     /__________|      /__/           |__|            |__|

print("This code is for a school project only. You can use a part if you want but we are an open source project.\nReminder this file is only ONE PART OF THE ENTIRE PROJECT so please be respectful")


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
        self.waves = []
        self.invaders = []
        self.direction = 1 # 1 for right and -1 for left

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
wave_system.add_wave(Wave(medium_invader, count=6, start_row=1))
wave_system.add_wave(Wave(big_invader, count=3, start_row=2))
# Start waves
wave_system.start_waves()
