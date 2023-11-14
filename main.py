import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("player_walk_1.png").convert_alpha()
        player_walk2 = pygame.image.load("player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk2]
        self.player_index = 0

        self.player_jump = pygame.image.load("jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom =(80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("jump.mp3")
        self.jump_sound.set_volume(0.3)
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]



    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == "fly":
            fly_1 = pygame.image.load("fly1.png").convert_alpha()
            fly_2 = pygame.image.load("fly2.png").convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load("snail1.png").convert_alpha()
            snail_2 = pygame.image.load("snail2.png").convert_alpha()
            self.frames = [snail_1,snail_2]
            y_pos = 300
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surface = test_font.render(f"Score: {current_time}",False,(64,64,64))
    score_rect = score_surface.get_rect(center =(330,50))
    gameDisplay.blit(score_surface, score_rect)
    return current_time
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 10
            if obstacle_rect.bottom == 300:
                gameDisplay.blit(snail_surface,obstacle_rect)
            else:
                gameDisplay.blit(fly_surface,obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True


def player_animation():
    global player_surface, player_index
    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]

pygame.init()
#display settings
display_width = 700
display_height = 400
gameDisplay = pygame.display.set_mode((700,400))
pygame.display.set_caption("Jumper by Roniel")
game_active = False
start_time = 0
score = 0

bg_music = pygame.mixer.Sound("music.wav")
bg_music.play(loops = -1)
bg_music.set_volume(0.01)
#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

#colors
white = (255,255,255)
black = (0,0,0)
#clock
clock = pygame.time.Clock()

test_font = pygame.font.Font("Pixeltype.ttf", 50)

sky_surface = pygame.image.load("Sky.png").convert()
ground_surface = pygame.image.load("ground.png").convert()
#enemy animation
snail_1 = pygame.image.load("snail1.png").convert_alpha()
snail_2 = pygame.image.load("snail2.png").convert_alpha()
snail_frames = [snail_1, snail_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

fly_1 = pygame.image.load("Fly1.png").convert_alpha()
fly_2 = pygame.image.load("Fly2.png").convert_alpha()
fly_frames = [fly_1,fly_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rect_list = []
player_walk_1 = pygame.image.load("player_walk_1.png").convert_alpha()
player_walk2 = pygame.image.load("player_walk_2.png").convert_alpha()
player_walk = [player_walk_1,player_walk2]
player_index = 0
player_jump = pygame.image.load("jump.png").convert_alpha()
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (80,300))
#gameover screen
player_stand = pygame.image.load("player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,120,2)
player_stand_rect = player_stand.get_rect(center=(350,200))

game_name = test_font.render("Jumper",False,(64,64,64))
game_name_rect = game_name.get_rect(center =(350,50))
start = test_font.render("Press space bar to start.",False,(64,64,64))
start_rect = start.get_rect(center= (350,370))
start_again = test_font.render("Press space bar to play again.", False,(64,64,64))
start_again_rect = start_again.get_rect(center= (350,370))

player_gravity = 0
last_seconds = None

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,900)

snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer, 400)

fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 300:
                    player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                        player_gravity = -20
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["fly","snail","snail"])))

            if event.type == snail_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]
            if event.type == fly_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)


    if game_active:
        gameDisplay.blit(sky_surface,(0,0))
        gameDisplay.blit(ground_surface,(0,300))
        score = display_score()


        player.draw(gameDisplay)
        player.update()

        obstacle_group.draw(gameDisplay)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        gameDisplay.fill("Pink")
        gameDisplay.blit(game_name,game_name_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0
        gameDisplay.blit(player_stand, player_stand_rect)
        score_message = test_font.render(f"High Score: {score}", False, (64, 64, 64))
        score_message_rect = score_message.get_rect(center=(350, 90))
        if score == 0:
            gameDisplay.blit(start,start_rect)
        else:
            gameDisplay.blit(score_message,score_message_rect)
            gameDisplay.blit(start_again,start_again_rect)

    pygame.display.update()
    clock.tick(60)
