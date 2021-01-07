__author__ = "bengunur6"
import pygame 
import random
import pygame.constants





#pygame.mixer.music.load('img/through_space.ogg')
#pygame.mixer.music.play(-1)


#shoot = False
#s = pygame.surface.Surface((screenWidth,screenHeight),0,win)
#c = pygame.camera.list_cameras()
#cam = pygame.camera.Camera(c[0],(screenWidth,screenHeight))
#cam.start()
class player ():
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
        spaceShip = pygame.image.load('img/ship1.png')
        win.blit(spaceShip,(self.x,self.y))
        self.hitbox = (self.x , self.y +5 ,65,65 )
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)

    

    def hit(self):
            print("ship was shoot")



        
class shoot (object):
    def __init__(self,x,y,win):
        self.x = x
        self.y= y 
        self.vel = 10
        self.gun = (self.x  , self.y -self.vel )
        self.win=win
        
    
    def shootIT(self):
        self.gun = (self.x  ,self.y  )
        pygame.draw.circle(self.win,(255,255,255),self.gun,6)
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
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)

    def hit(self):
        print("hit")
    

class enemyy(player):
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
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        #pygame.draw.circle(win,(255,255,255),self.gun,5) 
        # pygame.display.update()

    def hit(self):
        print("alien hit")        




  

# MAin loop


 

class SpaceWarrior():
    
    def __init__(self,width,height):
        self.clock = pygame.time.Clock()
        self.screenWidth = width
        self.screenHeight = height
        self.fps=30
      
        self.clock.tick(self.fps)
        
        self.actions = {
            "shoot" : K_SPACE,
            "left" :K_LEFT,
            "right" :K_RIGHT

        }
        self.win = pygame.display.set_mode((self.screenWidth,self.screenHeight),0)
        self.win.set_alpha(None) 
        pygame.display.set_caption("Game window BNG")
        self.att=2
        pygame.init()
        pygame.mixer.init()

        self.astreoidPic = [
        pygame.image.load('img/planet1.png'),pygame.image.load('img/planet2.png'),pygame.image.load('img/planet3.png'),
        pygame.image.load('img/planet4.png'),pygame.image.load('img/planet5.png'),pygame.image.load('img/planet6.png'),
        pygame.image.load('img/planet7.png'),pygame.image.load('img/planet8.png'),pygame.image.load('img/planet9.png'),
        pygame.image.load('img/planet10.png'),pygame.image.load('img/planet11.png'),pygame.image.load('img/planet12.png'),
        pygame.image.load('img/planet13.png'),pygame.image.load('img/planet14.png'),pygame.image.load('img/planet15.png'),
        pygame.image.load('img/planet16.png'),pygame.image.load('img/planet17.png'),pygame.image.load('img/planet18.png'),
        pygame.image.load('img/planet19.png'),pygame.image.load('img/planet20.png'),]

        
        self.backGround = pygame.image.load('img/spacebackground.png')
        self.ship1 = player(self.screenWidth/2,self.screenHeight-15,71,80)
        self.fire = []
        self.alien = []
        self.score = 0 
        self.alncnt = 4
        self.alienfire = []
        self.planets = []
        self.run = True
        for i in self.astreoidPic  :
            self.planets.append(asteroid(self.astreoidPic[random.randrange(1,20)],random.randrange(5,self.screenWidth),random.randrange(-700,2),64,64))

        self.rowas = []
        self.loopsht = 0
        self.ADDENEMY = pygame.USEREVENT + 1
        self.SHOOTSHIP = pygame.USEREVENT + 2


    def reDrawGameWindow (self):

        pygame.time.set_timer(self.ADDENEMY, 10)
        pygame.time.set_timer(self.SHOOTSHIP, 4000)
        for a in self.planets:
            if a.hitbox[1]+a.hitbox[3] > self.ship1.y :
                print ("you lost ")
                self.run = False
        for i in self.alienfire:
                i.shootIT()
                i.y += i.vel 

        for i in self.alienfire:     
            if i.y - 5 < self.ship1.hitbox[1]+ self.ship1.hitbox[3] and i.y + 5 > self.ship1.hitbox[1]:
                if i.x + 5 > self.ship1.hitbox[0] and i.x - 5 < self.ship1.hitbox[0] + self.ship1.hitbox[2]:
                    self.ship1.hit()
                    self.run = False
                    pygame.quit()
                    
            if i.y > self.screenHeight :
                self.alienfire.pop(self.alienfire.index(i))
                

        for a in self.alien : 
            if  a.hitbox[1] > self.ship1.hitbox[1] :
                self.ship1.hit()
                self.run = False
                pygame.quit()
            
            
        print("clasa girdi")

        if self.loopsht > 0: 
            self.loopsht +=1
        if self.loopsht >6: 
            self.loopsht = 0
    
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_LEFT] and  self.ship1.x > self.ship1.ve :
            self.ship1.x -= self.ship1.ve * 3
            self.ship1.left = True
            self.ship1.right = False 
        elif self.keys[pygame.K_RIGHT] and  self.ship1.x < self.screenWidth - self.ship1.width  :
            self.ship1.x += self.ship1.ve * 3 
            self.ship1.right = True
            self.ship1.left = False 
        
        else :
            self.ship1.right = False
            self.ship1.left = False
            self.ship1.walkCount = 0

        if self.keys[pygame.K_SPACE] :
            self.ship1.yesshoot = True
            self.fire.append(shoot(self.ship1.x+30,self.ship1.y,self.win))
            self.loopsht +=2 
            
        for i in self.fire :
            i.shootIT()
            i.y-=i.vel * 0.7
        
        if pygame.event.get(self.ADDENEMY) :
            if not self.alien : 
                for i in range(0,2 ):
                    self.alien.append(enemyy(random.randrange(34,self.screenWidth-34),random.randrange(-300,1),88,88))
                    print("here making alien")
                    #alienfire[i].shootIT()  
            
        if pygame.event.get(self.SHOOTSHIP):
            for al in self.alien:
                self.alienfire.append(shoot(al.x+44,al.y+88,self.win))
                self.alienfire.append(shoot(al.x+44,al.y+89,self.win))

        
        for i in self.fire :
            for a in self.planets:
                if i.y - 5 < a.hitbox[1]+ a.hitbox[3] and i.y + 5 > a.hitbox[1]:
                    if i.x + 5 > a.hitbox[0] and i.x - 5 < a.hitbox[0] + a.hitbox[2]:
                        a.hit()
                        self.planets.pop(self.planets.index(a))
                        self.score+=1
                        self.fire.pop(self.fire.index(i))
                        pygame.display.update()
                        break

        for i in self.fire :
            for al in self.alien:
                if i.y  < al.hitbox[1]+ al.hitbox[3]+2 and i.y +5 > al.hitbox[1]:
                    if i.x > al.hitbox[0] and i.x  < al.hitbox[0] + al.hitbox[2]:
                        al.hit()
                        self.alien.pop(self.alien.index(al))
                        self.score+=5
                        self.fire.pop(self.fire.index(i))
                        pygame.display.update()
                        break
        for i in self.fire : 
            if i.y < self.screenHeight and i.y > 0:
                i.y -= i.vel * 5
            else :
                self.fire.pop(self.fire.index(i))


        if not self.planets:
            for i in self.astreoidPic  :
                self.planets.append(asteroid(self.astreoidPic[random.randrange(1,20)],random.randrange(5,self.screenWidth),random.randrange(-700,2),64,64))

                    
        for events in pygame.event.get():
            if events == pygame.QUIT:
                pygame.quit()

            if self.run== False:
                pygame.quit()
                


        largeFont = pygame.font.SysFont('comicsans', 30) # Font object
        text = largeFont.render('Score: ' + str(self.score), 1, (255,255,255)) # create o
        self.win.blit(self.backGround,(0,0))
        self.ship1.draw(self.win)
        for planet in self.planets :
            planet.draw(self.win)
        for al in self.alien :   
            al.draw(self.win)

        self.win.blit(text, (600, 10))
        pygame.display.update()
        

play = SpaceWarrior(600,700)