# This is a simple car racing game that you play versus a computer car.
# You get 10 levels, and each level the computer car speed increases.
# To move your car, you have to press the arrow keys.
# As info on your screen, you will get the level you are, you car speed and time elapsed.
# ENJOY!

import pygame
import time
import math
from utils import scale_image, blit_rotate_center, blit_text_center
pygame.font.init()

# Creating constants for each images loaded and used for the game
GRASS = scale_image(pygame.image.load("C:/VSC/Car Game/imgs/grass.jpg"), 2)
TRACK = scale_image(pygame.image.load("C:/VSC/Car Game/imgs/track.png"), 0.9)
TRACK_BORDER = scale_image(pygame.image.load("C:/VSC/Car Game/imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH = pygame.image.load("C:/VSC/Car Game/imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (130, 250)
RED_CAR = scale_image(pygame.image.load("C:/VSC/Car Game/imgs/red-car.png"), 0.55)
GREEN_CAR = scale_image(pygame.image.load("C:/VSC/Car Game/imgs/green-car.png"), 0.55)
# Get the W and H of the track to be used later
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
# creating pygame window (tuple that includes the W and H of the track)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Adding the game title
pygame.display.set_caption("Racing Game!")
MAIN_FONT = pygame.font.SysFont("arial", 30) # Defining a FONT object (style and height)
# COnstant that will limit the game to run faster than 60FPS
FPS = 60
PATH = [(175, 119), (110, 70), (56, 133), (70, 481), (318, 731), (404, 680), (418, 521), (507, 475), (600, 551), (613, 715), (736, 713),
        (734, 399), (611, 357), (409, 343), (433, 257), (697, 258), (738, 123), (581, 71), (303, 78), (275, 377), (176, 388), (178, 260)]
# Class for the informations about the game
class GameInfo:
    LEVELS = 10 #Constant for the maximum levels of the game
    
    def __init__(self, Level = 1):
        self.level = Level
        self.started = False #Indicating if the current level started or not
        self.level_start_time = 0
# Method for incrementing to next level
    def next_level(self):
        self.level += 1
        self.started = False
# Method for reseting the game
    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0
# Method for finishing the game
    def game_finished(self):
        return self.level > self.LEVELS
# Method for starting the game
    def start_level(self):
        self.started = True
        self.level_start_time = time.time()
# Method for getting the elapsed time from start
    def get_level_time(self):
        if not self.started:
            return 0 # If game not started, return 0 as time
        return round(time.time() - self.level_start_time)# If game started, return elapsed time
# Creating a class that handles the movement of both cars(Players and computer) - Base class for the PlayerCar and ComputerCar classes
class AbstractCar:
# Defining the class constructor.This self represents the object of the class itself.
    def __init__(self, max_vel, rotation_vel): #Adding the parameters
        self.img = self.IMG 
        self.max_vel = max_vel
        self.vel = 0 #The car will start at speed 0
        self.rotation_vel = rotation_vel
        self.angle = 0 #The car will start at 0deg angle
        self.x, self.y = self.START_POS
# Everytime we press the "w" key, we increase the acceleration by 0.1 px/s
        self.acceleration = 0.1
# Method used for rotating the cars
    def rotate(self, left = False, right = False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
# Method that draws the cars  
    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)
# Method for increasing the velocity of the car based on the acceleration.
# If we are at max velocity it won't do anything but will move forward.
# If self.vel is already at the max and we add self.acceleration, we don't want to go faster than max vel.
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
#Method for reversing the car. Maximum reverse velocity is half of the forward velocity.
    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()
        
    def move(self):
        radians = math.radians(self.angle) #Converting angles into radians
        vertical = math.cos(radians) * self.vel #Calculating the vertical velocity
        horizontal = math.sin(radians) * self.vel #Calculating the horizontal velocity
        
        self.y -= vertical
        self.x -= horizontal
#Defining a method for collision of both cars with the track border 
    def collide(self, mask, x = 0, y = 0):
        car_mask = pygame.mask.from_surface(self.img)#Creating a mask for the cars
        offset = (int(self.x - x), int(self.y - y))# Calculating the offset
        poi = mask.overlap(car_mask, offset)#Point Of Intersection between the two masks
        return poi
# Reseting the cars positions when a level is completed    
    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0
        
# Creating a child class of AbstractCar class that inherits its methods for the player car
class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (180, 200)
# Method used to reduce the player car speed when we stop pressing the up arrow key.
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0) #Reducing the speed by half of the acceleration
        self.move()
# Method for bouncing the car back when we hit the track border, by reversing the velocity       
    def bounce(self):
        self.vel = -self.vel
        self.move()
    
    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

# Creating a child class of AbstractCar class that inherits its methods for the computer car
class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)
# Overriding the initialization
    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel
# Method for drawing the computer car path points          
    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)
      
 
    def draw(self, win):
        super().draw(win) #Calling the draw method from AbstractCar class
        # self.draw_points(win) # Drawing on the screen the computer car path points
        
#  Method for calculating the angle      
    def calculate_angle(self):
# Calculating the displacement in X an Y between the target point and the current position
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y
 
        if y_diff == 0: #If we have no diff in Y, we are horizontal
            desired_radian_angle = math.pi/2# Angle between the car and the point
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)# Angle between the car and the point
        
        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >=180:
            difference_in_angle -= 360
            
        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))
# Method for moving the car to the next path point  
    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):#Check for collision
            self.current_point += 1 #Moving to the next point
        
           
    def move(self):
        if self.current_point >= len(self.path): #Making sure that the computer car has a path point to move to.
            return
             
        self.calculate_angle()# Calculating the angle and shift the car towards that direction
        self.update_path_point() #Check if the computer car has to move to a next path point
        super().move() # Calling the move method from AbstractCar class
# Method for increaseing the computer car speed after each level (based on each level)    
    def next_level(self, Level):
        self.reset()
        self.vel = self.max_vel + (Level - 1) * 0.2 # We don't want the computer car to be faster than the player car, thus LEVEL-1 is used
        self.current_point = 0
         
def draw(win, images, player_car, computer_car, game_info):
    for img, pos in images:
        win.blit(img, pos)
# Adding to the game window text about level information
    level_text = MAIN_FONT.render(f"Level: {game_info.level}", 1, (255, 255, 255))   
    win.blit(level_text, (10, HEIGHT - level_text.get_height() - 80))# Displaying on the screen
# Adding to the game window text about elapsed time  
    time_text = MAIN_FONT.render(f"Time: {game_info.get_level_time()}s", 1, (255, 255, 255))   
    win.blit(time_text, (10, HEIGHT - time_text.get_height() - 45))# Displaying on the screen
 # Adding to the game window text about player car velocity    
    vel_text = MAIN_FONT.render(f"Vel: {round(player_car.vel, 1)}px/s", 1, (255, 255, 255))   
    win.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 10))# Displaying on the screen
        
    player_car.draw(win)
    computer_car.draw(win)
    pygame.display.update()
# Defining functiOn that moves the car by pressing the keyboard
def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False
#Rotate left when "LEFT ARROW" key is pressed 
    if keys[pygame.K_LEFT]:
        player_car.rotate(left=True)
# Rotate right when "RIGHT ARROW" key is pressed
    if keys[pygame.K_RIGHT]:
        player_car.rotate(right=True)
# Move forward when "UP ARROW" key is pressed
    if keys[pygame.K_UP]:
        moved = True
        player_car.move_forward()
# Move backwards when "DOWN" key is pressed
    if keys[pygame.K_DOWN]:
        moved = True
        player_car.move_backward()
# If we stop pressing the up arrow key, reduce the speed.
    if not moved:
        player_car.reduce_speed()
        
# Function that is checking if the cars collided with the track border / finish flag on track
def handle_collision(player_car, computer_car, game_info):
    if player_car.collide(TRACK_BORDER_MASK) != None:
        print("collision!")
        player_car.bounce()
#Checing if the computer car passes the finish line          
    computer_finish_poi_collide = computer_car.collide(FINISH_MASK, *FINISH_POSITION)
    if computer_finish_poi_collide != None:
        blit_text_center(WIN, MAIN_FONT, "You lost!")
        pygame.display.update()
        pygame.time.wait(5000)#Delaying the game with 5s before you can restart the game
        game_info.reset()
        player_car.reset()
        computer_car.reset()
#Checing if the player car passes the finish line    
    player_finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION) 
    if player_finish_poi_collide != None:
        if player_finish_poi_collide[1] == 0:#Check if player car passes the finish line from above the flag
            player_car.bounce() # Bounce the car back if the player car tries to pass the finish flag form above
            print(player_finish_poi_collide)
        else: #Moving on with the game/levels.
            game_info.next_level()#Incrementing the game level
            player_car.reset()#Reseting the player car
            computer_car.next_level(game_info.level)#Reseting the computer car and increases its speed

run = True
# Setting up a clock that makes sure the window will not run faster than a certain FPS
clock = pygame.time.Clock()
# List that contains images to be drawn and its positions
images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]
player_car = PlayerCar(4, 4)
computer_car = ComputerCar(2, 4, PATH)
game_info = GameInfo()

# Main event loop. Runs until we quit the game or the game ends.
while run:
# Method that makes sure the while loop will not run faster than "FPS" constant
    clock.tick(FPS)
# Calling the draw function   
    draw(WIN, images, player_car, computer_car, game_info)
# Loop that waits for the level to start, once it started user has to press any key to start
    while not game_info.started:
        blit_text_center(WIN, MAIN_FONT, f"Press any key to start level {game_info.level}!")
# Methon that is needed to show on the screen what we draw
        pygame.display.update()
# Loops through the events in the game
        for event in pygame.event.get():
# Check if user closed the game window
            if event.type == pygame.QUIT:
                pygame.quit()
                break
# Defining the computer car path points
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     pos = pygame.mouse.get_pos()
            #     computer_car.path.append(pos)
            if event.type == pygame.KEYDOWN: #Event if we press any key down
                game_info.start_level()
# Loops through the events in the game            
    for event in pygame.event.get():
# Check if user closed the game window
        if event.type == pygame.QUIT:
            run = False
            break
            
    move_player(player_car)
    computer_car.move()
    handle_collision(player_car, computer_car, game_info)
    
    if game_info.game_finished():
        blit_text_center(WIN, MAIN_FONT, "You win!")
        pygame.time.wait(5000)
        game_info.reset()
        computer_car.reset()
print(computer_car.path)
# Event that is closing the window  
pygame.quit()
