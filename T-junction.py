import time
from enum import Enum
from typing import Tuple, List

class Locations(Enum):
    EAST = "East"
    WEST = "West"
    SOUTH = "South"

class Directions(Enum):
    NORTH = "North"
    SOUTH = "South"
    EAST = "East"
    WEST = "West"

class Road:
    def __init__(self, name: str, positions: List[Tuple[float, float]], node_positions: List[Tuple[float, float]]):
        self.name: str = name
        self.positions: List[Tuple[float, float]] = positions
        self.node_positions: List[Tuple[float, float]] = node_positions

    def is_at_intersection(self, position: Tuple[float, float]) -> bool:
        return self.is_at_location(position, (0, 0))
    
    def is_at_location(self, position: Tuple[float, float], location: Tuple[float, float]) -> bool:
        return position[0] <= location[0] + 1 and position[0] >= location[0] - 1 and position[1] <= location[1] + 1 and position[1] >= location[1] - 1
    
    def is_at_node(self, position: Tuple[float, float]) -> bool:
        for node in self.node_positions:
            if self.is_at_location(position, node):
                return True
        return False

class Car:
    def __init__(self, name: str, position: Tuple[int, int], road: Road, 
                 source: Locations, destination: Locations, speed: int = 1):
        self.name: str = name
        self.position: Tuple[float, float] = position
        self.road: Road = road
        self.source: Locations = source
        self.destination: Locations = destination
        self.direction: Directions = self.get_initial_direction()
        self.speed: float = speed
        self.visited_intersection: bool = False
        self.passed_intersection: bool = False

    def get_initial_direction(self) -> Directions:
        if self.source == Locations.EAST:
            return Directions.WEST
        elif self.source == Locations.WEST:
            return Directions.EAST
        elif self.source == Locations.SOUTH:
            return Directions.NORTH
        return Directions.SOUTH
    
    def is_at_intersection(self) -> bool:
        return self.road.is_at_intersection(self.position)
    
    def has_reached_destination(self) -> bool:
        if self.destination == Locations.EAST:
            return self.position[0] > 50
        elif self.destination == Locations.WEST:
            return self.position[0] < -50
        elif self.destination == Locations.SOUTH:
            return self.position[1] < -50
        return self.position[1] > 50

class Controller:
    def __init__(self, cars: List[Car], roads: List[Road]):
        self.cars: List[Car] = cars
        self.roads: List[Road] = roads
        self.interection_busy_times: List[Tuple[float, float, Car]] = []
        self.current_time: int = 0
        self.speed_reduction: float = 0.2
    
    def print_status(self):
        for car in self.cars:
            print(f"{car.name} is at {car.position}", end="  | ")
        print()

    def check_if_at_node(self, car: Car):
        return car.road.is_at_node(car.position)

    def calculate_time_to_intersection(self, car: Car):
        return self.current_time + ((abs(car.position[0]) + abs(car.position[1])) / car.speed)

    def is_intersection_blocked(self, time_to_intersection: float, car: Car):
        for busy_time in self.interection_busy_times:
            if time_to_intersection >= busy_time[0] and time_to_intersection <= busy_time[1] and busy_time[2] != car:
                print(f"{car.name} will reach the intersection at {time_to_intersection}")
                print(f"Intersection is blocked for {busy_time[2].name} from {busy_time[0]} to {busy_time[1]}.")
                print(f"{car.name} is reducing speed by {self.speed_reduction} units.")
                return True
        return False

    def move_car(self, car: Car):
        if car.has_reached_destination():
            print(f"{car.name} has reached its destination.")
            return
        if car.is_at_intersection():
            car.visited_intersection = True
            if car.destination == Locations.EAST:
                car.direction = Directions.EAST
                car.road = west_to_east_road
            elif car.destination == Locations.SOUTH:
                car.direction = Directions.SOUTH
                car.road = north_to_south_road
            elif car.destination == Locations.WEST:
                car.direction = Directions.WEST
                car.road = east_to_west_road
        elif car.visited_intersection and not car.passed_intersection:
            car.passed_intersection = True
            print(f"{car.name} has passed the intersection. Regaining speed.")

            car.speed += self.speed_reduction
        if car.direction == Directions.EAST:
            car.position = (car.position[0] + car.speed, car.position[1])
        elif car.direction == Directions.WEST:
            car.position = (car.position[0] - car.speed, car.position[1])
        elif car.direction == Directions.NORTH:
            car.position = (car.position[0], car.position[1] + car.speed)
        else:
            car.position = (car.position[0], car.position[1] - car.speed)
        if self.check_if_at_node(car):
            time_to_intersection = self.calculate_time_to_intersection(car)
            print(f"{car.name} is at {car.position}. Time to intersection: {time_to_intersection}")
            if self.is_intersection_blocked(time_to_intersection, car):
                car.speed -= self.speed_reduction
                time_to_intersection = self.calculate_time_to_intersection(car)
                print(f"Reducing speed. New time to intersection: {time_to_intersection}")
            self.interection_busy_times.append((time_to_intersection, time_to_intersection+2, car))


    def simulate_intersection(self):
        cars_passed_intersection = []
        while True:
            if len(self.cars) == 0:
                print("All cars have passed the intersection.")
                print("Time taken: ", self.current_time, " units.")
                return
            for car in self.cars:
                if car.passed_intersection:
                    cars_passed_intersection.append(car)
                    self.cars.remove(car)
                    continue
                self.move_car(car)

                self.print_status()

                # Check for collisions
                for other_car in self.cars:
                    if car.is_at_intersection() and other_car.is_at_intersection() and car != other_car:
                        print("Collision detected! Simulation stopped.")
                        return
            time.sleep(0.1)
            self.current_time += 1


west_to_east_road = Road("West-East", [(x, 0) for x in range(-50, 51)], [(-40, 0), (-20, 0)])
east_to_west_road = Road("East-West", [(x, -1) for x in range(50, -51, -1)], [(0, 0)])
north_to_south_road = Road("North-South", [(1, y) for y in range(0, -51, -1)], [(0, 0)])
south_to_north_road = Road("South-North", [(0, y) for y in range(-50, 1)], [(0, -40), (0, -20)])

car1 = Car("Car1", (-50, 0), west_to_east_road, Locations.WEST, Locations.SOUTH)
car2 = Car("Car2", (0,-50), south_to_north_road, Locations.SOUTH, Locations.EAST)

def main():
    controller = Controller([car1, car2], [west_to_east_road, east_to_west_road, north_to_south_road, south_to_north_road])
    controller.simulate_intersection()

if __name__ == "__main__":
    main()
