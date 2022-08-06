from math import sqrt, atan2, pi, sin, cos
import csv

class CalculatorService:
    def __init__(self):
        self._max_coordinate = 10**5
        self._circle_divisions = 6400 

        self._coords = {}
        self._coords_set = {}
        self.zero_values()

        self._range_table = {}
        self._range_table_name = ""
        self._range_table_set = False

    @property
    def range_table_name(self):
        return self._range_table_name
    @property
    def range_table_set(self):
        return self._range_table_set

    def zero_values(self):
        self._coords["mortar"] = (0, 0)
        self._coords["target"] = (0, 0)
        self._coords["observer"] = (0, 0)
        self._coords_set["mortar"] =  False
        self._coords_set["target"] = False
        self._coords_set["observer"] = False

    def set_range_table(self, range_table_path: str):
        try:
            with open(range_table_path, "r") as file:
                csv_reader = csv.DictReader(file)
                for line in csv_reader:
                    charge = int(line["charge"])
                    dist = int(line["dist"])
                    elev = int(line["elev"])
                    time_of_flight = float(line["tof"].replace(",", "."))
                    if charge not in self._range_table:
                        self._range_table[charge] = []
                    self._range_table[charge].append((dist, elev, time_of_flight))
        except Exception as e:
            self._range_table = []
            self._range_table_name = ""
            self._range_table_set = False
            raise e
        self._range_table_set = True
        self._range_table_name = range_table_path[0:-4].upper()

    def set_coords(self, coordinate_string: str, pos_name: str):
        if pos_name not in self._coords:
            raise ValueError("Invalid position name!")
        try:
            self._coords[pos_name] = self._str_to_coords(coordinate_string)
            self._coords_set[pos_name] = True
        except ValueError as e:
            raise e

    def get_coords(self, pos_name: str):
        return self._coords[pos_name]

    def coords_set(self, pos_name: str):
        return self._coords_set[pos_name]

    def get_az_to_target(self):
        return self._azimuth(self._coords["mortar"], self._coords["target"])

    def get_dist_to_target(self):
        return self._distance_between(self._coords["mortar"], self._coords["target"])

    def get_elev_to_target(self):
        dist = self.get_dist_to_target()

        possible_values = []

        for charge, table in self._range_table.items():
            if table[0][0] > dist or table[-1][0] < dist:
                continue

            lower = 0
            while table[lower+1][0] <= dist:
                lower += 1
            upper = len(table)-1
            while table[upper-1][0] > dist:
                upper -= 1
            
            l_dist, l_elev, l_tof = table[lower]
            u_dist, u_elev, u_tof = table[upper]

            #Interpolate between the two closest values in the range table
            elev = l_elev + (dist-l_dist) * (u_elev-l_elev) / (u_dist-l_dist)
            tof = l_tof + (dist-l_dist) * (u_tof-l_tof) / (u_dist-l_dist)

            possible_values.append((tof, charge, elev))

        if len(possible_values) == 0:
            raise ValueError

        tof, charge, elev = min(possible_values)
        return (charge, elev, tof)

    def update_target(self, update_string: str):
        if not self.coords_set("observer"):
            raise ValueError("Virheellinen korjaus!")

        substrings = update_string.strip().split(" ")
        if not (0 < len(substrings) < 3):
            raise ValueError("Virheellinen korjaus!")

        sideways_str = None
        lengthways_str = None

        for substring in substrings:
            c = substring[0].upper()
            if c == "O":
                sideways_str = substring[1:]
            elif c == "V":
                sideways_str = "-" + substring[1:]
            elif c == "J":
                lengthways_str = substring[1:]
            elif c == "L":
                lengthways_str = "-" + substring[1:]
            else:
                raise ValueError("Virheellinen korjaus!")

        try:
            side_correction = int(sideways_str)
        except:
            side_correction = 0

        try:
            length_correction = int(lengthways_str)
        except:
            length_correction = 0

        observer = self.get_coords("observer")
        target = self.get_coords("target")

        dist = self._distance_between(self.get_coords("observer"), self.get_coords("target"))

        #Find a vector of length 1m facing forward from the forward observer
        observer_forward_vec = self._vec_mult(1/dist, self._vec_sub(target, observer))

        #Find a vector of the same length at a 90 degree angle to forward vec
        observer_right_vec = (observer_forward_vec[1], -observer_forward_vec[0])

        side_correction_vec = self._vec_mult(side_correction, observer_right_vec)
        length_correction_vec = self._vec_mult(length_correction, observer_forward_vec)
        correction_vec = self._vec_add(side_correction_vec, length_correction_vec)

        target = self._vec_add(target, correction_vec)

        self._coords["target"] = (round(target[0]), round(target[1]))

    def set_pos_az_dist(self, ref_pos_name: str, new_pos_name: str, string: str, invert=False):
        if string[0] != "T" and string[0] != "A":
            raise ValueError("Syöte ei ole suuntima-etäisyys-merkkijono!")
        try:
            if string[0] == "T":
                string = string[1:]

            string = string[1:].strip()
            az_str, dist_str = string.split(" ")
            az = int(az_str)
            dist = int(dist_str)
            
            if not self._coords_set[ref_pos_name]:
                self.set_coords("5 5", ref_pos_name)

            #Find easting and northing vector from azimuth
            vec_e = sin(2*pi * az/360) * dist
            vec_n = cos(2*pi * az/360) * dist

            if invert:
                vec_e *= -1
                vec_n *= -1

            easting, northing = self._coords[ref_pos_name]
            easting += vec_e
            northing += vec_n
            self._coords[new_pos_name] = (round(easting), round(northing))
            self._coords_set[new_pos_name] = True

        except ValueError as e:
            errors = errors + str(e) + "\n"

    def set_target_and_observer(self, string: str):
        try:
            substrings = string[1:].strip().split(" ")
            self.set_coords(substrings[0]+" "+substrings[1], "target")
            self.set_pos_az_dist("target", "observer", "A "+substrings[2]+" "+substrings[3], True)
        except ValueError as e:
            raise e

    def _vec_sub(self, vec1, vec2):
        return (vec1[0]-vec2[0], vec1[1]-vec2[1])

    def _vec_add(self, vec1, vec2):
        return (vec1[0]+vec2[0], vec1[1]+vec2[1])

    def _vec_mult(self, mult, vec):
        return (mult*vec[0], mult*vec[1])

    def _str_to_coords(self, string: str):
        try:
            string = string.strip()
            if len(string) > 0:
                substrings = string.split(" ")
                if len(substrings) == 2:
                    values = []
                    for substring in substrings:
                        coord = 0
                        counter = self._max_coordinate
                        try:
                            for c in substring:
                                if counter > 1:
                                    counter = counter // 10
                                    coord *= 10
                                    coord += int(c)
                        except ValueError:
                            raise ValueError("Virheellinen merkki koordinaateissa!")
                        while counter > 1:
                            counter = counter // 10
                            coord*= 10
                        values.append(coord)

                    easting = values[0]
                    northing = values[1]

                    if 0 <= easting < self._max_coordinate and 0<= northing < self._max_coordinate:
                        return (easting, northing)
                raise ValueError("Virheelliset koordinaatit!")
            raise ValueError("Tyhjät koordinaatit!")
        except ValueError as e:
            raise e 

    def _distance_between(self, coords1, coords2):
        e_dist = coords1[0] - coords2[0]
        n_dist = coords1[1] - coords2[1]
        return sqrt(e_dist**2 + n_dist**2)

    #Find azimuth from one point to another
    def _azimuth(self, coords1, coords2):
        d_e, d_n = self._vec_sub(coords2, coords1)

        if d_e == 0:
            return 0 if d_n > 0 else self._circle_divisions / 2
        if d_n == 0:
            return self._circle_divisions / 4 if d_e > 0 else 3*self._circle_divisions / 4

        az = atan2(d_e, d_n)/(2*pi) * self._circle_divisions 
        if az < 0:
            az += self._circle_divisions
        return az 

calculatorService = CalculatorService()
