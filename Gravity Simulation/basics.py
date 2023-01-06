import pygame
from pygame.locals import *

import math


def draw_surface(my_screen,
               my_surface,
               x, y):

    """This function draws the given surface onto the screen."""

    x = x - (my_surface.get_width()/2)
    y = y - (my_surface.get_height()/2)

    my_screen.blit(my_surface, (x, y))


def draw_image(my_screen, filename, x, y, img_dir, transparent=False):

    """This function draws the given image onto the screen."""

    if transparent is False:
        image = pygame.image.load(img_dir + filename).convert()
    else:
        image = pygame.image.load(img_dir + filename).convert_alpha()

    image_x = x - image.get_width()/2
    image_y = y - image.get_height()/2

    my_screen.blit(image, (image_x, image_y))


def draw_text(my_screen, text, x, y, my_size=25, my_color="white", my_font="Arial"):

    """This function draws text, with the given characteristics, onto the screen."""

    my_font = pygame.font.SysFont(my_font, my_size, False, False)
    text_surface = my_font.render(text, True, my_color)

    text_x = x - text_surface.get_width()/2

    my_screen.blit(text_surface, (text_x, y))


def text_to_image(text, img_dir, my_size=25, my_color="white", my_font="Arial"):

    """This function converts a text, with the given properties, into an image, which can
    be found in the given image directory."""

    font = pygame.font.SysFont(my_font, my_size)
    surface = font.render(text, True, my_color)
    pygame.image.save(surface, img_dir + text + ".png")

def text_to_surface(text, my_size=25, my_color="white", my_font="Arial"):

    """This function converts a text, with the given properties, into a surface."""

    font = pygame.font.SysFont(my_font, my_size)
    surface = font.render(text, True, my_color)
    return surface


def draw_rect(my_screen, x, y, width, height, color="white", filled_in=True):

    """This function draws a rectangle, with the given parameters, onto the screen."""

    if filled_in:
        filled_in = 0
    else:
        filled_in = 1

    pygame.draw.rect(my_screen, color, Rect((x - (width/2), y - (height/2)), (width, height)), filled_in)


def scale_surface(my_surface, dilated_x, dilated_y):

    """This function scales a given surface, by replacing its
     width and height parameters with the new ones given."""

    scaled_surface = pygame.transform.scale(my_surface, (dilated_x, dilated_y))
    return scaled_surface


def rotate_surface(my_surface, angle):

    """This function rotates a given surface by the given angle, in degrees."""

    rotated_surface = pygame.transform.rotate(my_surface, angle)
    return rotated_surface


def image_to_surface(filename, img_dir,
                     translucent=False):

    """This function converts an image into a surface."""

    if translucent is True:
        image_surface = pygame.image.load(img_dir + filename).convert_alpha()
    else:
        image_surface = pygame.image.load(img_dir + filename).convert()
    return image_surface


def keys_dic(dic):
    key_dic = {}
    index = 0
    for key in dic:
        key_dic[index] = key
        index += 1
    return key_dic


def reverse_dic(dic):
    reversed_dic = {}

    index = 0

    for value in dic.values():
        reversed_dic[value] = index
        index += 1
    return reversed_dic