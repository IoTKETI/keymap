# http://www.codingwithruss.com/pygame/how-to-use-joysticks-in-pygame/
import pygame

pygame.init()

#initialise the joystick module
pygame.joystick.init()

#define screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Joysticks")

#define font
font_size = 30
font = pygame.font.SysFont("Futura", font_size)

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#create clock for setting game frame rate
clock = pygame.time.Clock()
FPS = 60

#create empty list to store joysticks
joysticks = []

#create player rectangle
x = 350
y = 200
player = pygame.Rect(x, y, 100, 100)

#define player colour
col = "royalblue"

#game loop
run = True
while run:

  clock.tick(FPS)

  #update background
  screen.fill(pygame.Color("midnightblue"))

  #draw player
  player.topleft = (x, y)
  pygame.draw.rect(screen, pygame.Color(col), player)

  #show number of connected joysticks
  draw_text("Controllers: " + str(pygame.joystick.get_count()), font, pygame.Color("azure"), 10, 10)
  for joystick in joysticks:
    draw_text("Battery Level: " + str(joystick.get_power_level()), font, pygame.Color("azure"), 10, 35)
    draw_text("Controller Type: " + str(joystick.get_name()), font, pygame.Color("azure"), 10, 60)
    draw_text("Number of axes: " + str(joystick.get_numaxes()), font, pygame.Color("azure"), 10, 85)

  for joystick in joysticks:
    # #change player colour with buttons
    if joystick.get_button(0):
      col = "royalblue"
    if joystick.get_button(1):
      col = "crimson"
    if joystick.get_button(2):
      col = "fuchsia"
    if joystick.get_button(3):
      col = "forestgreen"


    #player movement with analogue sticks
    horiz_move1 = joystick.get_axis(0)
    vert_move1 = joystick.get_axis(1)
    if abs(vert_move1) > 0.05:
      y += vert_move1 * 5
    if abs(horiz_move1) > 0.05:
      x += horiz_move1 * 5

    horiz_move2 = joystick.get_axis(2)
    vert_move2 = joystick.get_axis(3)
    if abs(vert_move2) > 0.05:
      y += vert_move2 * 5
    if abs(horiz_move2) > 0.05:
      x += horiz_move2 * 5

    #player movement with hat button
    hatVar = joystick.get_hat(0)
    if hatVar == (-1,0):
      x -= 3
    elif hatVar == (1,0):
      x += 3
    elif hatVar == (0,1):
      y -= 3
    elif hatVar == (0,-1):
      y += 3

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.JOYDEVICEADDED:
      joy = pygame.joystick.Joystick(event.device_index)
      joysticks.append(joy)
    #quit program
    if event.type == pygame.QUIT:
      run = False

  #update display
  pygame.display.flip()

pygame.quit()