from os import system, name
from math import sqrt, atan2, pi

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
        self._circle_divisions = 360 
        self.zero_values()

    def zero_values(self):
        self._target_entered = False
        self._target_coords = (0,0)

        self._observer_entered = False
        self._observer_coords = (0,0)

        self._firing_position_entered = False
        self._firing_position_coords = (0,0)

    def _check_exit(self, string):
        if string.upper() == "E":
            print("Shutting down...")
            exit()

    def _str_to_coords(self, string: str):
        str_len = len(string)

        try:
            if str_len % 2 == 0 and str_len > 0:
                values = []
                for substring in [string[0:str_len//2], string[str_len//2:str_len]]:
                    coord = 0
                    counter = self._max_precision
                    for c in substring:
                        if counter > 1:
                            counter = counter // 10
                            coord *= 10
                            coord += int(c)
                    while counter > 1:
                        counter = counter // 10
                        coord*= 10
                    values.append(coord)

                easting = values[0]
                northing = values[1]

                if 0 <= easting < self._max_precision and 0<= northing < self._max_precision:
                    return (easting, northing)
                raise ValueError
            else:
                raise ValueError
        except ValueError:
            print("Enter valid coordinates!")
            print()

    def _distance_between(self, coords1, coords2):
        e_dist = coords1[0] - coords2[0]
        n_dist = coords1[1] - coords2[1]
        return sqrt(e_dist**2 + n_dist**2)

    def _azimuth(self, coords1, coords2):
        pos1e, pos1n = coords1
        pos2e, pos2n = coords2

        d_e = pos2e-pos1e
        d_n = pos2n-pos1n

        if d_e == 0:
            return 0 if d_n > 0 else self._circle_divisions / 2
        if d_n == 0:
            return self._circle_divisions / 4 if d_e > 0 else 3*self._circle_divisions / 4

        az = atan2(d_e, d_n)/(2*pi) * self._circle_divisions 
        if az < 0:
            az += self._circle_divisions
        return az 

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
            print(f"Target:\t\t{self._target_coords[0]:05d} {self._target_coords[1]:05d}")
            print(f"Observer:\t{self._observer_coords[0]:05d} {self._observer_coords[1]:05d}")
            print(f"Firing pos:\t{self._firing_position_coords[0]:05d} {self._firing_position_coords[1]:05d}")
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
                if self._str_to_coords(action_str):
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
        print()
        solution_str = "FIRING DATA"
        print(solution_str)
        print("-"*len(solution_str))
        print(f"Dist: {self._distance_between(self._firing_position_coords, self._target_coords):.0f}m")
        print(f"Az: {self._azimuth(self._firing_position_coords, self._target_coords)}")
        print()

    def update_firing_values(self):
        pass

calc = Calculator()
while True:
    calc.get_starting_values()
    try:
        calc.firing_values()
        calc.update_firing_values()
    except ValueError:
        clear()
        calc.zero_values()
    break
