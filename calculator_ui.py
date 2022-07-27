from os import system, name

from calculator_service import calculatorService as calc

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux
    else:
        _ = system('clear')


class CalculatorUI:
    def __init__(self):
        clear()

    def _close(self):
        print("Shutting down...")
        exit()

    def _get_starting_values(self):
        calc.zero_values()
        action_str = "_"
        while action_str != "" or not (calc.coords_set("mortar") and calc.coords_set("target")):
            clear()
            self._print_coordinates()
            action_str = input("Enter coordinates to fill next position.\n'M', 'T' or 'O' to change specific value.\n'Enter' to continue. 'E' to Exit: ")

            if action_str.upper() == "E":
                self._close()

            pos_name = None
            if action_str.upper() == "M":
                pos_name = "mortar"
            elif action_str.upper() == "T":
                pos_name = "target"
            elif action_str.upper() == "O":
                pos_name = "observer"

            if pos_name:
                while True:
                    try:
                        calc.set_coords(input(f"Set {pos_name} coordinates: "), pos_name)
                        break
                    except ValueError:
                        continue
            else:
                for pos in ["mortar", "target", "observer"]:
                    if not calc.coords_set(pos):
                        try:
                            calc.set_coords(action_str, pos)
                            if pos == "observer":
                                return
                        except ValueError:
                            pass
                        break

    def _print_coordinates(self):
        print()
        confirm_str = "DATA ENTERED"
        print(confirm_str)
        print("-"*len(confirm_str))
        print(f"Mortar:\t\t{calc.get_coords('mortar')[0]:05d} {calc.get_coords('mortar')[1]:05d}")
        print(f"Target:\t\t{calc.get_coords('target')[0]:05d} {calc.get_coords('target')[1]:05d}")
        print(f"Observer:\t{calc.get_coords('observer')[0]:05d} {calc.get_coords('observer')[1]:05d}")
        print()


    def _print_firing_values(self):
        print()
        solution_str = "FIRING DATA"
        print(solution_str)
        print("-"*len(solution_str))
        print(f"Dist: {calc.get_dist_to_target():.0f}m")
        print(f"Az: {calc.get_az_to_target():.0f}")
        print()

    def _update_firing_values(self):
        while True:
            clear()
            self._print_coordinates()
            self._print_firing_values()

            if calc.coords_set("observer"):
                print("Give updates string as \"X(V/O) and/or Y(J/L)\".")
                print("Set new observer position with 'T' followed by coordinates.")
            else:
                print("Set observer position with 'T' followed by coordinates.")

            action_str = input("Set new target with 'K' followed by coordinates.\nReset with 'R'. Exit with 'E': ")
            if not action_str:
                continue

            if action_str.upper() == "E":
                self._close()
            if action_str.upper() == "R":
                return
            if action_str[0].upper() == "T":
                try:
                    calc.set_coords(action_str[1:], "observer")
                except ValueError:
                    pass
            if action_str[0].upper() == "K":
                try:
                    calc.set_coords(action_str[1:], "target")
                except ValueError:
                    pass

            try:
                calc.update_target(action_str)
            except ValueError:
                pass

    def run(self):
        while True:
            self._get_starting_values()
            try:
                self._update_firing_values()
            except ValueError:
                clear()
                calc.zero_values()

calculator = CalculatorUI()
