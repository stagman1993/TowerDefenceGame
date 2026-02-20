import pygame as pg

class Enemy():
    def __init__(self, waypoints):
        self.waypoints = waypoints
        self.pos = pg.Vector2(waypoints[0])
        self.target_waypoint = 1
        self.speed = 5
        self.color = None

    def update(self):
        self.move()

    def move(self):
        if self.target_waypoint < len(self.waypoints):
            self.target = pg.Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            # enemy has reached the end of the path
            self.kill()

            # calculate distance to target
        dist = self.movement.length()
        # check if remaining distance is greater than the enemy speed
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

    def kill(self):
        self.pos = pg.Vector2(self.waypoints[0])
        self.target_waypoint = 0

class BlueEnemy(Enemy):
    def __init__(self, waypoints):
        super().__init__(waypoints)
        self.color = ("Blue")