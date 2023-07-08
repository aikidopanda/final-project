import pygame

# Colours of buttons and badges
black = (0, 0, 0)
blue = (88, 60, 178)
red = (204, 0, 0)
yellow = (244, 250, 47)
white = (255, 255, 255)
maroon = (128, 0, 0)
player_color = (48, 19, 196)
opponent_color = (192, 42, 19)

clicked = False

screen = pygame.display.set_mode((1600, 900), pygame.SCALED)


def text_objects(text, font):
    textSurface = font.render(text, True, maroon)
    return textSurface, textSurface.get_rect()


def text_objects_sm(text, font):
    textSurface = font.render(text, True, yellow)
    return textSurface, textSurface.get_rect()


def button(msg, x, y, width, height, colour, status, action=None, image=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        if status == 'active':
            colour = maroon
        if click[0] == 1 and action != None and clicked == False:
            action()

    if image != None:
        screen.blit(
            pygame.image.load(image), (x, y)
        )
        smallText = pygame.font.Font("freesansbold.ttf", 22)
        textSurf, textRect = text_objects_sm(msg, smallText)
        textRect.center = ((x+(width/2) + 20), (y+(height/2)))
        screen.blit(textSurf, textRect)
    else:
        pygame.draw.rect(screen, colour, (x, y, width, height))
        smallText = pygame.font.Font("freesansbold.ttf", 18)
        textSurf, textRect = text_objects_sm(msg, smallText)
        textRect.center = ((x+(width/2)), (y+(height/2)))
        screen.blit(textSurf, textRect)


def cardborder(x, y, width, height, colour):
    pygame.draw.rect(screen, colour, (x, y, width, height))
