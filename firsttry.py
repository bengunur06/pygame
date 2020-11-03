import pygame 

pygame.init()

win = pygame.display.set_mode((500,500))
screenWidth = 500
screenHeight = 500
pygame.display.set_caption("Game window BNG")

x = 50 
y = 50
width = 40
height = 60
ve = 5 

run = True 
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and  x >ve :
        x -= ve
    if keys[pygame.K_RIGHT] and  x < screenWidth - width  :
        x += ve 
    if keys[pygame.K_UP] and y > ve  :
        y -= ve
    if keys[pygame.K_DOWN] and y < screenHeight - height:
        y += ve
    
    win.fill((0,0,0))
    pygame.draw.rect(win,(255,0,0),(x,y,width ,height))
    pygame.display.update()

pygame.quit()
