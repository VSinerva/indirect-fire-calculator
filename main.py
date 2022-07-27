class Calculator:
    def __init__(self):
        self._target_coords = (0,0)
        self._observer_coords = (0,0)
        self._firing_position_coords = (0,0)

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

                if easting < 0 or northing < 0:
                    raise ValueError

                return (easting, northing)
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
            coords_str = input(f"{pos_name} coordinates ('E' to Exit): ")
            self._check_exit(coords_str)
            coords = self._str_to_coords(coords_str)
        return coords

    def get_starting_values(self):
        action_str = "_"
        while action_str != "":
            confirm_str = "DATA ENTERED"
            print()
            print(confirm_str)
            print("-"*len(confirm_str))
            print(f"Target: {self._target_coords[0]} {self._target_coords[1]}")
            print(f"Observer: {self._observer_coords[0]} {self._observer_coords[1]}")
            print(f"Firing position: {self._firing_position_coords[0]} {self._firing_position_coords[1]}")
            print()

            while True:
                action_str = input("'T', 'O' or 'F' to re-enter specific value.\n'Enter' to continue. 'E' to Exit:")
                self._check_exit(action_str)
                if action_str.upper() == "T":
                    self._target_coords = self._get_coordinates("Target")
                    break
                if action_str.upper() == "O":
                    self._observer_coords = self._get_coordinates("Observer")
                    break
                if action_str.upper() == "F":
                    self._firing_position_coords = self._get_coordinates("Firing position")
                    break
                if action_str.upper() == "":
                    break

    def firing_values(self):
        pass

    def update_firing_values(self):
        pass

calc = Calculator()
while True:
    calc.get_starting_values()
    calc.firing_values()
    calc.update_firing_values()
