import pygame
from math import sin, cos, radians

class BallSimulation:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.radius = 30
        # Box dimensions
        self.box_width = 200
        self.box_height = 300
        self.box_x = 50
        self.box_y = (self.display_surface.get_height() - self.box_height) // 2
        # Ball position relative to box
        self.center_x = self.box_x + self.box_width // 2
        self.center_y = self.box_y + self.box_height // 2
        self.angle = 0
        self.rotation_speed = 2
        self.color = '#b68f40'  # Matching the UI gold color
        self.orbit_radius = 20

    def update(self, dt):
        # Draw container box
        pygame.draw.rect(self.display_surface, 'white', 
                        (self.box_x, self.box_y, self.box_width, self.box_height), 2)

        # Update angle
        self.angle = (self.angle + self.rotation_speed) % 360

        # Calculate orbit position within box bounds
        orbit_x = self.center_x + cos(radians(self.angle)) * self.orbit_radius
        orbit_y = self.center_y + sin(radians(self.angle)) * self.orbit_radius

        # Draw the ball
        pygame.draw.circle(self.display_surface, self.color, (orbit_x, orbit_y), self.radius)

#Example usage (requires a pygame initialization)
#pygame.init()
#screen = pygame.display.set_mode((800, 600))
#simulation = BallSimulation()
#running = True
#while running:
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            running = False
#    screen.fill((0,0,0)) #Black background
#    simulation.update(0) #dt =0 for simplicity
#    pygame.display.flip()
#pygame.quit()