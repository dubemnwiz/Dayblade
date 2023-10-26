import os
import pygame

BASE_IMG_PATH = 'data/images/'

# Loading image (entities)
def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0)) # Making all images transparent
    return img

# Loading multiple tiles at once
def load_images(path):
    images = []

    # Note: 'os.listdir' - Gives all files in passed in path -> dynamic loading of images
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images