import pygame
import sys
import pygame_gui
import numpy as np
import requests
from io import BytesIO

from pygame_gui.elements import UIButton
from pygame_gui.windows import UIColourPickerDialog


pygame.init()

pygame.display.set_caption('Neuron Simulator')
SCREEN = pygame.display.set_mode((800, 600))

ui_manager = pygame_gui.UIManager((800, 600))
background = pygame.Surface((800, 600))
background.fill("#3a3b3c")
colour_picker_button = UIButton(relative_rect=pygame.Rect(-180, -60, 150, 30),
                                text='Pick Colour',
                                manager=ui_manager,
                                anchors={'left': 'right',
                                        'right': 'right',
                                        'top': 'bottom',
                                        'bottom': 'bottom'})
colour_picker = None                                    
current_colour = pygame.Color(0, 0, 0)

padding_x = 20
padding_y = 20

#Set up picked_colour_surface
square_size = min(background.get_width(), background.get_height()) // 5
picked_colour_surface = pygame.Surface((square_size, square_size))
picked_colour_surface.fill(current_colour)

# Font setup
font = pygame.font.Font(None, 34)  # You can change the font and size here
text_surface = font.render("Picked color:", True, (255, 255, 255))  # White color

# Add circles and lines
circle_radius = 50
triangle_side = 300
circle_y = background.get_height() // 2

# Calculate circle positions for the triangle
circle_positions = [
    (background.get_width() // 2, circle_y - triangle_side // 2),  # Top
    (background.get_width() // 2 - triangle_side // 2, circle_y + triangle_side // 2),  # Bottom left
    (background.get_width() // 2 + triangle_side // 2, circle_y + triangle_side // 2)  # Bottom right
]

# Colors for the circles
circle_colors = [(90, 0, 0), (0, 90, 0), (0, 0, 90)]

# Load brain image from a local file
brain_image_path = "Human_brain.png"
brain_image = pygame.image.load(brain_image_path)

#increase brain size
scaled_width = int(brain_image.get_width() * 1.2)
scaled_height = int(brain_image.get_height() * 1.2)
brain_image = pygame.transform.scale(brain_image, (scaled_width, scaled_height))

# Set transparency of the brain image
brain_image.set_alpha(80)  # Adjust the alpha value (0-255) for desired transparency

clock = pygame.time.Clock()

generate_red_pois = False
generate_green_pois = False
generate_blue_pois = False

while True:
    time_delta = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == colour_picker_button:
            colour_picker = UIColourPickerDialog(pygame.Rect(160, 50, 420, 400),
                                                ui_manager,
                                                window_title="Change Colour...",
                                                initial_colour=current_colour)
            colour_picker_button.disable()
        if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
            current_colour = event.colour
            picked_colour_surface.fill(current_colour)

            print(current_colour)
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            colour_picker_button.enable()
            colour_picker = None
        
        ui_manager.process_events(event)
        
    ui_manager.update(time_delta)

    SCREEN.blit(background, (0, 0))
    SCREEN.blit(picked_colour_surface, (background.get_width() - square_size - padding_x,
                                        padding_y))
    
    # Blit the text_surface to the left of the picked_colour_surface
    SCREEN.blit(text_surface, (background.get_width() - square_size - padding_x - text_surface.get_width() - 10,
                               padding_y + 40))
    
    rgb_values = [current_colour.r, current_colour.g, current_colour.b]
    circle_colors = [(90, 0, 0), (0, 90, 0), (0, 0, 90)]

    #generate num of frames to wait
    if (generate_red_pois == False):
        red_frames_wait = np.random.poisson(260 - rgb_values[0])
        generate_red_pois = True
    if (generate_green_pois == False):
        green_frames_wait = np.random.poisson(260 - rgb_values[1])
        generate_green_pois = True
    if (generate_blue_pois == False):
        blue_frames_wait = np.random.poisson(260 - rgb_values[2])
        generate_blue_pois = True
    
   
    #decrement wait frames, change color
    red_frames_wait -= 1
    if (red_frames_wait <= 0 and red_frames_wait >= -5):
        circle_colors[0] = (255, 0, 0)
    elif (red_frames_wait < -1):
        generate_red_pois = False

    green_frames_wait -= 1
    if (green_frames_wait <= 0 and green_frames_wait >= -5):
        circle_colors[1] = (0, 255, 0)
    elif (green_frames_wait < -1):
        generate_green_pois = False
    
    blue_frames_wait -= 1
    if (blue_frames_wait <= 0 and blue_frames_wait >= -5):
        circle_colors[2] = (0, 0, 255)
    elif (blue_frames_wait < -1):
        generate_blue_pois = False
    
    # Draw circles and lines forming a triangle
    for color, position in zip(circle_colors, circle_positions):
        pygame.draw.circle(background, color, position, circle_radius)

    #Blit brain image
    SCREEN.blit(brain_image, (background.get_width() // 2 - scaled_width // 2,
                              circle_y - scaled_height // 2))
    
    # Draw lines connecting the circles to form a triangle
    pygame.draw.line(background, (255, 255, 255), circle_positions[0], circle_positions[1], 2)
    pygame.draw.line(background, (255, 255, 255), circle_positions[1], circle_positions[2], 2)
    pygame.draw.line(background, (255, 255, 255), circle_positions[2], circle_positions[0], 2)



    ui_manager.draw_ui(SCREEN)

    pygame.display.update()