import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pygame
import sys
import os
from enum import Enum
import random

file_name = "car_positions.xlsx"

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1100, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Movement")
font = pygame.font.Font(None, 36)

class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    TEAL = (0, 128, 128)
    PINK = (255, 192, 203)
    LIME = (0, 255, 0)
    BROWN = (165, 42, 42)
    GOLD = (255, 215, 0)
    SILVER = (192, 192, 192)
    GRAY = (128, 128, 128)
    MAROON = (128, 0, 0)
    NAVY = (0, 0, 128)
    OLIVE = (128, 128, 0)


# Define colors
colors = [
    (255, 255, 255),  # WHITE
    (0, 0, 0),        # BLACK
    (255, 0, 0),      # RED
    (0, 255, 0),      # GREEN
    (0, 0, 255),      # BLUE
    (255, 255, 0),    # YELLOW
    (0, 255, 255),    # CYAN
    (255, 0, 255),    # MAGENTA
    (255, 165, 0),    # ORANGE
    (128, 0, 128),    # PURPLE
    (0, 128, 128),    # TEAL
    (255, 192, 203),  # PINK
    (0, 255, 0),      # LIME
    (165, 42, 42),    # BROWN
    (255, 215, 0),    # GOLD
    (192, 192, 192),  # SILVER
    (128, 128, 128),  # GRAY
    (128, 0, 0),      # MAROON
    (0, 0, 128),      # NAVY
    (128, 128, 0)     # OLIVE
]

class PointsDataProcessor:
    def __init__(self, path):
        self.df=pd.read_excel(path)
        self.scaled_R=[]

    def scale_points(self, tpoints, points, original_range, target_range):
        """
        Scale points from the original range to the target range.
        """
        # Scale the points
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaler.fit(points)
        scaled_points = scaler.transform(tpoints)

        # Map the scaled points to the target range
        scaled_x = [scaled_point[0] * (target_range[1][0] - target_range[0][0]) + target_range[0][0] for scaled_point in scaled_points]
        scaled_y = [scaled_point[1] * (target_range[1][1] - target_range[0][1]) + target_range[0][1] for scaled_point in scaled_points]

        # Return the scaled points
        return [(scaled_x[i], scaled_y[i]) for i in range(len(scaled_points))]

    def process_data(self):
        cars_way=[]
        for col in self.df.columns:
            if col.startswith('SE'):
                cars_way.append({"car":col,"way":"SE","points":self.df[col]})
            elif col.startswith('WS'):
                cars_way.append({"car":col,"way":"WS","points":self.df[col]})

        # Given points
        points1 = [
            (-50, 0), (-49, 0), (-48, 0), (-47, 0), (-46, 0), (-45, 0), (-44, 0), (-43, 0), (-42, 0), (-41, 0),
            (-40, 0), (-39, 0), (-38, 0), (-37, 0), (-36, 0), (-35, 0), (-34, 0), (-33, 0), (-32, 0), (-31, 0),
            (-30, 0), (-29, 0), (-28, 0), (-27, 0), (-26, 0), (-25, 0), (-24, 0), (-23, 0), (-22, 0), (-21, 0),
            (-20, 0), (-19, 0), (-18, 0), (-17, 0), (-16, 0), (-15, 0), (-14, 0), (-13, 0), (-12, 0), (-11, 0),
            (-10, 0), (-9, 0), (-8, 0), (-7, 0), (-6, 0), (-5, 0), (-4, 0), (-3, 0), (-2, 0), (-1, 0), (0, 0)
        ]

        points2 = [
            (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0),
            (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0), (17, 0), (18, 0), (19, 0),
            (20, 0), (21, 0), (22, 0), (23, 0), (24, 0), (25, 0), (26, 0), (27, 0), (28, 0), (29, 0),
            (30, 0), (31, 0), (32, 0), (33, 0), (34, 0), (35, 0), (36, 0), (37, 0), (38, 0), (39, 0),
            (40, 0), (41, 0), (42, 0), (43, 0), (44, 0), (45, 0), (46, 0), (47, 0), (48, 0), (49, 0), (50, 0)
        ]

        points3 = [
            (0, -50), (0, -49), (0, -48), (0, -47), (0, -46), (0, -45), (0, -44), (0, -43), (0, -42), (0, -41),
            (0, -40), (0, -39), (0, -38), (0, -37), (0, -36), (0, -35), (0, -34), (0, -33), (0, -32), (0, -31),
            (0, -30), (0, -29), (0, -28), (0, -27), (0, -26), (0, -25), (0, -24), (0, -23), (0, -22), (0, -21),
            (0, -20), (0, -19), (0, -18), (0, -17), (0, -16), (0, -15), (0, -14), (0, -13), (0, -12), (0, -11),
            (0, -10), (0, -9), (0, -8), (0, -7), (0, -6), (0, -5), (0, -4), (0, -3), (0, -2), (0, -1), (0, 0)
        ]

        points4 = [(1, -x) for x in range(51)]

        for car in cars_way:
            result=[]
            for point in car['points']:
                if str(point)!='nan':
                    point=eval(str(point))
                    if (point[0]>=-50 and point[0]<0) and point[1]==0:
                        result.extend(self.scale_points([point], points1, [(-50, 0), (0, 0)], [(300, 200), (600, 200)])) #x 
                    elif point[0]==1 and (point[1]>=-50 and point[1]<0):
                        result.extend(self.scale_points([point],points4, [(1, -50), (1, 0)], [(605, 500), (605, 200)]))
                    elif (point[0]>0 and point[0]<=50):
                        result.extend(self.scale_points([point],points2, [(0, 0), (50, 0)], [(600, 200), (900, 200)])) #y
                    elif point[0]==0 and (point[1]>=-50 and point[1]<0):
                        result.extend(self.scale_points([point],points3, [(0, -50), (0, 0)], [(600, 500), (600, 200)]))
            if car['way']=="SE":
                car["points"]=[(x,y+10) for x,y in result]
            elif car['way']=="WS":
                car["points"]=[(x+10,y) for x,y in result]
            self.scaled_R.append(car)

        # print(self.scaled_R)
    
    def get_scaled_data(self):
        return self.scaled_R
    
    def execute(self):
        self.process_data()
        return self.get_scaled_data()

class Car:
    def __init__(self, path, color=Color.RED.value):
        self.path = path
        self.current_point = 0
        self.x, self.y = self.path[self.current_point]
        self.color = color

    def move(self):
        if self.current_point < len(self.path) - 1:
            self.current_point += 1
            self.x, self.y = self.path[self.current_point]

    def get_position(self):
        return self.x, self.y
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x - 10, self.y - 10, 10, 10))

intersection_points = [ (600, 500), (300, 200), (600, 200), (900, 200)]

scaled_R = PointsDataProcessor(os.path.join(os.curdir, 'simulation/data', file_name)).execute()
car_path_1 = scaled_R[1]['points']
car_path_2 = scaled_R[0]['points']
car_path_3 = scaled_R[2]['points']
car_path_4 = scaled_R[3]['points']
car_path_5 = scaled_R[4]['points']
car_path_6 = scaled_R[5]['points']

# Create car
car1 = Car(car_path_1, Color.RED.value)
car2 = Car(car_path_2, Color.GREEN.value)
car3 = Car(car_path_3, Color.NAVY.value)
car4 = Car(car_path_4, Color.ORANGE.value)
car5 = Car(car_path_5, Color.BROWN.value)
car6 = Car(car_path_6, Color.GOLD.value)

# cars = [car1, car2]
cars = [car1, car2, car3, car4, car5, car6]

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(Color.WHITE.value)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move and draw car
    for car in cars:
        car.move()
        car.draw()
    # cap_car_1 = "Car A : " + str(car1.get_position())
    # cap_car_2="Car B : " + str(car2.get_position())
    
    # text_1= font.render(cap_car_1, True, (0, 0, 0))
    # text_2= font.render(cap_car_2, True, (0, 0, 0))
    
    # text_rect_1 = text_1.get_rect(topleft=(20, 20))
    # text_rect_2 = text_2.get_rect(topleft=(20, 40))
    
    # screen.blit(text_1, text_rect_1)
    # screen.blit(text_2, text_rect_2)

    # Draw intersection points
    i=1
    for point in intersection_points:
        pygame.draw.circle(screen, colors[i], point, 10)
        i += 1

    pygame.display.flip()
    clock.tick(20)

# Quit Pygame
pygame.quit()
sys.exit()
