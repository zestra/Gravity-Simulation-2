import pygame

import math
import random

from basics import *

img_dir = "/Users/czeslawtracz/Library/Mobile Documents/com~apple~CloudDocs/School Demonstration/Gravity Simulation/images/"

colours = []
for i in range(1, 7):
    colours.append(f"ball{i}.png")

BLACK = (0, 0, 0)
BLUE = (0, 155, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (128, 0, 0)

DARK_BLUE = (0, 100, 200)
BRIGHT_BLUE = (100, 255, 355)
PALE_BLUE = (0, 35, 135)

DARK_GREY = (50, 50, 50)
DARKER_GREY = (10, 10, 10)

pygame.init()
WIDTH, HEIGHT = 1200, 640
TILE_SIZE = 5
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulation, by Czeslaw H.Z.T")

clock = pygame.time.Clock()

class Ball:
    def __init__(self, pos_x_i, pos_y_i, agl_i, vel_i):

        ### Mechanics

        # initial and final positions, split into x and y components
        self.pos_x, self.pos_y = self.pos_x_i, self.pos_y_i = pos_x_i, pos_y_i
        
        # initial and final velocities and angles
        self.vel, self.agl = self.vel_i, self.agl_i = vel_i, agl_i

        # initial and final velocities, split into x and y components
        self.vel_x, self.vel_y = self.vel_x_i, self.vel_y_i = self.vel_i * math.cos(math.radians(self.agl_i)), \
                                                              self.vel_i * math.sin(math.radians(self.agl_i))

        # acceleration, split into x and y components
        self.acl_y, self.acl_x = -10, 0

        ### Effects

        # filename of ball image
        self.image_filename = random.choice(colours)
        # trail effect list
        self.trail = [(pos_x_i, pos_y_i)]
        # time information
        self.clock = pygame.time.Clock()

        self.prev_t = 0
        self.t = 0

        ### Controls
        
        # remove ball from world?
        self.destroy = False
        # freeze ball on the spot? 
        self.freeze = False
        # show ball's trail?
        self.show_path = True
        # show ball's status?
        self.show_status = True


    def update(self):

        if self.freeze:
            return

        time_passed_milliseconds = self.clock.tick()
        time_passed_seconds = time_passed_milliseconds / 1000.0
        self.t += time_passed_seconds
        
        # Uniform Acceleration Equations (UAE 🇦🇪)
        self.pos_x = self.pos_x_i + self.vel_x_i*self.t + (1/2)*self.acl_x*(self.t**2)
        self.pos_y = self.pos_y_i + self.vel_y_i*self.t + (1/2)*self.acl_y*(self.t**2)
        
        self.vel_x = self.vel_x_i + self.acl_x*self.t
        self.vel_y = self.vel_y_i + self.acl_y*self.t

        # Pythagorean Theorem
        self.vel = math.sqrt((self.vel_x**2) + (self.vel_y**2))

        # Trigonometry
        self.agl = math.degrees(math.atan(self.vel_y/self.vel_x))

        # Simulate Bouncing
        # if self.pos_y < impact_ground_y:
        #     self.vel_y = self.vel_y_i = -self.vel_y
        #     self.pos_y = self.pos_y_i = impact_ground_y + 10

        # Create Trail
        if int(self.t) != int(self.prev_t):
            self.add_trail()

        self.prev_t = self.t
    
    def unfreeze_time(self):
        self.clock = pygame.time.Clock()

    def add_trail(self):
        self.trail.append((self.pos_x, self.pos_y))

    def render(self):
        draw_image(window, self.image_filename, self.pos_x*TILE_SIZE, HEIGHT - self.pos_y*TILE_SIZE, img_dir, True)
        
        if self.show_path:
            for pos in self.trail:
                pos_x, pos_y = pos
                draw_image(window, "ball0.png", pos_x*TILE_SIZE, HEIGHT - pos_y*TILE_SIZE, img_dir, True)

class Cannon:
    def __init__(self):
        pass
    
    def update(self):
        pass
    
    def render(self):
        pass

class World:
    def __init__(self):
        self.balls = []
        self.selected_ball = None
        self.cannon = None
    
    def render_selected_ball_information(self):
        
        if self.selected_ball is None or self.selected_ball.show_status is False:
            # draw box around information
            draw_rect(window, WIDTH - 150, 65, 260, 90, "orange", True)

            # show title
            draw_text(window, "Information", WIDTH - 150, 40, 40, "white", "DinCondensed")
            draw_text(window, "on selected ball", WIDTH - 150, 75, 20, "white", "DinCondensed")

            return
            
        # draw box around information
        draw_rect(window, WIDTH - 150, 240, 260, 440, "orange", True)

        # show title
        draw_text(window, "Information", WIDTH - 150, 40, 40, "white", "DinCondensed")
        draw_text(window, "on selected ball", WIDTH - 150, 75, 20, "white", "DinCondensed")

        # give mechanics information
        draw_text(window, f"Position, along x-axis: {round(self.selected_ball.pos_x, 1)} m", WIDTH - 150, 100, 15, "white", "Arial")
        draw_text(window, f"Position, along y-axis: {round(self.selected_ball.pos_y, 1)} m", WIDTH - 150, 120, 15, "white", "Arial")
        draw_text(window, f"Velocity, along x-axis: {round(self.selected_ball.vel_x, 1)} m/s", WIDTH - 150, 140, 15, "white", "Arial")
        draw_text(window, f"Velocity, along y-axis: {round(self.selected_ball.vel_y, 1)} m/s", WIDTH - 150, 160, 15, "white", "Arial")
        draw_text(window, f"Acceleration, along x-axis: {round(self.selected_ball.acl_x, 1)} m/s/s", WIDTH - 150, 180, 15, "white", "Arial")
        draw_text(window, f"Acceleration, along y-axis: {round(self.selected_ball.acl_y, 1)} m/s/s", WIDTH - 150, 200, 15, "white", "Arial")
        draw_text(window, f"Angle, North of East: {round(self.selected_ball.agl, 1)}˚", WIDTH - 150, 220, 15, "white", "Arial")
        draw_text(window, f"Time: {round(self.selected_ball.t, 1)} s", WIDTH - 150, 240, 15, "white", "Arial")

        # draw velocity-angle-indicator, very fancy
        pygame.draw.line(window, "white", (WIDTH - 150, 350), 
                        (WIDTH - 150 + 60*math.sin(math.radians(self.selected_ball.agl + 90)), 
                        350 + 60*math.cos(math.radians(self.selected_ball.agl + 90))), 2)
        agl_surface = text_to_surface(str(round(self.selected_ball.agl, 1)) + "˚", 15, "white", "Arial")
        agl_surface = rotate_surface(agl_surface, self.selected_ball.agl)
        draw_surface(window, agl_surface,
                    (WIDTH - 150 + 30*math.sin(math.radians(self.selected_ball.agl + 110))),
                    (350 + 30*math.cos(math.radians(self.selected_ball.agl + 110))))
        arrow_head_surface = image_to_surface("arrow_head.png", img_dir, True)
        arrow_head_surface = rotate_surface(arrow_head_surface, self.selected_ball.agl)
        draw_surface(window, arrow_head_surface, WIDTH - 150 + 60*math.sin(math.radians(self.selected_ball.agl + 90)), 
                        350 + 60*math.cos(math.radians(self.selected_ball.agl + 90)))

        draw_text(window, "N", WIDTH - 150, 268, 15, "white", "Arial")
        pygame.draw.line(window, "white", (WIDTH - 150, 290), (WIDTH - 150, 415))
        draw_text(window, "S", WIDTH - 150, 418, 15, "white", "Arial")
        draw_text(window, "E", WIDTH - 75, 343, 15, "white", "Arial")
        pygame.draw.line(window, "white", (WIDTH - 88, 350), (WIDTH - 210, 350))
        draw_text(window, "W", WIDTH - 225, 343, 15, "white", "Arial")


    def controls(self):
        keys_down = pygame.key.get_pressed()

        if keys_down[K_1] and self.selected_ball is not None:
            if self.selected_ball.freeze:
                self.selected_ball.freeze = False
                self.selected_ball.unfreeze_time()
            else:
                self.selected_ball.freeze = True
            pygame.time.delay(int(100*2))
        
        if keys_down[K_2] and self.selected_ball is not None:
            if self.selected_ball.show_path:
                self.selected_ball.show_path = False
            else:
                self.selected_ball.show_path = True
            pygame.time.delay(int(100*2))

        if keys_down[K_3] and self.selected_ball is not None:
            if self.selected_ball.show_status:
                self.selected_ball.show_status = False
            else:
                self.selected_ball.show_status = True
            pygame.time.delay(int(100*2))

        if keys_down[K_4] and self.selected_ball is not None:
            self.delete(self.selected_ball)
            self.selected_ball = None
            pygame.time.delay(int(100*2))

        if keys_down[K_SPACE]:
            self.balls.append(Ball(20, 20, random.randint(10, 30), random.randint(40, 90)))
            pygame.time.delay(int(100*2))

        if keys_down[K_RIGHT] or keys_down[K_LEFT]:
            index = 0
            for ball in self.balls:
                if ball == self.selected_ball:
                    break
                index += 1
            
            if keys_down[K_RIGHT]:
                if index + 1 <= len(self.balls) - 1:
                    self.selected_ball = self.balls[index + 1]
                else:
                    self.selected_ball = self.balls[0]
            else:
                if index - 1 >= 0:
                    self.selected_ball = self.balls[index - 1]
                else:
                    self.selected_ball = self.balls[len(self.balls) - 1]

            pygame.time.delay(int(100*2))
            

    def update(self):
        self.controls()
        for ball in self.balls:
            ball.update()
        self.cannon.update()
    
    def render(self):
        for ball in self.balls:
            ball.render()
            if ball == self.selected_ball:
                draw_rect(window, ball.pos_x*TILE_SIZE, HEIGHT - ball.pos_y*TILE_SIZE, 20, 20, "orange", False)

                pygame.draw.line(window, "orange", (self.selected_ball.pos_x*TILE_SIZE, HEIGHT - self.selected_ball.pos_y*TILE_SIZE), 
                        (self.selected_ball.pos_x*TILE_SIZE + 60*math.sin(math.radians(self.selected_ball.agl + 90)), 
                        HEIGHT - self.selected_ball.pos_y*TILE_SIZE + 60*math.cos(math.radians(self.selected_ball.agl + 90))), 2)

                vel_surface = text_to_surface(str(round(self.selected_ball.vel, 1)) + " m/s", 15, "orange", "Arial")
                vel_surface = rotate_surface(vel_surface, self.selected_ball.agl)

                draw_surface(window, vel_surface,
                            (self.selected_ball.pos_x*TILE_SIZE + 30*math.sin(math.radians(self.selected_ball.agl + 110))),
                            (HEIGHT - self.selected_ball.pos_y*TILE_SIZE + 30*math.cos(math.radians(self.selected_ball.agl + 110))))

                arrow_head_surface = image_to_surface("arrow_head2.png", img_dir, True)
                arrow_head_surface = rotate_surface(arrow_head_surface, self.selected_ball.agl)
                
                draw_surface(window, arrow_head_surface, self.selected_ball.pos_x*TILE_SIZE + 60*math.sin(math.radians(self.selected_ball.agl + 90)), 
                                HEIGHT - self.selected_ball.pos_y*TILE_SIZE + 60*math.cos(math.radians(self.selected_ball.agl + 90)))

        self.cannon.render()
        self.render_selected_ball_information()
    
    def append(self, ball):
        self.balls.append(ball)

    def delete(self, ball):
        index = 0
        for ball_i in self.balls:
            if ball_i == ball:
                del self.balls[index]
                return
            index += 1

world = World()
world.append(Ball(20, 20, 75, 40))
world.selected_ball = world.balls[0]
world.cannon = Cannon()

time = 0  # measured in seconds

impact_ground_y = 20

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()

    window.fill("white")

    world.update()
    world.render()

    pygame.display.update()
