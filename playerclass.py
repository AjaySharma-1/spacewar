import pygame ,random
pygame.init()
bgCol= (0,0,0)

HEIGHT= 800
WEIDTH = 800
SPEED= 10
screen = pygame.display.set_mode((WEIDTH, HEIGHT))
enemycount= 0
scale= 1


        
class Player(pygame.sprite.Sprite):
    
    def __init__(self,picture):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(picture).convert_alpha()
        self.image= pygame.transform.scale(self.image, (60,60))
        self.rect= self.image.get_rect(center = (WEIDTH//2,HEIGHT-60))
        self.count= 0
        self.hitcount= 0
        self.playerspeed_x= 10 
        self.playerspeed_y= 10 


        
    def keyHandling(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]or keys[pygame.K_LEFT]:
            self.rect.x-= self.playerspeed_x
            if self.rect.centerx < 0 :
                self.rect.centerx= 0
            
        if keys[pygame.K_d]or keys[pygame.K_RIGHT]:
            self.rect.x += self.playerspeed_x
            if self.rect.centerx>= WEIDTH:
                self.rect.centerx= WEIDTH
        if keys[pygame.K_w]or keys[pygame.K_UP]:
            self.rect.y -= self.playerspeed_y
            if self.rect.centery< 0:
                self.rect.centery= 0

        if keys[pygame.K_s]or keys[pygame.K_DOWN]:
            self.rect.y += self.playerspeed_y 
            if self.rect.centery>= HEIGHT:
                self.rect.centery= HEIGHT

        if keys[pygame.K_SPACE]:
            if self.count== 5:
                bullet = self.createBullet()
                bulletGroup.add(bullet)
                self.count= 0        

            self.count+=1

    def checkCollision (self):
        hit = pygame.sprite.spritecollide(self, enemybulletGroup, True)
        if hit:
            self.hitcount+= 1
            if self.hitcount== 2:
                # managestate.state= "playagain"
                self.kill()
                self.hitcount= 0  
                # del self
                     

        
    def createBullet(self):
        return Bullet(self.rect.centerx, self.rect.centery-20,bullet_speed=20, kill_dis=30)   


    def update(self ):
        self.keyHandling()
        self.checkCollision()
       
        
        if self.rect.y<= -20 or self.rect.y>= WEIDTH+ 20 :
            self.rect.y = self.rect.y
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image= pygame.image.load(f"ship{random.randint(1,5)}.jpg").convert_alpha()
        self.image= pygame.transform.scale(self.image,(scale*60,scale*60))
        self.rect= self.image.get_rect(center= (random.randint(66,WEIDTH-60),0))
        self.x_speed= random.randint(-5,5)
        self.y_speed =1
        self.count = 300
        
    def checkCollision (self):
        hit = pygame.sprite.spritecollide(self, bulletGroup, True)
        if hit:
            
            self.kill()


    def update(self):
        self.rect.y += self.y_speed
        if self.rect.y> HEIGHT+ 60:
            self.kill()

        self.rect.x+=self.x_speed
        if self.rect.x > WEIDTH-60 or self.rect.x < 0 :
            self.x_speed= - self.x_speed
        self.checkCollision()
        
        if self.count==300:
            bullet=self.create_bullet()
            enemybulletGroup.add(bullet)
            self.count = 0

            
        self.count+=1    
            


    def create_bullet(self):
        return Bullet(self.rect.centerx, self.rect.centery+20,bullet_speed=-5, bullet_rotation=90, bullet_scale=1,kill_dis=600)   

        


                     

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x,y,bullet_rotation= -90, bullet_speed=15,bullet_scale=2,kill_dis=-200):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_rotation= bullet_rotation
        self.image = pygame.image.load("bullet.png").convert_alpha()
        self.image= pygame.transform.rotate(self.image,self.bullet_rotation)
        self.image= pygame.transform.scale(self.image, (bullet_scale*5,bullet_scale*20))
        self.rect= self.image.get_rect(center= (x,y))
        self.bullet_speed = bullet_speed
        self.kill_dis= kill_dis
    def update(self):
        self.rect.y-= self.bullet_speed
        if self.rect.y==  self.kill_dis:
            self.kill()


player= Player("spaceship.png")
pygame.mouse.set_visible(False)
playerGroup= pygame.sprite.Group()
playerGroup.add(player)
bulletGroup= pygame.sprite.Group()
enemyGroup= pygame.sprite.Group()

enemybulletGroup= pygame.sprite.Group()
clock = pygame.time.Clock()
running = True 
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running= False

        
             
    screen.fill(bgCol)
    if enemycount == 50:
        for i in range(1):
            enemy = Enemy()
            enemyGroup.add(enemy)
            enemycount = 0
    enemycount+=1   
    bulletGroup.draw(screen)
    playerGroup.draw(screen)
    playerGroup.update()
    bulletGroup.update()
    enemyGroup.update()
    enemybulletGroup.draw(screen)
    enemyGroup.draw(screen)

    enemybulletGroup.update()
    pygame.display.update()
    clock.tick(60)

    