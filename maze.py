from pygame import *
# Game scene:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))


# parent class for sprites
class GameSprite(sprite.Sprite):
    # class constructor
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        # each sprite must store an image property
        self.image = transform.scale(image.load(player_image), (55, 55))
        self.speed = player_speed
        # each sprite must store the rect property it is inscribed in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# child class for the player sprite (controlled by arrows)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        new_x, new_y = self.rect.x, self.rect.y
        if keys[K_LEFT] and self.rect.x > 5:
            new_x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            new_x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            new_y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            new_y += self.speed
        if not self.collide_with_color(new_x, new_y, WALL_COLOR):
            self.rect.x, self.rect.y = new_x, new_y
            

    def collide_with_color(self, x, y, color):
        if self.rect.colliderect(maze_surface.get_rect()):
            for check_x in range(self.rect.width):
                for check_y in range(self.rect.height):
                    if self.image.get_at((x + check_x, y + check_y)) == color:
                        return True
            return False
maze_surface = transform.scale(image.load("maze.png"), (win_width, win_height))
WALL_COLOR = Color("black")



    

    

# child class for the enemy sprite (moves itself)
class Enemy(GameSprite):
    def update(self):
        if self.rect.x <= 470:
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


# class for obstacle sprites
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        # picture of the wall — a rectangle of the desired size and color
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        # each sprite must store a rect property
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        # draw.rect(window, (self.color_1, self.color_2, self.color_3), (self.rect.x, self.rect.y, self.width, self.height))



# Game characters:
player = Player('hero.png', 5, win_height - 80, 4)
monster = Enemy('cyborg.png', win_width - 80, 280, 2)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

w1 = Wall(154, 205, 50, 100, 20, 450, 10)
w2 = Wall(154, 205, 50, 100, 480, 350, 10)
w3 = Wall(154, 205, 50, 100, 20, 10, 380)

game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))


# mixer.init()
# mixer.music.load('jungles.ogg')
# mixer.music.play()
#
# money = mixer.Sound('money.ogg')
# kick = mixer.Sound('kick.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        #window.blit(background, (0, 0))
        window.blit(maze_surface, (0, 0))
        player.update()
        monster.update()

        player.reset()
        monster.reset()
        final.reset()

        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()

        # “Losing” situation
        if sprite.collide_rect(player, monster) or sprite.collide_rect(player, w1) or sprite.collide_rect(player,
                                                                                                          w2) or sprite.collide_rect(
                player, w3):
            finish = True
            window.blit(lose, (200, 200))
            #kick.play()

        # “Winning” situation
        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (200, 200))
            #money.play()

    display.update()
    clock.tick(FPS)
