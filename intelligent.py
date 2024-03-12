import random
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

class Edge:
    def __init__(self, start: Tuple[float, float], end: Tuple[float, float], speed: float) -> None:
        self.start: Tuple[float, float] = start
        self.end: Tuple[float, float] = end
        self.speed: float = speed

    def is_point_on_edge(self, point: Tuple[float, float]) -> bool:
        return point[0] >= self.start[0] and point[0] <= self.end[0] and point[1] >= self.start[1] and point[1] <= self.end[1]
    
    def set_speed(self, speed: float) -> None:
        self.speed = speed

class Node:
    def __init__(self, position: Tuple[float, float]) -> None:
        self.position: Tuple[float, float] = position

    def get_position(self) -> Tuple[float, float]:
        return self.position

class Road:
    def __init__(self, name: str, positions: List[Tuple[float, float]], node_positions: List[Tuple[float, float]], edges: List[Tuple[Tuple[float, float], Tuple[float, float]]]):
        self.name: str = name
        self.positions: List[Tuple[float, float]] = positions
        self.node_positions: List[Node] = self.get_nodes(node_positions)
        self.default_speed: float = 1
        self.edges: List[Edge] = self.get_edges(edges)

    def get_nodes(self, node_positions: List[Tuple[float, float]]) -> List[Node]:
        node_objects = []
        for position in node_positions:
            node_objects.append(Node(position))
        return node_objects

    def get_edges(self, edges: List[Tuple[Tuple[float, float], Tuple[float, float]]]) -> List[Edge]:
        edge_objects = []
        for edge in edges:
            edge_objects.append(Edge(edge[0], edge[1], self.default_speed))
        return edge_objects

    def is_at_intersection(self, position: Tuple[float, float]) -> bool:
        return self.is_at_location(position, (0, 0))
    
    def is_at_location(self, position: Tuple[float, float], location: Tuple[float, float]) -> bool:
        return position[0] < location[0] + 1 and position[0] > location[0] - 1 and position[1] < location[1] + 1 and position[1] > location[1] - 1
    
    def is_at_node(self, position: Tuple[float, float]) -> bool:
        for node in self.node_positions:
            if self.is_at_location(position, node.get_position()):
                return True
        return False

    def get_speed(self, position: Tuple[float, float]) -> float:
        for edge in self.edges:
            if edge.is_point_on_edge(position):
                return edge.speed
        return self.default_speed
    
    def get_edge(self, position: Tuple[float, float]) -> Edge:
        for edge in self.edges:
            if edge.is_point_on_edge(position):
                return edge
        print("No edge found for position: ", position)
        return self.edges[0]
    
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
        self.visited_nodes: List[Node] = []

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

class QLearningAgent:

    def __init__(self, actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.Q = {}
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_q_value(self, state, action):
        return self.Q.get((state, action), 0.0)

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)
        else:
            return max(self.actions, key=lambda a: self.get_q_value(state, a))

    def learn(self, state, action, reward, next_state):
        old_value = self.get_q_value(state, action)
        next_max = max([self.get_q_value(next_state, a) for a in self.actions])
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        self.Q[(state, action)] = new_value

class Controller:
    def __init__(self, cars: List[Car], roads: List[Road]):
        self.cars: List[Car] = cars
        self.roads: List[Road] = roads
        self.interection_busy_times: List[Tuple[float, float, Car]] = []
        self.current_time: int = 0
        self.speed_reduction: float = 0.07
    
    def print_status(self):
        for car in self.cars:
            print(f"{car.name} is at {car.position}", end="  | ")
        print()

    def check_if_at_node(self, car: Car):
        return car.road.is_at_node(car.position)

    def calculate_time_to_intersection(self, car: Car):
        print(f"Calculating time to intersection for {car.name} with speed {car.speed}")
        return self.current_time + ((abs(car.position[0]) + abs(car.position[1])) / car.road.get_speed(car.position))

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
            print(f"{car.name} has passed the intersection")
        permitted_speed = car.road.get_speed(car.position)
        if car.direction == Directions.EAST:
            car.position = (car.position[0] + permitted_speed, car.position[1])
        elif car.direction == Directions.WEST:
            car.position = (car.position[0] - permitted_speed, car.position[1])
        elif car.direction == Directions.NORTH:
            car.position = (car.position[0], car.position[1] + permitted_speed)
        else:
            car.position = (car.position[0], car.position[1] - permitted_speed)
        if self.check_if_at_node(car):
            time_to_intersection = self.calculate_time_to_intersection(car)
            print(f"{car.name} is at {car.position}. Time to intersection: {time_to_intersection}")
            if self.is_intersection_blocked(time_to_intersection, car):
                car.road.get_edge(car.position).speed -= self.speed_reduction
                car.speed = car.road.get_speed(car.position)
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

class RLController(Controller):

    def __init__(self, cars, roads):
        super().__init__(cars, roads)
        self.q_agent = QLearningAgent(actions=['keep', 'reduce_speed'])

    def is_intersection_blocked(self, time_to_intersection, car):
        if super().is_intersection_blocked(time_to_intersection, car):
            if self.q_agent.choose_action(car.position) == 'reduce_speed':
                car.road.get_edge(car.position).speed -= self.speed_reduction
                car.speed = car.road.get_speed(car.position)
                time_to_intersection = self.calculate_time_to_intersection(car)
                print(f"Reducing speed. New time to intersection: {time_to_intersection}")
            return True
        return False

    def simulate_intersection(self):
        while True:
            if len(self.cars) == 0:
                print("All cars have passed the intersection.")
                print("Time taken: ", self.current_time, " units.")
                return

            for car in self.cars:
                if car.passed_intersection:
                    self.q_agent.learn(car.position, 'keep', 0, None)
                    continue

                state = car.position
                action = self.q_agent.choose_action(state)
                next_state = car.road.get_edge(car.position).end
                reward = 0  # Define your own reward function based on the scenario

                self.q_agent.learn(state, action, reward, next_state)

                time_to_intersection = self.calculate_time_to_intersection(car)
                if action == 'reduce_speed':
                    car.road.get_edge(car.position).speed -= self.speed_reduction
                    car.speed = car.road.get_speed(car.position)
                    time_to_intersection = self.calculate_time_to_intersection(car)
                    print(f"Reducing speed. New time to intersection: {time_to_intersection}")

                self.interection_busy_times.append((time_to_intersection, time_to_intersection + 2, car))
                self.move_car(car)
                self.print_status()

                for other_car in self.cars:
                    if car.is_at_intersection() and other_car.is_at_intersection() and car != other_car:
                        print("Collision detected! Simulation stopped.")
                        return

            time.sleep(0.1)
            self.current_time += 1

west_to_east_road = Road("West-East", [(x, 0) for x in range(-50, 51)], [(-40, 0), (-20, 0)], [
    ((-40, 0), (-20, 0)),
    ((-20, 0), (0, 0)),
])
east_to_west_road = Road("East-West", [(x, -1) for x in range(50, -51, -1)], [(0, 0)], [])
north_to_south_road = Road("North-South", [(1, y) for y in range(0, -51, -1)], [(0, 0)], [])
south_to_north_road = Road("South-North", [(0, y) for y in range(-50, 1)], [(0, -40), (0, -20)], [
    ((0, -40), (0, -20)),
    ((0, -20), (0, 0)),
])

car1 = Car("Car1", (-50, 0), west_to_east_road, Locations.WEST, Locations.SOUTH)
car2 = Car("Car2", (0,-50), south_to_north_road, Locations.SOUTH, Locations.EAST)


def main():
    controller = RLController([car1, car2], [west_to_east_road, east_to_west_road, north_to_south_road, south_to_north_road])
    controller.simulate_intersection()

if __name__ == "__main__":
    main()
