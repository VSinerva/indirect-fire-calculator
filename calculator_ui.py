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

    def _get_starting_values(self):
        calc.zero_values()
        action_str = "_"
        confirm_str = "DATA ENTERED"
        while action_str != "":
            clear()
            print(confirm_str)
            print("-"*len(confirm_str))
            print(f"Mortar:\t\t{calc.get_coords('mortar')[0]:05d} {calc.get_coords('mortar')[1]:05d}")
            print(f"Target:\t\t{calc.get_coords('target')[0]:05d} {calc.get_coords('target')[1]:05d}")
            print(f"Observer:\t{calc.get_coords('observer')[0]:05d} {calc.get_coords('observer')[1]:05d}")
            print()

            action_str = input("Enter coordinates to fill next position.\n'M', 'T' or 'O' to change specific value.\n'Enter' to continue. 'E' to Exit: ")

            if action_str.upper() == "E":
                print("Shutting down...")
                exit()

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
                        except ValueError:
                            pass
                        break

    def _firing_values(self):
        print()
        solution_str = "FIRING DATA"
        print(solution_str)
        print("-"*len(solution_str))
        print(f"Dist: {calc.get_dist_to_target():.0f}m")
        print(f"Az: {calc.get_az_to_target():.0f}")
        print()

    def _update_firing_values(self):
        input("Enter to continue...")

    def run(self):
        while True:
            self._get_starting_values()
            try:
                self._firing_values()
                self._update_firing_values()
            except ValueError:
                clear()
                calc.zero_values()

calculator = CalculatorUI()
