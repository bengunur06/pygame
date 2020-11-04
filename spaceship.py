import pygame 

pygame.init()

win = pygame.display.set_mode((500,500))
screenWidth = 500
screenHeight = 500
pygame.display.set_caption("Game window BNG")



x = 50 
y = 400
width = 64
height = 64
ve = 5 

isJump = False
jumpCount = 10
left = False
right = False
walkCount = 0

spaceShip = [pygame.image.load('ship_F.png'),pygame.image.load('ship_F5.png'),]
backGround = pygame.image.load('bg_1.png')

def reDrawGameWindow ():
    global walkCount

    win.blit(backGround,(0,0))
    win.blit(spaceShip[0],(x,y))
    pygame.display.update()


run = True 
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and  x >ve :
        x -= ve
        left = True
        right = False 
    elif keys[pygame.K_RIGHT] and  x < screenWidth - width  :
        x += ve 
        right = True
        left = False 
    
    else :
        right = False
        left = False
        walkCount = 0
        
    if not (isJump):
       # if keys[pygame.K_UP] and y > ve  :
       #     y -= ve
       # if keys[pygame.K_DOWN] and y < screenHeight - height:
        #    y += ve
        if keys[pygame.K_SPACE] :
            isJump = True
            right=False
            left = False
            walkCount = 0 

    else:
        if jumpCount >= -10 :
            neg = 1 
            if jumpCount < 0 :
                neg = -1
            y -= ( jumpCount ** 2) * 0.5 * neg 
            jumpCount-=1
        else : 
            isJump = False
            jumpCount = 10
    reDrawGameWindow()
 #   win.fill((0,0,0))
 #   pygame.draw.rect(win,(255,0,0),(x,y,width ,height))
 #   pygame.display.update()

pygame.quit()
