import math
import pygame
from Constants import *

class PhysicsObject:
    def __init__(self, x, y, radius, mass, color):
        self.x = x
        self.y = y 
        self.radius = radius
        self.mass = mass
        self.color = color
        self.vx = 0.0           # Velocity x
        self.vy = 0.0           # Velocity y
        self.friction = 0.99    # Velocity dceay factor
        
    def update(self):
        # Aply friction to gradually slow the object down
        self.vx *= self.friction
        self.vy *= self.friction
        
        # Update position based on velocity
        self.x += self.vx / FPS
        self.y += self.vy / FPS
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        
        
class Robot(PhysicsObject):
    def __init__(self, x, y, radius, mass, color):
        super().__init__(x, y, radius, mass, color)
        self.theta = 0.0        # Orientation (in radians)
        self.v_linear = 0.0     # Forward/Backward speed
        self.v_angular = 0.0    # Turning speed
        
        # Robot tuning parameters
        self.max_linear_v = 150.0  # Max forward speed
        self.max_angular_v = 3.0    # Max turning speed
        self.accel = 5.0            # How fast the robot accelerates
        self.turn_rate = 0.05       # How fast the robot changes angle
        
    def update(self):
        # Update orientaton
        self.theta += self.v_angular / FPS
        
        # Convert polar velocity to catesian
        self.vx = self.v_linear * math.cos(self.theta)
        self.vy = self.v_linear * math.sin(self.theta)
        
        super().update()
        
        # Implement simple field bounderies
        if self.x < self.radius or self.x > WIDTH - self.radius:
            self.x = max(self.radius, min(self.x, WIDTH - self.radius))
            self.vx = -self.vx * 0.5  # Simple bounce
        if self.y < self.radius or self.y > HEIGHT - self.radius:
            self.y = max(self.radius, min(self.y, HEIGHT - self.radius))
            self.vy = -self.vy * 0.5  # Simple bounce
            
    def draw(self, surface):
        # Draw the main circle
        super().draw(surface)
        
        # Draw the orientation line (for visualization)
        end_x = int(self.x + self.radius * math.cos(self.theta))
        end_y = int(self.y + self.radius * math.sin(self.theta))
        pygame.draw.line(surface, BLACK, (int(self.x), int(self.y)),  (end_x, end_y), 3)
        
class Ball(PhysicsObject):
    def __init__(self, x, y, radius, mass, color):
        super().__init__(x, y, radius, mass, color)
        self.restitution = 0.9
        
    def update(self):
        # Run the base physics update (friction and position)
        super().update()

        # Wall Collision Check (Specific logic for the Ball)
        
        # Check X-boundaries
        if self.x - self.radius < 0:  # Left wall
            self.x = self.radius
            self.vx = -self.vx * self.restitution
            
        elif self.x + self.radius > WIDTH:  # Right wall
            self.x = WIDTH - self.radius
            self.vx = -self.vx * self.restitution
            
        # Check Y-boundaries
        if self.y - self.radius < 0:  # Top wall
            self.y = self.radius
            self.vy = -self.vy * self.restitution
            
        elif self.y + self.radius > HEIGHT:  # Bottom wall
            self.y = HEIGHT - self.radius
            self.vy = -self.vy * self.restitution