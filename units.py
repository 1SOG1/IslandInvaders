import math
from config import *
"""
This files contains the classes that are used to create instances of the players unit (a tower/tank)
as well as the enemy units (ships)
The superclass in this file is called "Units" all other units will inherit from this unit. 
"""


class Projectile:

    def __init__(self, x, y, projectile_image, speed_x, speed_y, ):
        self.x = x + 80
        self.y = y + 35
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.image = projectile_image
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = self.x, self.y
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, window):
        """
        Draws projectile on the Surcface
        :param window: Surface
        :return: None
        """
        window.blit(self.image, (self.x, self.y))

    def move(self, speed):
        """
        sets the direction for the projectile to travel and moves the projectile
        :param speed: Int
        :return: None
        """
        self.x += self.speed_x
        self.y += self.speed_y



    def off_screen(self, width):
        """
        Checks if projectile is off screen
        :param width: Int
        :return: Bool
        """
        return not (self.x <= width and self.x >= 0)

    def collision(self, enemy):
        """
        checks for collision
        :param enemy: Enemy
        :return: Bool
        """
        return collide(self, enemy)


class Player:
    cooldown_time = 5

    def __init__(self, health=1000):
        self.x = 100
        self.y = 540
        self.position = self.x, self.y
        self.health = health
        self.image = player_tower
        self.original_image = player_tower
        self.projectile_image = projectile_image_one
        self.projectiles = []
        self.projectile_speed = 10
        self.cool_down_counter = 0
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, window):
        """
        Draws the player object/unit on to the screen.
        For any projectiles fired it will also draw these to the window.
        :param window: Surface
        :return: None
        """
        window.blit(self.image, (self.x, self.y))
        self.move()
        for projectile in self.projectiles:
            projectile.draw(window)

    def move(self):

        vector2_pos = pygame.math.Vector2(self.position)
        direction = pygame.mouse.get_pos() - vector2_pos
        radius, angle = direction.as_polar()
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_width(self):
        """
        Returns the width of the player object/unit
        :return: Int
        """
        return self.image.get_width()

    def get_height(self):
        """
        Returns the height of the player object/unit
        :return: Int
        """
        return self.image.get_height()

    def cooldown(self):
        """
        Sets a cooldown for the player unit between each shot fired
        :return: None
        """

        if self.cool_down_counter >= self.cooldown_time:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        """
        Controls weather or not the player can shoot or not based on the cooldown counter
        :return: None
        """

        mouse_pos = pygame.mouse.get_pos()
        mouse_pos_x = mouse_pos[0]
        mouse_pos_y = mouse_pos[1]
        dir_x = self.x - mouse_pos_x
        dir_y = mouse_pos_y - self.y
        angle = math.atan2(dir_x, dir_y)
        speed_x = math.sin(angle) * self.projectile_speed
        speed_y = math.cos(angle) * self.projectile_speed
        if speed_x < 0:
            speed_x = speed_x * -1
        else:
            speed_y = speed_y

        if self.cool_down_counter == 0:
            projectile = Projectile(self.x, self.y, self.projectile_image, speed_x, speed_y)
            self.projectiles.append(projectile)
            self.cool_down_counter = 1


    def projectile_control(self, speed, units):
        """
        Moves projectiles fired by the player. Also runs the cooldown methode, and checks for collision and
        if projectile is outside the playspace
        :param speed: Int
        :param units:
        :return: None
        """


        self.cooldown()

        for projectile in self.projectiles:
            projectile.move(speed)
            if projectile.off_screen(WIDTH):
                self.projectiles.remove(projectile)
            else:
                for unit in units:
                    if projectile.collision(unit):
                        units.remove(unit)
                        if projectile in self.projectiles:
                            self.projectiles.remove(projectile)


# Spawning class/function?


class Enemy:
    images = []

    def __init__(self, health=1000):
        random_x = random.randint(2000, 3500)
        random_y = random.randint(100, 980)
        self.x = round(random_x)
        self.y = round(random_y)
        self.health = health
        self.image = red_ship
        self.animation = 0
        self.explode_image = enemy_explosion
        self.enemies = []
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, window):
        """
        Draws enemy onto the surface
        :param window: Surface
        :return: None
        """

        window.blit(self.image, (self.x, self.y))

    def move(self, speed, window):
        """
        Moves the enemy, and also displays an explosion effect if enemy gets to close to shore
        :param speed: Int
        :param window: Surface
        :return: None
        """
        self.animation += 1
        if self.animation == 8:
            self.animation = 1
        if self.x > 500:
            self.x -= speed
        elif self.x > 370 and self.x < 500:
            self.x -= (speed / 2)
            window.blit(enemy_explosion, (self.x, self.y))
            pygame.display.update()
        else:
            self.x = 0.1

    def explode(self):
        """
        Adds an explosion to the enemy ship
        :return: None
        """
        self.draw(self.explode_image)

    def get_width(self):
        """
        Returns the width of the enemy object/unit
        :return: Int
        """
        return self.image.get_width()
    def get_height(self):
        """
        Returns the height of the enemy object/unit
        :return: Int
        """
        return self.image.get_height()



# I did not get this to work right so it is not part of the code being run, but i wanted to leave it in so at least the
# thought process was available. It was suppose to add an animation to the ship movement.
class Gunboat(Enemy):
    """
    Easiest enemy
    Adds enemy animation by cycleing thru the images in the enemie/red_ship folder named enemyOneX.png where x is
    increased for each frame
    """
    # imgs = []
    # x_axis = 2000
    # # Animates the ship on the water
    # while x_axis >= 150:
    #     for x in range(1, 9):
    #         imgs.append(
    #             pygame.image.load(os.path.join("assets/enemies/red_ship",
    #                                            ("enemyOne" + str(x) + ".png")))
    #                     )
    #         x += 1
    #
    pass


class Cruiser(Enemy):
    pass


def collide(unit1, unit2):
    offset_x = int(unit2.x) - int(unit1.x)
    offset_y = int(unit2.y) - int(unit1.y)
    return unit1.mask.overlap(unit2.mask, (offset_x, offset_y)) != None
