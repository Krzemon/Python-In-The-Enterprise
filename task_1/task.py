import time
import os 
import random
import logging

class Car:    
    def __init__(self):
        self.wheel_angle = 0   # start angle
        self.speed = 0         # start speed
        self.time = 0          # time from start

    def update_speed(self, change):
        self.speed = max(0, min(100, self.speed + change))

    def update_wheel_angle(self, angle):
        self.wheel_angle = angle

    def apply_event(self, event):
        if event == 'obstacle':
            self.update_speed(-20)
            self.update_wheel_angle(random.choice([-45, 45]))
        elif event == 'turn_left':
            self.update_wheel_angle(-30)
            self.update_speed(-5)
        elif event == 'turn_right':
            self.update_wheel_angle(30)
            self.update_speed(-5)
        elif event == 'accelerate':
            self.update_speed(10)
            self.update_wheel_angle(0)
        elif event == 'stop':
            self.update_speed(-self.speed)
            self.update_wheel_angle(0)
        else:
            logging.warning("Unknown event")
        return self.speed, self.wheel_angle
    
    def __str__(self):
        return f"Speed: {self.speed} km/h, Wheel Angle: {self.wheel_angle}°, Time: {self.time}s"


class Environment:
    def __init__(self):
        self.events = [
            ('obstacle', 3),
            ('turn_left', 2),
            ('turn_right', 2),
            ('accelerate', 4),
            ('stop', 5)
        ]
    def generate_event(self):
            event, duration = random.choice(self.events)
            duration = max(1, int(random.gauss(duration, 1)))
            return event, duration

class CarSimulation:
    def __init__(self, car, environment):
        self.car = car
        self.environment = environment

    def simulate(self):
        while True:
            event, duration = self.environment.generate_event()
            self.car.time += duration
            speed, angle = self.car.apply_event(event)
            logging.info(
                f"Event: {event} | Duration: {duration}s | Speed: {speed} km/h | Angle: {angle}°"
            )
            yield speed, angle, self.car.time  # generator returns the car's state at each step

# function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

if __name__ == "__main__":
    car = Car()
    environment = Environment()
    simulation = CarSimulation(car, environment)

    for state in simulation.simulate():
        logging.info(f"Car State: {car}")
        time.sleep(1)
        clear_screen()