import pygame 
import random
 

pygame.init()
pygame.mixer.init()
#pygame.mixer.music.load('img/through_space.ogg')
#pygame.mixer.music.play(-1)
clock = pygame.time.Clock()
screenWidth = 700
screenHeight = 900
win = pygame.display.set_mode((screenWidth,screenHeight))

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
        self.right = False 
        self.left = False
        self.hitbox = (self.x , self.y +5 ,65,65 )
        self.gun = (self.x , self.y- 10  ) 

    def draw(self,win):
        win.blit(spaceShip[0],(self.x,self.y))
        self.hitbox = (self.x , self.y +5 ,65,65 )
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)

    def hit(self):
        print("ship was shoot")


        
class shoot (object):
    def __init__(self,x,y):
        self.x = x
        self.y= y 
        self.vel = 10
        self.gun = (self.x  , self.y -self.vel )
        
    
    def shootIT(self):
        self.gun = (self.x  ,self.y  )
        pygame.draw.circle(win,(255,255,255),self.gun,6)
        pygame.display.update()
    
    


class asteroid(player):
    def __init__(self,pic ,x,y,w,h):
        self.x= x 
        self.y = y 
        self.width = w 
        self.height = h
        self.pic = pic 
        self.hitbox = (self.x , self.y ,64,64 )

    def draw(self,win):
        self.y+=1
        win.blit(self.pic,(self.x ,self.y))
        self.hitbox = (self.x , self.y ,65,65 )
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)

    def hit(self):
        print("hit")
    

class enemyy():
    def __init__(self,x,y,w,h):
        self.x = x 
        self.y = y 
        self.width = w 
        self.height = h
        self.pic = pygame.image.load('img/5.png') 
        self.vel=3
        self.neg= 1
        self.hitbox = (self.x , self.y ,w,h )
        self.jumpCount = random.randrange(-10,20)
        self.ay = y
        self.ax = x
        self.gun = (self.ax  ,self.ay)

    def draw(self,win):
        self.y+=1
        self.gun = (self.ax  ,self.ay)
        self.ay +=4
        if(self.jumpCount >= -20):
            self.neg= 1
            if(self.jumpCount < 0):
                self.neg = -1
        else : 
            self.jumpCount = 20

        self.x += (self.vel ** 2) * 0.5 * self.neg
        self.jumpCount-=0.5
        win.blit(self.pic,(self.x ,self.y))
        self.hitbox = (self.x , self.y ,self.width+1,self.height+1 )
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        #pygame.draw.circle(win,(255,255,255),self.gun,5) 
        # pygame.display.update()

    def hit(self):
        print("alien hit")        



def reDrawGameWindow ():
    largeFont = pygame.font.SysFont('comicsans', 30) # Font object
    text = largeFont.render('Score: ' + str(score), 1, (255,255,255)) # create o
    win.blit(backGround,(0,0))
    ship1.draw(win)
    for planet in planets :
        planet.draw(win)
    for al in alien :   
        al.draw(win)

    win.blit(text, (600, 10))
    pygame.display.update()
    
win.set_alpha(None)   

# MAin loop
astreoidPic = [
pygame.image.load('img/planet1.png'),pygame.image.load('img/planet2.png'),pygame.image.load('img/planet3.png'),
pygame.image.load('img/planet4.png'),pygame.image.load('img/planet5.png'),pygame.image.load('img/planet6.png'),
pygame.image.load('img/planet7.png'),pygame.image.load('img/planet8.png'),pygame.image.load('img/planet9.png'),
pygame.image.load('img/planet10.png'),pygame.image.load('img/planet11.png'),pygame.image.load('img/planet12.png'),
pygame.image.load('img/planet13.png'),pygame.image.load('img/planet14.png'),pygame.image.load('img/planet15.png'),
pygame.image.load('img/planet16.png'),pygame.image.load('img/planet17.png'),pygame.image.load('img/planet18.png'),
pygame.image.load('img/planet19.png'),pygame.image.load('img/planet20.png'),]

spaceShip = [pygame.image.load('img/ship1.png'),pygame.image.load('ship_F5.png'),]
backGround = pygame.image.load('img/spacebackground.png')
ship1 = player(225,620,71,80)
fire = []
alien = []
score = 0 
alncnt = 4
alienfire = []
planets = []
for i in astreoidPic  :
    planets.append(asteroid(astreoidPic[random.randrange(1,20)],random.randrange(64,screenWidth-64),random.randrange(-700,2),64,64))

rowas = []
loopsht = 0
ADDENEMY = pygame.USEREVENT + 1
SHOOTSHIP = pygame.USEREVENT + 2

pygame.time.set_timer(ADDENEMY, 10)
pygame.time.set_timer(SHOOTSHIP, 4000)

run = True 
while run:
    clock.tick(50)
    for a in planets:
        if a.hitbox[1]+a.hitbox[3] > ship1.y :
            print ("you lost ")
            run = False

 #   for af in alienfire:
  #      for al in alien:
   #         alienfire.append(shoot(alien[al].x+15,alien[al].y))
    #        alienfire.append(shoot(alien[al].x+15,alien[al].y+10))

    for i in alienfire:
        i.shootIT()
        i.y += i.vel 

    for i in alienfire:     
        if i.y - 5 < ship1.hitbox[1]+ ship1.hitbox[3] and i.y + 5 > ship1.hitbox[1]:
            if i.x + 5 > ship1.hitbox[0] and i.x - 5 < ship1.hitbox[0] + ship1.hitbox[2]:
                ship1.hit()
                run = False
                
        if i.y > screenHeight :
            alienfire.pop(alienfire.index(i))
            

    for a in alien : 
        if  a.hitbox[1] > ship1.hitbox[1] :
            ship1.hit()
            run = False
        
        
            

    if loopsht > 0: 
        loopsht +=1
    if loopsht >6: 
        loopsht = 0
   
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and  ship1.x > ship1.ve :
        ship1.x -= ship1.ve * 3
        ship1.left = True
        ship1.right = False 
    elif keys[pygame.K_RIGHT] and  ship1.x < screenWidth - ship1.width  :
        ship1.x += ship1.ve * 3 
        ship1.right = True
        ship1.left = False 
    
    else :
        ship1.right = False
        ship1.left = False
        ship1.walkCount = 0

    if keys[pygame.K_SPACE] :
        ship1.yesshoot = True
        fire.append(shoot(ship1.x+30,ship1.y))
        loopsht +=2 

    for i in fire :
        i.shootIT()
        i.y-=i.vel * 0.7
    
    if pygame.event.get(ADDENEMY) :
        if not alien : 
            for i in range(0,2 ):
                alien.append(enemyy(random.randrange(34,screenWidth-34),random.randrange(-300,1),88,88))
                print("here making alien")
                #alienfire[i].shootIT()  
        
    if pygame.event.get(SHOOTSHIP):
        for al in alien:
            alienfire.append(shoot(al.x+44,al.y+88))
            alienfire.append(shoot(al.x+44,al.y+89))

    
    for i in fire :
        for a in planets:
            if i.y - 5 < a.hitbox[1]+ a.hitbox[3] and i.y + 5 > a.hitbox[1]:
                if i.x + 5 > a.hitbox[0] and i.x - 5 < a.hitbox[0] + a.hitbox[2]:
                    a.hit()
                    planets.pop(planets.index(a))
                    score+=1
                    fire.pop(fire.index(i))
                    pygame.display.update()
                    break

    for i in fire :
        for al in alien:
            if i.y  < al.hitbox[1]+ al.hitbox[3]+2 and i.y +5 > al.hitbox[1]:
                if i.x > al.hitbox[0] and i.x  < al.hitbox[0] + al.hitbox[2]:
                    al.hit()
                    alien.pop(alien.index(al))
                    score+=5
                    fire.pop(fire.index(i))
                    pygame.display.update()
                    break
    for i in fire : 
        if i.y < screenHeight and i.y > 0:
            i.y -= i.vel * 5
        else :
            fire.pop(fire.index(i))


    if not planets:
        for i in astreoidPic  :
            planets.append(asteroid(astreoidPic[random.randrange(1,20)],
            random.randrange(64,screenWidth-64),random.randrange(-700,2),64,64))

                
        #fire = []
       

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    reDrawGameWindow()

pygame.quit()
exit()  