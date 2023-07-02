#init stuff
import pygame
import random
from particle import Particle

pygame.init()

#makes a new class
class Particle_System:

    #this method is always called when a new instance of a class is created
    def __init__(self, particle_amount, img, x, y, vector_min, vector_max, speed_min, speed_max, lifetime_min, lifetime_max):
        
        #creating all the values the particle needs
        self.particle_amount = particle_amount
        
        self.img = img

        self.x = x

        self.y = y

        self.vector_constraints = [vector_min, vector_max]

        self.speed_constraints = [speed_min, speed_max]

        self.lifetime_constraints = [lifetime_min, lifetime_max]
        
        self.particles = []

    #draw method, must be placed after background is drawn but before display is updated
    def draw(self, screen, camera):

        #iterates through each particle in the system
        for particle in self.particles:

           particle.draw(screen, camera)

    #update method, moves the particles, and creates and removes them as needed
    def update(self):

        for particle in self.particles:

            if particle.dead == True:

                self.particles.remove(particle)

        if len(self.particles) < self.particle_amount:

            new_particle = Particle(self.img, self.x, self.y,
            random.randint(self.vector_constraints[0], self.vector_constraints[1]),
            random.randint(self.speed_constraints[0], self.speed_constraints[1]),
            random.randint(self.lifetime_constraints[0], self.lifetime_constraints[1]))
            self.particles.append(new_particle)

        for particle in self.particles:

            particle.update()