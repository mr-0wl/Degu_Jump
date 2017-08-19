import os, pygame, random, time
from pygame.locals import *
from pygame.compat import geterror

global startnewgame
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')
screen_width = 800
screen_height = 400
spawn_time = 1
WHITE = (255, 255, 255)
BLACK = (0,0,0)
Clock = pygame.time.Clock()
DEAD = pygame.USEREVENT + 1
FPS, timer = 60,0
startnewgame = True
bg = pygame.image.load('background.png')

class SpriteSheet(object):
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()
    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        return image

def image(name, colorkey = None):
    #image stuff here
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
        self.change_y = 0
        self.rect.topleft = 10, 400
        self.original = self.image
        self.Dead = False
        self.jump_sound = sound('jump.wav')

    def update(self):
        self.gravity()
        self.rect.y += self.change_y

    def ground(self):
        if self.rect.bottom >= screen_height:
            self.image, self.rect = image('degurest.png', -1)

    def gravity(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 1
        if self.rect.y >= screen_height - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = screen_height - self.rect.height

    def jump(self):

        if self.rect.bottom >= 385:
            self.change_y = -24
            self.image = pygame.transform.rotate(self.image, 25)
            self.jump_sound.play()

    def dead(self):
        self.Dead = True
        self.image, self.rect = image('degudead.png', -1)
        self.rect.topleft = 10, 400

class Pipe(pygame.sprite.Sprite):
    def __init__(self, screen, height):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = image('pipe.png', -1)
        self.image = pygame.transform.scale(self.image, (50, 210))
        screen = pygame.display.get_surface()
        self.rect.topleft = 770, height
        self.change_x = 6.5

    def update(self):
        self.rect.x -= self.change_x

    def stop(self):
        self.change_x = 0
        self.rect.x += 2

def startMenu():
    startFont = pygame.font.Font('freesansbold.ttf', 100)
    instructionFont = pygame.font.Font('freesansbold.ttf', 18)
    startSurf = startFont.render('Degu Jump', True, BLACK)
    instructSurf = instructionFont.render('Press space to jump. Press space to start', True, BLACK)
    startRect = startSurf.get_rect()
    instructRect = instructSurf.get_rect()
    startRect.midtop = (screen_width / 2, 10)
    instructRect.midtop = (screen_width / 2, startRect.height + 10 + 25)
    screen.blit(bg, (0, 0))
    screen.blit(startSurf, startRect)
    screen.blit(instructSurf, instructRect)
    pygame.display.update()
    global startnewgame

    while True:

         Clock.tick(60)
         for event in pygame.event.get():
             if event.type == QUIT:
                 pygame.quit()
                 sys.exit()
             elif event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_SPACE:
                     startnewgame = False

                     return

def main():
    #main game loop here
    global running, clock, BASICFONT, screen, background
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Degu Jump")
    background = pygame.Surface(screen.get_size())
    background.fill((250,250,250))
    screen.blit(bg, (0, 0))
    pygame.display.flip()
    hit_pipe_sound = sound('hit.wav')
    score_sound = sound('score.wav')
    degu = Degu()
    score = 0
    pipelist = pygame.sprite.Group()
    clock = pygame.time.Clock()
    timer = 0
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    degusprites = pygame.sprite.RenderPlain((degu))
    running = True

    if startnewgame == True:
        startMenu()

    def GameOverScreen():
        gameOverFont = pygame.font.Font('freesansbold.ttf', 100)
        restartFont = pygame.font.Font('freesansbold.ttf', 18)
        gameSurf = gameOverFont.render('Game Over', True, BLACK)
        overSurf = gameOverFont.render('Score: ' + str(score), True, BLACK)
        restartSurf = restartFont.render('Press spacebar to restart', True, BLACK)
        gameRect = gameSurf.get_rect()
        overRect = overSurf.get_rect()
        restartRect = restartSurf.get_rect()
        gameRect.midtop = (screen_width / 2, 10)
        overRect.midtop = (screen_width / 2, gameRect.height + 10 + 25)
        restartRect = (300, overRect.height + 130)
        degusprites.update()
        pipelist.update()
        screen.blit(bg, (0, 0))
        degusprites.draw(screen)
        pipelist.draw(screen)
        screen.blit(gameSurf, gameRect)
        screen.blit(overSurf, overRect)
        screen.blit(restartSurf, restartRect)
        pygame.display.update()
        pygame.time.wait(500)

        while True:

             Clock.tick(60)
             for event in pygame.event.get():
                 if event.type == QUIT:
                     pygame.quit()
                     sys.exit()
                 elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:

                        pipelist.empty()
                        degu.Dead = False
                        running = True
                        main()

    while running:
        Clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

                    degu.jump()

        timer += 1
        if timer >= random.randint(46, 66) and degu.Dead == False:
            pipelist.add(Pipe(screen, random.randint(270, 380)))
            timer = 0

        pipelist.update()
        degusprites.update()

        screen.blit(bg, (0, 0))
        degusprites.draw(screen)
        pipelist.draw(screen)
        hit = pygame.sprite.spritecollide(degu, pipelist, False)
        if hit:
            hit_pipe_sound.play()
            degu.dead()
            running = False
            GameOverScreen()
            timer = 0

            for i in pipelist:
                i.stop()


        for pipe in pipelist:
            if pipe.rect.x < 0:
                pipe.kill()
                score += 1
                score_sound.play()
        for gu in degusprites:
            if gu.rect.y <= 180:
                gu.image = gu.original

        scoreSurf = BASICFONT.render('Score: ' + str(score), 1, BLACK)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (screen_width - 100, 10)
        screen.blit(scoreSurf, scoreRect)


        pygame.display.flip()


    pygame.quit()

if __name__ == '__main__':
    main()
