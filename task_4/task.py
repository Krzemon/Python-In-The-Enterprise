import unittest
from lab01 import Environment, Action, Car


class TestCarSimulation(unittest.TestCase):
    # 1
    def setUp(self):
        self.environment = Environment()
        self.car = Car(self.environment)
    # 2
    def test_start_engine_and_drive(self):
        self.car.send_action(Action("start the engine"))
        self.car.send_action(Action("drive"))
        self.assertTrue(self.environment.on_the_road)
        self.assertGreater(self.environment.speed, 0)
    # 3
    def test_accelerate_and_brake(self):
        self.environment.handle_action(Action("accelerate", duration=2))
        initial_speed = self.environment.speed
        self.environment.handle_action(Action("brake", duration=2))
        self.assertLess(self.environment.speed, initial_speed)
    # 4
    def test_enter_and_exit_highway(self):
        self.environment.handle_action(Action("highway"))
        self.assertTrue(self.environment.on_the_highway)
        self.environment.handle_action(Action("exit highway"))
        self.assertFalse(self.environment.on_the_highway)
    # 5
    def test_overtake_and_truck(self):
        self.environment.handle_action(Action("highway"))
        self.environment.handle_action(Action("overtake"))
        self.assertEqual(self.environment.speed, self.environment.OVERTAKE_SPEED_HIGHWAY)
        self.environment.handle_action(Action("truck"))
        self.assertEqual(self.environment.speed, self.environment.TRUCK_SPEED_HIGHWAY)
    # 6
    def test_stop_car(self):
        self.environment.drive()
        self.environment.stop()
        self.assertEqual(self.environment.speed, 0)
        self.assertFalse(self.environment.on_the_road)
    # 7
    def test_truck_on_highway(self):
        self.environment.highway()
        self.environment.truck()
        self.assertEqual(self.environment.speed, Environment.TRUCK_SPEED_HIGHWAY)
    # 8
    def test_truck_on_road(self):
        self.environment.drive()
        self.environment.truck()
        self.assertEqual(self.environment.speed, Environment.TRUCK_SPEED_ROAD)
    # 9
    def test_status_on_road(self):
        self.environment.drive()
        with self.assertLogs(level='INFO') as log:
            self.environment.status()
            self.assertIn("Car is on the road.", log.output[-1])
    # 10
    def test_brake(self):
        self.environment.drive()
        self.environment.accelerate(5)
        initial_speed = self.environment.speed
        self.environment.brake(3)
        self.assertLess(self.environment.speed, initial_speed)

if __name__ == '__main__':
    unittest.main()
