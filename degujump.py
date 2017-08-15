import os, pygame, random
from pygame.locals import *
from pygame.compat import geterror

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')
screen_width = 800
screen_height = 400
Clock = pygame.time.Clock()


def image(name, colorkey = None):
    #image load stuff here
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ("cannot load image:", fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def sound(name):
    #sound load stuff here
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ("Cannot load sound: %s" % fullname)
        raise SystemExit(str(geterror()))
    return sound

class Degu(pygame.sprite.Sprite):
    #degu stuff here, jump, collission, animation
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = image('degurest.png', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 300
        self.change_x = 0
        self.change_y = 0
        self.power_y = 0
    def update(self):
        self.gravity()
        self.power()
        self.rect.x += self.change_x
        self.rect.y -= self.change_y
        self.rect.y += self.power_y

    def gravity(self):
        if self.rect.y < 300:
            self.change_y = -9
        elif self.rect.y == 300:
            self.change_y = 0



    def power(self):
        if self.rect.y <= 150:
            self.power_y = 0
        else:
            pass

    def jump(self):
        if self.rect.y >= 300:
            self.power_y = -18




class Pipe(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.image.load('Pipe.png')
        #self.image = pygame.transform.scale(image, (100, 100))
        #self.rect = image.get_rect()
        self.image, self.rect = image('pipe.png', -1)
        self.image = pygame.transform.scale(self.image, (50, 210))
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 500, random.randint(200, 450)
        self.change_x = 0
    def move(self):
        self.rect.x -= 4
    #def spawn(self):
     #   size = random.randint(200, 450)
      #  self.rect.topleft = 500, size
       # self.move()





def score():
    #score stuff here
    pass

def menu():
    # start menu here
    pass

def tube():
    #tubes and random sizing here
    pass



def main():
    #main game loop here
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Degu Jump")
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250,250,250))


    screen.blit(background, (0, 0))
    pygame.display.flip()

    degu = Degu()
    pipe = Pipe()

    count = 0

    allsprites = pygame.sprite.RenderPlain((degu, pipe))
    running = True
    while running:
        Clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    degu.jump()


        pipelist = pygame.sprite.Group()

        pipelist.add(pipe)
        for pipe in pipelist:
            pipe.move()
            screen.blit(background, (0,0))
            pipelist.draw(screen)
            allsprites.draw(screen)
            pygame.display.update()
            pygame.display.flip()


    pygame.quit()

if __name__ == '__main__':
    main()
