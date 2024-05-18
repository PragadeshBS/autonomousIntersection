import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pygame
import sys
import os
from enum import Enum

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
colors = [Color.WHITE, Color.BLACK, Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW, Color.CYAN, Color.MAGENTA, Color.ORANGE, Color.PURPLE, Color.TEAL, Color.PINK, Color.LIME, Color.BROWN, Color.GOLD, Color.SILVER, Color.GRAY, Color.MAROON, Color.NAVY, Color.OLIVE]

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
            elif col.startswith('NW'):
                cars_way.append({"car":col,"way":"NW","points":self.df[col]})

        # Given points
        points1 = [(x, 0) for x in range(-50, 1)]

        points2 = [(x, 0) for x in range(51)]

        points3 = [(0, x) for x in range(-50, 1)]

        points4 = [(1, -x) for x in range(51)]

        points5 = [(1, x) for x in range(41)]

        points6 = [(x, 1) for x in range(-50, 1)]

        for car in cars_way:
            result=[]
            with open("simulation_logs.log", "w") as f:
                for point in car['points']:
                    if str(point)!='nan':
                        point=eval(str(point))
                        f.write(str(point) + "\n")
                        if (point[0]>=-50 and point[0]<0) and point[1]==0:
                            result.extend(self.scale_points([point], points1, [(-50, 0), (0, 0)], [(300, 200), (600, 200)])) #x 
                            f.write("case 1" +"\n")
                        elif point[0]==1 and (point[1]>=-50 and point[1]<0):
                            result.extend(self.scale_points([point],points4, [(1, -50), (1, 0)], [(605, 500), (605, 200)]))
                            f.write("case 2" + "\n")
                        elif point[0] == 1 and (point[1]>=0 and point[1]<=40):
                            result.extend(self.scale_points([point], points5, [(1, 0), (1, 40)], [(605, 200), (605, -400)]))
                            f.write("case 3" + "\n")
                        elif (point[0]>0 and point[0]<=50):
                            result.extend(self.scale_points([point],points2, [(0, 0), (50, 0)], [(600, 200), (900, 200)])) #y
                            f.write("case 4" + "\n")
                        elif point[0]==0 and (point[1]>=-50 and point[1]<0):
                            result.extend(self.scale_points([point],points3, [(0, -50), (0, 0)], [(600, 500), (600, 200)]))
                            f.write("case 5" + "\n")
                        elif (point[0]>=-50 and point[0]<0) and point[1]==1:
                            result.extend(self.scale_points([point], points6, [(-50, 1), (0, 1)], [(300, 200), (600, 200)]))
            if car['way']=="SE":
                car["points"]=[(x,y+10) for x,y in result]
            elif car['way']=="WS":
                car["points"]=[(x+10,y) for x,y in result]
            elif car['way']=='NW':
                car['points']=[(x,y+10) for x,y in result]
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

intersection_points = [ (600, 500), (300, 200), (600, 200), (900, 200), (600, 10)]

scaled_R = PointsDataProcessor(os.path.join(os.curdir, 'data', file_name)).execute()

car_paths = [scaled_R[i]['points'] for i in range(len(scaled_R))]

cars = [Car(car_paths[i], Color.NAVY.value) for i in range(len(car_paths))]

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

    # Draw intersection points
    i=1
    for point in intersection_points:
        pygame.draw.circle(screen, colors[i].value, point, 10)
        i += 1

    pygame.display.flip()
    clock.tick(75)

# Quit Pygame
pygame.quit()
sys.exit()
