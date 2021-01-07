import pygame 
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('img/through_space.ogg')
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()
win = pygame.display.set_mode((800,600))
screenWidth = 800
screenHeight = 600
pygame.display.set_caption("Game window BNG")
att=2
#shoot = False
class player (object):
    def __init__(self,x,y,width,height):
        self.x= x 
        self.y = y 
        self.width = width 
        self.height = height 
        self.ve = 5
        self.isJump = False 
        self.jumpCount = 10 
        self.right = False 
        self.left = False 
        self.walkCount = 0 
        self.hitbox = (self.x , self.y +5 ,65,65 )
        self.gun = (self.x , self.y- 10  )
        self.yesshoot = False 

    def draw(self,win):
        win.blit(spaceShip[0],(self.x,self.y))
        self.hitbox = (self.x , self.y +5 ,65,65 )
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        


        
class shoot (object):
    def __init__(self,x,y):
        self.x = x
        self.y= y 
        self.vel = 10
        self.gun = (self.x  , self.y -self.vel )
        
    
    def shootIT(self):
        self.gun = (self.x  ,self.y -self.vel )
        pygame.draw.circle(win,(0,0,0),self.gun,3)
        pygame.draw.circle(win,(0,0,0),self.gun,4)
        pygame.draw.circle(win,(0,0,0),self.gun,5)
        pygame.draw.circle(win,(0,0,0),self.gun,6)
        pygame.display.update()
    



class asteroid(player):
    def draw(self,win):
        self.y+=2
        win.blit(astreoidPic[random.randrange(1,20)],(self.x ,self.y))
        self.hitbox = (self.x , self.y +5 ,65,65 )
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)

    def hit (self):
        self
    

    
    def updateTicks(self,ticks):
        self.x += float(self.ve) * ticks / 1000

class projectile(object):
    def __init__(self,x,y,width,height):
        self.x= x 
        self.y = y 
        self.width = width 
        self.height = height 
        self.ve = 10



def reDrawGameWindow ():
    
    win.blit(backGround,(0,0))
    ship1.draw(win)
    for planet in planets :
        planet.draw(win)
        
    pygame.display.update()
    
    

# MAin loop
astreoidPic = [
pygame.image.load('img/planet1.png'),pygame.image.load('img/planet2.png'),pygame.image.load('img/planet3.png'),
pygame.image.load('img/planet4.png'),pygame.image.load('img/planet5.png'),pygame.image.load('img/planet6.png'),
pygame.image.load('img/planet7.png'),pygame.image.load('img/planet8.png'),pygame.image.load('img/planet9.png'),
pygame.image.load('img/planet10.png'),pygame.image.load('img/planet11.png'),pygame.image.load('img/planet12.png'),
pygame.image.load('img/planet13.png'),pygame.image.load('img/planet14.png'),pygame.image.load('img/planet15.png'),
pygame.image.load('img/planet16.png'),pygame.image.load('img/planet17.png'),pygame.image.load('img/planet18.png'),
pygame.image.load('img/planet19.png'),pygame.image.load('img/planet20.png'),]
spaceShip = [pygame.image.load('ship_F.png'),pygame.image.load('ship_F5.png'),]
backGround = pygame.image.load('bg_1.png')
ship1 = player(225,500,64,64)
fire = []
planets = []
for i in astreoidPic  :
    planets.append(asteroid(random.randrange(0,screenWidth),random.randrange(-700,2),64,64))
run = True 
while run:
    clock.tick(27)
    
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

   
    keys = pygame.key.get_pressed()
    
    


    if keys[pygame.K_LEFT] and  ship1.x > ship1.ve :
        ship1.x -= ship1.ve
        ship1.left = True
        ship1.right = False 
    elif keys[pygame.K_RIGHT] and  ship1.x < screenWidth - ship1.width  :
        ship1.x += ship1.ve 
        ship1.right = True
        ship1.left = False 
    
    else :
        ship1.right = False
        ship1.left = False
        ship1.walkCount = 0
        
    if not (ship1.isJump):
       # if keys[pygame.K_UP] and y > ve  :
       #     y -= ve
       # if keys[pygame.K_DOWN] and y < screenHeight - height:
        #    y += ve
        if keys[pygame.K_SPACE] :
            ship1.yesshoot = True
            fire.append(shoot(ship1.x+30,ship1.y))

        for i in fire :
            i.vel+=30
            i.shootIT()

    
            
            #fire = []
        else :
            ship1.yesshoot = False     

    else:
        if ship1.jumpCount >= -10 :
            neg = 1 
            if ship1.jumpCount < 0 :
                neg = -1
            ship1.y -= ( ship1.jumpCount ** 2) * 0.5 * neg 
            ship1.jumpCount-=1
        else : 
            ship1.isJump = False
            ship1.jumpCount = 10
    reDrawGameWindow()
 #   win.fill((0,0,0))
 #   pygame.draw.rect(win,(255,0,0),(x,y,width ,height))
 #   pygame.display.update()

pygame.quit()
