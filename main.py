from os import system, name
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux
    else:
        _ = system('clear')

class Calculator:
    def __init__(self):
        self._max_precision = 10**5
        self.zero_values()

    def zero_values(self):
        self._target_entered = False
        self._target_coords = (0,0)
        self._target_pos = (0,0)

        self._observer_entered = False
        self._observer_coords = (0,0)
        self._observer_pos = (0,0)

        self._firing_position_entered = False
        self._firing_position_coords = (0,0)
        self._firing_position = (0,0)

        self._observer_az = 0
        self._observer_dist_to_target = 0

    def _check_exit(self, string):
        if string.upper() == "E":
            print("Shutting down...")
            exit()

    def _str_to_coords(self, string: str):
        str_len = len(string)

        try:
            if str_len == 0:
                return (0,0)
            if str_len % 2 == 0:
                easting_str = string[0:str_len//2]
                easting = int(easting_str)

                northing_str = string[str_len//2:str_len]
                northing = int(northing_str)

                if 0 <= easting < self._max_precision and 0<= northing < self._max_precision:
                    return (easting, northing)
                raise ValueError
            else:
                raise ValueError
        except ValueError:
            print("Enter valid coordinates!")
            print()

    def _coords_to_meters(self, coords):
        pass

    def _get_coordinates(self, pos_name: str):
        coords = None
        while not coords:
            coords_str = input(f"{pos_name} coordinates: ")
            coords = self._str_to_coords(coords_str)
        return coords

    def get_starting_values(self):
        self.zero_values()
        action_str = "_"
        confirm_str = "DATA ENTERED"
        while action_str != "":
            clear()
            print(confirm_str)
            print("-"*len(confirm_str))
            print(f"Target:\t\t{self._target_coords[0]} {self._target_coords[1]}")
            print(f"Observer:\t{self._observer_coords[0]} {self._observer_coords[1]}")
            print(f"Firing pos:\t{self._firing_position_coords[0]} {self._firing_position_coords[1]}")
            print()

            action_str = input("Enter coordinates to fill next position.\n'T', 'O' or 'F' to change specific value.\n'Enter' to continue. 'E' to Exit: ")
            self._check_exit(action_str)
            if action_str.upper() == "T":
                self._target_coords = self._get_coordinates("Target")
                self._target_entered = True
            if action_str.upper() == "O":
                self._observer_coords = self._get_coordinates("Observer")
                self._observer_entered = True
            if action_str.upper() == "F":
                self._firing_position_coords = self._get_coordinates("Firing position")
                self._firing_position_entered = True

            try:
                int(action_str)
                if not self._target_entered:
                    self._target_coords = self._str_to_coords(action_str)
                    self._target_entered = True
                elif not self._observer_entered:
                    self._observer_coords = self._str_to_coords(action_str)
                    self._observer_entered = True
                elif not self._firing_position_entered:
                    self._firing_position_coords = self._str_to_coords(action_str)
                    self._firing_position_entered = True
            except ValueError:
                pass

    def firing_values(self):
        pass

    def update_firing_values(self):
        pass

calc = Calculator()
while True:
    calc.get_starting_values()
    calc.firing_values()
    calc.update_firing_values()
