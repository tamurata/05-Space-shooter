import sys, logging, os, random, math, open_color, arcade

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MARGIN = 30
SCREEN_TITLE = "Space Shooter"

NUM_ENEMIES = 5 
INITIAL_VELOCITY = 10
STARTING_LOCATION = (400,100)
BULLET_DAMAGE = 10
PLAYER_HP = 200
ENEMY_HP = 100
HIT_SCORE = 10
KILL_SCORE = 100

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the bullet
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("assets/sara-logo.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy

class Enemy_Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):

        super().__init__("assets/facebook-24x24.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity 
        self.damage = damage
    def update(self):
        self.center_x += self.dx
        self.center_y += self.dy

    
class Player(arcade.Sprite):
    def __init__(self):
        self.hp = PLAYER_HP
        super().__init__("assets/straship2.PNG", 0.3)
        (self.center_x, self.center_y) = STARTING_LOCATION

class Enemy(arcade.Sprite):
    def __init__(self, x, y, dx, dy):
        '''
        initializes a twitter enemy
        Parameter: position: (x,y) tuple
        '''
        super().__init__("assets/twitter-24x24.png", 2.0)
        self.center_x = x
        self.center_y = y
        self.dx = dx
        self.dy = dy
        self.hp = ENEMY_HP

    def update(self):
      self.center_x += self.dx
      
 

    def accelerate(self, dx, dy):
        self.dx += dx
        self.dy += dy

        



        


class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.background = None
        self.set_mouse_visible(True)
        arcade.set_background_color((255,192,120))
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.player = Player()
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.score = 0
        self.alive = True

    def setup(self):
        '''
        Set up enemies
        '''
        self.background = arcade.load_texture("open_color/background.jpg")
        for i in range(NUM_ENEMIES):
            x = random.randint(MARGIN,SCREEN_WIDTH-MARGIN)
            y = 500
            dx = random.uniform(-INITIAL_VELOCITY, INITIAL_VELOCITY)
            dy = random.uniform(-INITIAL_VELOCITY, INITIAL_VELOCITY)
            self.enemy = Enemy(x,y,dx,dy)
            self.enemy_list.append(self.enemy)
            print(self.enemy_list)          

    def update(self, delta_time):
        if self.alive:
            self.enemy_list.update()
            for a in self.enemy_list:
                a.center_x = a.center_x + a.dx
                if a.center_x <= 0:
                    a.dx = abs(a.dx)    
                if a.center_x >= SCREEN_WIDTH:
                    a.dx = abs(a.dx) * -1
                

            self.bullet_list.update()
            for e in self.enemy_list:
                if random.randint(0,100) < 1:
                    x = e.center_x
                    y = e.center_y + 15
                    bullet = Bullet((x,y),(0,-10),BULLET_DAMAGE)
                    self.enemy_bullet_list.append(bullet) 

                damage = arcade.check_for_collision_with_list(e,self.bullet_list)
                for d in damage:
                    e.hp = e.hp - d.damage
                    d.kill()
                    if e.hp < 0:
                        self.score += KILL_SCORE
                        e.kill()
                    else:
                        self.score += HIT_SCORE
                
                # check for collision
                # for every bullet that hits, decrease the hp and then see if it dies
                # increase the score
                # e.kill() will remove the enemy sprite from the game
                # the pass statement is a placeholder. Remove line 81 when you add your code
            
            self.enemy_bullet_list.update()
            for p in self.player_list:
                damage = arcade.check_for_collision_with_list(p,self.enemy_bullet_list)
                for d in damage:
                    p.hp = p.hp - d.damage
                    d.kill()
                    if p.hp < 0:
                        p.kill()
                        self.alive = False
                    
        
        self.enemy_bullet_list.update()
                


    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
        SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        if self.alive:
            arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT -10, open_color.white, 16)
            self.player.draw()
            self.bullet_list.draw()
            self.enemy_list.draw()
            self.enemy_bullet_list.draw()
        else:
            arcade.draw_text("You have died", 400, SCREEN_HEIGHT - 350, open_color.white, 50)


    def on_mouse_motion(self, x, y, dx, dy):
        '''
        The player moves left and right with the mouse
        '''
        self.player.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            x = self.player.center_x
            y = self.player.center_y + 15
            bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
            self.bullet_list.append(bullet) 
            #fire a bullet
            #the pass statement is a placeholder. Remove line 97 when you add your code


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()