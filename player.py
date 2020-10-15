import math


class Player:
    def __init__(self, name, fuel=10, actions=[]):
        self.name = name
        self.fuel = fuel
        self.actions = actions
        self.position = [0, 0]
        self.current_action = ""
        self.complete = False
        self.dead = False
        self.direction = [1, 0]
        self.facing = 0
        self.docked = False
        self.finished = False
        self.points = 0
        self.total_fuel_used = fuel

    def set_position(self, new_position):
        self.position = new_position

    def move(self, game_map, any_finished):
        if self.dead or self.finished:
            return

        if self.current_action == "":
            if len(self.actions) > 0 and self.fuel > 0:
                self.current_action = self.actions.pop(0)

                # As long as we are not refueling, every new move costs us 1 fuel
                if "refuel" not in self.current_action:
                    self.fuel = self.fuel - 1
            else:
                self.complete = True

        # handle forward
        if "forward" in self.current_action:
            print(self.name, "is Going forward!")
            self.position[0] = self.position[0] + self.direction[0]
            self.position[1] = self.position[1] + self.direction[1]
            val = int(self.current_action.replace("forward ", ""))
            val = val - 1

            # If we have more forward moves, update current action
            # Otherwise, clear the current action so we can pick a new action next move
            if val > 0:
                self.current_action = "forward " + str(val)
            else:
                self.current_action = ""

            if self.docked:
                self.docked = False

            if game_map[self.position[0]][self.position[1]] in "Aa-":
                self.dead = True
                self.complete = True
                print(self.name, " crashed!!!")

        # handle turn left
        if "turn left" in self.current_action:
            print(self.name, "is Turning left!")
            self.facing = self.facing - 90
            if self.facing == -360:
                self.facing = 0
            self.direction[0] = int(math.cos(math.radians(self.facing)))
            self.direction[1] = int(math.sin(math.radians(self.facing)))

            # Clear the action since we're done turning
            self.current_action = ""

        # handle turn right
        if "turn right" in self.current_action:
            print(self.name, "is Turning right!")
            self.facing = self.facing + 90
            if self.facing == 360:
                self.facing = 0
            self.direction[0] = int(math.cos(math.radians(self.facing)))
            self.direction[1] = int(math.sin(math.radians(self.facing)))

            # Clear the action since we're done turning
            self.current_action = ""

        # handle dock
        if "dock" in self.current_action:
            self.current_action = ""
            if self.docked:
                print(self.name, "is already docked!")
            if game_map[self.position[0]][self.position[1]] in "123456789":
                print(self.name, "is Docking!")
                self.docked = True
            else:
                print(self.name, "attempted to dock with a dust cloud!?")

        # handle refuel
        if "refuel" in self.current_action:
            if self.docked:
                print(self.name, "is Refueling!")
                val = int(self.current_action.replace("refuel ", ""))
                if val >= 20:
                    self.points = self.points - 10
                self.fuel = self.fuel + val
                self.total_fuel_used = self.total_fuel_used + val  # even if they don't use it, they took it
                print(self.name, "Refueled: ", val)
            else:
                print(self.name, "tried to refuel in empty space!?")

            self.current_action = ""

        # Ran out of fuel, spinning forever
        if self.no_fuel():
            self.facing = self.facing + 90
        # ran out of moves, stuck
        elif self.no_moves():
            self.facing = 45

        if game_map[self.position[0]][self.position[1]] in "5":
            print(self.name, "Finished and earned 20 points!")
            self.finished = True
            self.complete = True
            self.points = self.points + 20
            if not any_finished:
                print(self.name, "Was one of the first ones and got 10 more points!")
                self.points = self.points + 10

    def is_dead(self):
        return self.dead

    def no_fuel(self):
        return self.fuel < 1

    def no_moves(self):
        return self.current_action == "" and len(self.actions) == 0

    def debug_print(self):
        print("Debug Print Player:", self.current_action, self.position, self.facing, self.direction, self.fuel)
