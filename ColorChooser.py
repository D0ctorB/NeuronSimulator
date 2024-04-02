import pygame
import sys
import pygame_gui

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
font = pygame.font.Font(None, 24)  # You can change the font and size here
text_surface = font.render("Picked color:", True, (255, 255, 255))  # White color

clock = pygame.time.Clock()

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
    SCREEN.blit(text_surface, (background.get_width() - square_size - padding_x - text_surface.get_width(),
                               padding_y))

    ui_manager.draw_ui(SCREEN)

    pygame.display.update()