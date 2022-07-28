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
        print("Suljetaan...")
        exit()

    def _get_starting_values(self):
        calc.zero_values()
        action_str = "_"
        while action_str != "" or not (calc.coords_set("mortar") and calc.coords_set("target")):
            clear()
            self._print_coordinates()
            action_str = input("Lisää seuraavat koordinaatit ja paina 'Enter'.\nPaina 'H', 'K' or 'T' tiettyjen arvojen päivittämiseksi.\nPaina 'Enter' jatkaaksesi. Paina 'S' sulkeaksesi ohjelma: ")

            if action_str.upper() == "S":
                self._close()

            pos_name = None
            if action_str:
                if action_str[0].upper() == "H":
                    pos_name = "mortar"
                elif action_str[0].upper() == "K":
                    pos_name = "target"
                elif action_str[0].upper() == "T":
                    pos_name = "observer"

            if pos_name:
                while True:
                    try:
                        calc.set_coords(input("Aseta koordinaatit: "), pos_name)
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
        confirm_str = "KOORDINAATIT"
        print(confirm_str)
        print("-"*len(confirm_str))
        print(f"Heitin:\t\t{calc.get_coords('mortar')[0]:05d} {calc.get_coords('mortar')[1]:05d}")
        print(f"Kohde:\t\t{calc.get_coords('target')[0]:05d} {calc.get_coords('target')[1]:05d}")
        print(f"Tulenjohtaja:\t{calc.get_coords('observer')[0]:05d} {calc.get_coords('observer')[1]:05d}")
        print()


    def _print_firing_values(self):
        print()
        solution_str = "HEITTIMEN ARVOT"
        print(solution_str)
        print("-"*len(solution_str))
        print(f"Etäisyys: {calc.get_dist_to_target():.0f}m")
        print(f"Suuntima: {calc.get_az_to_target():.0f}")
        print()

    def _update_firing_values(self):
        while True:
            clear()
            self._print_coordinates()
            self._print_firing_values()

            if calc.coords_set("observer"):
                print("Anna korjaukset muodossa \"X(V/O) ja/tai Y(J/L)\".")
                print("Päivitä tulenjohtajan sijainti syöttämällä 'T' ja uudet koordinaatit.")
            else:
                print("Aseta tulenjohtajan sijainti syöttämällä 'T' ja koordinaatit.")

            action_str = input("Päivitä kohde syöttämällä 'K' ja uudet koordinaatit.\nPaina 'N' nollataksesi. Paina 'S' sulkeaksesi: ")
            if not action_str:
                continue

            if action_str.upper() == "S":
                self._close()
            if action_str.upper() == "N":
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
