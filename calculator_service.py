from math import sqrt, atan2, pi

class CalculatorService:
    def __init__(self):
        self._max_coordinate = 10**5
        self._circle_divisions = 6200 
        self._coords = {}
        self._coords_set = {}
        self.zero_values()

    def zero_values(self):
        self._coords["mortar"] = (0, 0)
        self._coords["target"] = (0, 0)
        self._coords["observer"] = (0, 0)
        self._coords_set["mortar"] =  False
        self._coords_set["target"] = False
        self._coords_set["observer"] = False

    def set_coords(self, coordinate_string: str, pos_name: str):
        if pos_name not in self._coords:
            raise ValueError
        try:
            self._coords[pos_name] = self._str_to_coords(coordinate_string)
            self._coords_set[pos_name] = True
        except ValueError:
            raise ValueError

    def get_coords(self, pos_name: str):
        return self._coords[pos_name]

    def coords_set(self, pos_name: str):
        return self._coords_set[pos_name]

    def get_dist_to_target(self):
        return self._distance_between(self._coords["mortar"], self._coords["target"])

    def get_az_to_target(self):
        return self._azimuth(self._coords["mortar"], self._coords["target"])

    def _str_to_coords(self, string: str):
        try:
            if len(string) > 0:
                substrings = string.split(" ")
                if len(substrings) == 2:
                    values = []
                    for substring in substrings:
                        coord = 0
                        counter = self._max_coordinate
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

                    if 0 <= easting < self._max_coordinate and 0<= northing < self._max_coordinate:
                        return (easting, northing)
            raise ValueError
        except ValueError:
            raise ValueError

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

calculatorService = CalculatorService()
