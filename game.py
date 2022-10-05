import pygame, sys, random

pygame.init()

clock = pygame.time.Clock()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display_rect = display_surface.get_rect()

pygame.display.set_caption('asteroid shooter')

bg_surface = pygame.image.load('./graphics/background.png').convert_alpha()

ship_surface = pygame.image.load('./graphics/ship.png').convert_alpha()
ship_rect = ship_surface.get_rect(
        center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT))

font = pygame.font.Font('./graphics/subatomic.ttf', 50)

lasers = []
laser_surface = pygame.image.load('./graphics/laser.png').convert_alpha()
can_shoot = True
shoot_time = None

def laser_timer(can_shoot, duration = 500):
    if not can_shoot:
        current_time = pygame.time.get_ticks()
        if current_time - shoot_time > duration:
            can_shoot = True

    return can_shoot

def create_laser(pos):
    laser_rect = laser_surface.get_rect(center = pos)
    return laser_rect

def update_laser(laser_list, dt, speed = 300):
    for index, laser in enumerate(laser_list):
        if laser.y <= 0:
            laser_list.remove(laser)
            continue
        
        laser.y -= round(speed * dt)
        display_surface.blit(laser_surface, laser)

def display_score():
    text = f'Score: {pygame.time.get_ticks() // 1000}'
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(topleft = (0, 0))

    display_surface.blit(text_surface, text_rect)

meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 500)

meteor_surface = pygame.image.load('./graphics/meteor.png').convert_alpha()
meteors = []

def create_meteor():
    pos = (random.randint(0, WINDOW_WIDTH), 0)
    direction = pygame.math.Vector2(random.uniform(-0.5, 0.5), 1)

    meteor_rect = meteor_surface.get_rect(center = pos)
    return (meteor_rect, direction)


def update_meteor(meteor_list, dt, speed = 300):
    for index, meteor_tuple in enumerate(meteor_list):
        meteor, direction = meteor_tuple

        if meteor.y >= WINDOW_HEIGHT:
            meteor_list.remove(meteor_tuple)
            continue
        
        meteor.center += direction * speed * dt
        display_surface.blit(meteor_surface, meteor)

# import sound
laser_sound = pygame.mixer.Sound('./sounds/laser.ogg')
explosion_sound = pygame.mixer.Sound('./sounds/explosion.wav')
background_music = pygame.mixer.Sound('./sounds/music.wav')
background_music.play(loops = -1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:
            lasers.append(create_laser(ship_rect.midtop))
            can_shoot = False
            shoot_time = pygame.time.get_ticks()

            laser_sound.play()

        if event.type == meteor_timer:
            meteors.append(create_meteor())

    # framerate limit
    dt = clock.tick(120) / 1000

    # mouse input
    ship_rect.center = pygame.mouse.get_pos()
    presses = pygame.mouse.get_pressed()

    # update
    can_shoot = laser_timer(can_shoot)

    display_surface.fill((0, 0, 0))
    display_surface.blit(bg_surface, (0, 0))
    display_surface.blit(ship_surface, ship_rect)
    display_score() 
    update_laser(lasers, dt)
    update_meteor(meteors, dt)
    pygame.display.update()

    # collisions
    for meteor_tuple in meteors:
        meteor_rect = meteor_tuple[0]
        if ship_rect.colliderect(meteor_rect):
            pygame.quit()
            sys.exit()

    for meteor_tuple in meteors:
        meteor_rect = meteor_tuple[0]
        for laser_rect in lasers:
            if meteor_rect.colliderect(laser_rect):
                meteors.remove(meteor_tuple)
                lasers.remove(laser_rect)
                explosion_sound.play()

