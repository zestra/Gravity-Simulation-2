# A Gravity Simulation, 
# began on Jan 3, 2023, ended on Jan ..., 2023,
# by Czeslaw Herbert Zestra Tracz (H.Z.T),
# for one's self-satisfaction and Al Bateen Academy, Aldar Academies

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
        self.show_path = False
        # show ball's information?
        self.show_info = True

        self.border, self.box_width = 0, 0

    def controls(self):
        keys_down = pygame.key.get_pressed()

        if keys_down[K_7]:
            if self.freeze:
                self.freeze = False
                self.unfreeze_time()
            else:
                self.freeze = True
            pygame.time.delay(int(100*2))
        
        if keys_down[K_8]:
            if self.show_path:
                self.show_path = False
            else:
                self.show_path = True
            pygame.time.delay(int(100*2))

        if keys_down[K_9]:
            world.delete(self)
            world.selected_ball = None
            pygame.time.delay(int(100*2))


    def update(self):
        # If frozen, do not update
        if self.freeze:
            return

        # Simulate time passed
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

        # Create Trail
        if int(self.t) != int(self.prev_t):
            self.add_trail()

        self.prev_t = self.t

        # Check if Ball Out of Screen.
        # If so, delete Ball from World.
        if self.pos_y*TILE_SIZE < 0:
            self.destroy = True
        if self.pos_y*TILE_SIZE > HEIGHT:
            self.destroy = True
        elif self.pos_x*TILE_SIZE > WIDTH:
            self.destroy = True
        if self.destroy:
            world.delete(self)
            if world.selected_ball == self:
                world.selected_ball = None

    def unfreeze_time(self):
        self.clock = pygame.time.Clock()

    def add_trail(self):
        self.trail.append((self.pos_x, self.pos_y))
    
    def render_information(self):

        box_number = 4
        box_center = self.border*box_number + self.box_width/2 + self.box_width*(box_number - 1)
            
        # draw box around information
        draw_rect(window, box_center, 320, self.box_width, 600, "orange", True)

        # show title
        draw_text(window, "Information", box_center, 40, 40, "white", "DinCondensed")
        draw_text(window, "on selected ball", box_center, 75, 20, "white", "DinCondensed")

        # give mechanics information
        draw_text(window, f"Position, along x-axis: {round(self.pos_x - self.pos_x_i, 1)} m", box_center, 100, 15, "white", "Arial")
        draw_text(window, f"Position, along y-axis: {round(self.pos_y - self.pos_y_i, 1)} m", box_center, 120, 15, "white", "Arial")
        draw_text(window, f"Velocity, along x-axis: {round(self.vel_x, 1)} m/s", box_center, 140, 15, "white", "Arial")
        draw_text(window, f"Velocity, along y-axis: {round(self.vel_y, 1)} m/s", box_center, 160, 15, "white", "Arial")
        draw_text(window, f"Acceleration, along x-axis: {round(self.acl_x, 1)} m/s/s", box_center, 180, 15, "white", "Arial")
        draw_text(window, f"Acceleration, along y-axis: {round(self.acl_y, 1)} m/s/s", box_center, 200, 15, "white", "Arial")
        draw_text(window, f"Angle, North of East: {round(self.agl, 1)}˚", box_center, 220, 15, "white", "Arial")
        draw_text(window, f"Time: {round(self.t, 1)} s", box_center, 240, 15, "white", "Arial")

        # draw angle-indicator, very fancy
        arrow_length = 70*(self.vel/self.vel_i)

        pygame.draw.line(window, "white", (box_center, 350), 
                        (box_center + arrow_length*math.sin(math.radians(self.agl + 90)), 
                        350 + arrow_length*math.cos(math.radians(self.agl + 90))), 2)
        agl_surface = text_to_surface(str(round(self.agl, 1)) + "˚", 15, "white", "Arial")
        agl_surface = rotate_surface(agl_surface, self.agl)
        draw_surface(window, agl_surface,
                    (box_center + (arrow_length/2)*math.sin(math.radians(self.agl + 110))),
                    (350 + (arrow_length/2)*math.cos(math.radians(self.agl + 110))))
        arrow_head_surface = image_to_surface("arrow_head.png", img_dir, True)
        arrow_head_surface = rotate_surface(arrow_head_surface, self.agl)
        draw_surface(window, arrow_head_surface, box_center + arrow_length*math.sin(math.radians(self.agl + 90)), 
                        350 + arrow_length*math.cos(math.radians(self.agl + 90)))

        # draw compass-graph
        draw_text(window, "N", box_center, 268, 15, "white", "Arial")
        pygame.draw.line(window, "white", (box_center, 290), (box_center, 415))
        draw_text(window, "S", box_center, 418, 15, "white", "Arial")
        draw_text(window, "E", WIDTH - 80, 343, 15, "white", "Arial")
        pygame.draw.line(window, "white", (WIDTH - 93, 350), (WIDTH - 215, 350))
        draw_text(window, "W", WIDTH - 230, 343, 15, "white", "Arial")

        pygame.draw.line(window, "white", (box_center - 130 + 20, 445), (box_center + 130 - 20, 445), 1)

        # give initial mechanics information
        draw_text(window, f"Inital Angle: {self.agl_i}", box_center, 455, 15, "white", "Arial")
        draw_text(window, f"Inital Velocity: {self.vel_i}", box_center, 475, 15, "white", "Arial")

        pygame.draw.line(window, "white", (box_center - 130 + 20, 500), (box_center + 130 - 20, 500), 1)

        # give controls information
        draw_text(window, "Press \"7\" key to Freeze on Spot", box_center, 510, 15, "white", "Arial")
        draw_text(window, "Press \"8\" key to Show/Hide Path", box_center, 530, 15, "white", "Arial")
        draw_text(window, "Press \"9\" key to Delete Ball", box_center, 550, 15, "white", "Arial")
        draw_text(window, "Press \"LEFT\" and \"RIGHT\" buttons", box_center, 570, 15, "white", "Arial")
        draw_text(window, "to Select a Another Ball", box_center, 590, 15, "white", "Arial")

        # draw velocity-arrow for selected ball, also very fancy
        pygame.draw.line(window, "orange", (self.pos_x*TILE_SIZE, HEIGHT - self.pos_y*TILE_SIZE), 
        (self.pos_x*TILE_SIZE + arrow_length*math.sin(math.radians(self.agl + 90)), 
        HEIGHT - self.pos_y*TILE_SIZE + arrow_length*math.cos(math.radians(self.agl + 90))), 2)

        vel_surface = text_to_surface(str(round(self.vel, 1)) + " m/s", 15, "orange", "Arial")
        vel_surface = rotate_surface(vel_surface, self.agl)

        draw_surface(window, vel_surface,
                    (self.pos_x*TILE_SIZE + (arrow_length/2)*math.sin(math.radians(self.agl + 110))),
                    (HEIGHT - self.pos_y*TILE_SIZE + (arrow_length/2)*math.cos(math.radians(self.agl + 110))))

        arrow_head_surface = image_to_surface("arrow_head2.png", img_dir, True)
        arrow_head_surface = rotate_surface(arrow_head_surface, self.agl)
        
        draw_surface(window, arrow_head_surface, self.pos_x*TILE_SIZE + arrow_length*math.sin(math.radians(self.agl + 90)), 
                        HEIGHT - self.pos_y*TILE_SIZE + arrow_length*math.cos(math.radians(self.agl + 90)))


    def render(self):
        draw_image(window, self.image_filename, self.pos_x*TILE_SIZE, HEIGHT - self.pos_y*TILE_SIZE, img_dir, True)
        
        if self.show_path:
            for pos in self.trail:
                pos_x, pos_y = pos
                draw_image(window, "ball0.png", pos_x*TILE_SIZE, HEIGHT - pos_y*TILE_SIZE, img_dir, True)

class Cannon:
    def __init__(self):
        self.body_surface = image_to_surface("body.png", img_dir, True)
        self.head_surface = image_to_surface("head.png", img_dir, True)
        
        self.fire_angle = 0  # in degrees
        self.fire_velocity = 40
        
        self.show_info = True
        self.border, self.box_width = 0, 0

    def controls(self):
        keys_down = pygame.key.get_pressed()

        if keys_down[K_UP] and self.fire_angle < 90:
            self.fire_angle += 1
            pygame.time.delay(int(100*0.2))
        elif keys_down[K_DOWN] and self.fire_angle > 0:
            self.fire_angle -= 1
            pygame.time.delay(int(100*0.2))
        
        if keys_down[K_5]:
            self.fire_velocity += 1
            pygame.time.delay(int(100*0.9))
        elif keys_down[K_6] and self.fire_velocity > 0:
            self.fire_velocity -= 1
            pygame.time.delay(int(100*0.9))

        if keys_down[K_SPACE]:
            if world.selected_ball is not None:
                world.selected_ball.show_path = False
            world.balls.append(Ball(23 + (self.head_surface.get_size()[0]/2 - 80)*math.cos(math.radians(self.fire_angle)), 15 + (self.head_surface.get_size()[0]/2 - 80)*math.sin(math.radians(self.fire_angle)), self.fire_angle, self.fire_velocity))
            world.selected_ball = world.balls[len(world.balls) - 1]
            world.selected_ball.border, world.selected_ball.box_width = world.border, world.box_width
            pygame.time.delay(int(100*2))
    
    def update(self):
        self.controls()
    
    def render_information(self):
        
        box_number = 3
        box_center = self.border*box_number + self.box_width/2 + self.box_width*(box_number - 1)

        # draw box around information
        draw_rect(window, box_center, 155, self.box_width, 270, "orange", True)

        # show title
        draw_text(window, "Information", box_center, 40, 40, "white", "DinCondensed")
        draw_text(window, "on cannon", box_center, 75, 20, "white", "DinCondensed")

        # give mechanics information
        draw_text(window, f"Fire Angle, North of East: {self.fire_angle}˚", box_center, 100, 15, "white", "Arial")
        draw_text(window, f"Fire Velocity: {self.fire_velocity} m/s", box_center, 120, 15, "white", "Arial")

        # draw line separation
        pygame.draw.line(window, "white", (box_center - 130 + 20, 150), (box_center + 130 - 20, 150), 1)

        # give controls information
        draw_text(window, "Press \"Up\" and \"Down\" buttons", box_center, 160, 15, "white", "Arial")
        draw_text(window, "to adjust Fire Angle", box_center, 180, 15, "white", "Arial")
        draw_text(window, "Press \"5\" and \"6\" buttons", box_center, 210, 15, "white", "Arial")
        draw_text(window, "to adjust Fire Velocity", box_center, 230, 15, "white", "Arial")
        draw_text(window, "Press \"SPACE\" button to Fire", box_center, 260, 15, "white", "Arial")
        
    
    def render(self):
        head_surface = rotate_surface(self.head_surface, self.fire_angle)
        draw_surface(window, head_surface, 40 + self.body_surface.get_size()[0]/2, HEIGHT - 40 - self.body_surface.get_size()[1]/2)
        draw_surface(window, self.body_surface, 20 + self.body_surface.get_size()[0]/2, HEIGHT - 20 - self.body_surface.get_size()[1]/2)


class World:
    def __init__(self):
        self.balls = []
        self.selected_ball = None
        self.cannon = Cannon()

        self.show_quadratic_info = False
        self.show_guide_info = True

        self.border = 20
        self.box_width = 275
    
    def update(self):
        for ball in self.balls:
            if ball == self.selected_ball:
                ball.controls()
            ball.update()
        self.sort_balls()
        if self.cannon.show_info:
            self.cannon.update()
        self.controls()

    def controls(self):
        keys_down = pygame.key.get_pressed()

        if keys_down[K_1]:
            if self.show_guide_info:
                self.show_guide_info = False
            else:
                self.show_guide_info = True
            pygame.time.delay(int(100*2))
        
        if keys_down[K_2]:
            if self.show_quadratic_info:
                self.show_quadratic_info = False
            else:
                self.show_quadratic_info = True
            pygame.time.delay(int(100*2))
        
        if keys_down[K_3]:
            if self.cannon.show_info:
                self.cannon.show_info = False
            else:
                self.cannon.show_info = True
            pygame.time.delay(int(100*2))
        
        if keys_down[K_4]:
            for ball in self.balls:
                if ball.show_info:
                    ball.show_info = False
                else:
                    ball.show_info = True
            pygame.time.delay(int(100*2))

        if (keys_down[K_RIGHT] or keys_down[K_LEFT]) and len(self.balls) > 0:
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

    def render_quadratic_information(self):

        box_number = 2
        box_center = self.border*box_number + self.box_width/2 + self.box_width*(box_number - 1)

        # draw box
        draw_rect(window, box_center, 65, self.box_width, 90, "orange", True)

        # show title
        draw_text(window, "Information", box_center, 40, 40, "white", "DinCondensed")
        draw_text(window, "on quadratic trajectory", box_center, 75, 20, "white", "DinCondensed")
        

        if self.show_quadratic_info is False:
            return

        draw_rect(window, box_center, 155, self.box_width, 90, "orange", True)

    
    def render_guide_information(self):

        box_number = 1
        box_center = self.border*box_number + self.box_width/2 + self.box_width*(box_number - 1)

        # draw box
        draw_rect(window, box_center, 65, self.box_width, 90, "orange", True)

        # show title
        draw_text(window, "GUIDE", box_center, 40, 40, "white", "DinCondensed")
        draw_text(window, "Click the \"1\" button to Hide/Reveal", box_center, 75, 20, "white", "DinCondensed")
        

        if self.show_guide_info is False:
            return
        
        draw_rect(window, box_center, 180, self.box_width, 150, "orange", True)
        
        draw_text(window, "Press the \"2\" button", box_center, 100, 15, "white", "Arial")
        draw_text(window, "to Hide/Reveal Quadratic Info", box_center, 120, 15, "white", "Arial")

        draw_text(window, "Press the \"3\" button", box_center, 150, 15, "white", "Arial")
        draw_text(window, "to Hide/Reveal Cannon Info", box_center, 170, 15, "white", "Arial")
        
        draw_text(window, "Press the \"4\" button", box_center, 200, 15, "white", "Arial")
        draw_text(window, "to Hide/Reveal Selected Ball Info", box_center, 220, 15, "white", "Arial")
    
    def render_selected_ball_information(self):
        box_number = 4
        box_center = self.border*box_number + self.box_width/2 + self.box_width*(box_number - 1)

        # draw box
        draw_rect(window, box_center, 65, self.box_width, 90, "orange", True)

        # show title
        draw_text(window, "Information", box_center, 40, 40, "white", "DinCondensed")
        draw_text(window, "on selected ball", box_center, 75, 20, "white", "DinCondensed")
        
        if self.selected_ball is None:
            return
        elif self.selected_ball.show_info is False:
            return
        
        self.selected_ball.render_information()
    
    def render_cannon_information(self):
        box_number = 3
        box_center = self.border*box_number + self.box_width/2 + self.box_width*(box_number - 1)

        # draw box
        draw_rect(window, box_center, 65, self.box_width, 90, "orange", True)

        # show title
        draw_text(window, "Information", box_center, 40, 40, "white", "DinCondensed")
        draw_text(window, "on cannon", box_center, 75, 20, "white", "DinCondensed")

        if self.cannon.show_info is False:
            return
    
        self.cannon.render_information()

    def render(self):
        for ball in self.balls:
            ball.render()
            if ball == self.selected_ball:
                draw_rect(window, ball.pos_x*TILE_SIZE, HEIGHT - ball.pos_y*TILE_SIZE, 20, 20, "orange", False)
        self.render_selected_ball_information()

        self.cannon.render()
        self.render_cannon_information()

        self.render_quadratic_information()
        self.render_guide_information()

    def append(self, ball):
        self.balls.append(ball)

    def delete(self, ball):
        index = 0
        for ball_i in self.balls:
            if ball_i == ball:
                del self.balls[index]
                return
            index += 1
    
    def sort_balls(self):
        balls = []
        while len(self.balls) != 0:
            minimum_x = self.balls[len(self.balls) - 1]
            for ball in self.balls:
                if ball.pos_x <= minimum_x.pos_x:
                    minimum_x = ball
            self.delete(minimum_x)
            balls.append(minimum_x)
        self.balls = balls

world = World()
world.cannon = Cannon()
world.cannon.border, world.cannon.box_width = world.border, world.box_width

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

