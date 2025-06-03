def citire(fisier):
    f = open(fisier, "r")
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if "/" in line:
            new_line = ""
            for chr in line:
                if chr != "/":
                    new_line += chr
                else:
                    break
            line = new_line
        if line == "[State]":
            current = "State"   # Folosim variabila current pentru a sti in ce sectiune ne aflam (State, Symbols, Rules)
            d[current] = []     # Cream o lista pentru "State"
        elif line == "[Symbols]":
            current = "Symbols"
            d[current] = []     # Cream o lista pentru "Symbols"
        elif line == "[Rules]":
            current = "Rules"
            d[current] = {}     # Cream un dictionar pentru "Rules"
        elif line == "[Start_State]":
            current = "Start_State"
            d[current] = []     # Cream o lista pentru "Start_State"
        elif line == "[Accept_States]":
            current = "Accept_States"
            d[current] = []     # Cream o lista pentru "Accept_States"
        elif line == "[Tests]":
            current = "Tests"
            d[current] = []     # Cream o lista pentru "Tests"

        else:
            if current != "Rules":
                line_split = line.split()
                if len(line_split) != 1:
                    return f"Error in line {line} from {current}. Invalid input."      # Verificam daca datele din sectiunile diferite de Rules au doar un element (sunt valide)
                d[current].append(line)
            if current == "Tests":
                for seq in d[current]:
                    for symbol in seq:
                        if symbol not in d["Symbols"]:
                            return f"Error in line {line} from {current}. Symbol {symbol} from {seq} is invalid."   # Verificam daca symbolurile din fiecare test apar in "Symbols"
            if current == "Rules":
                line_split = line.split(", ")
                print(line_split)
                if len(line_split) != 3:
                    return f"Error in line {line} from {current}. Invalid format"      # Verificam daca instructiunea este valida
                if line_split[0] not in d["State"]:
                    return f"Error in line {line} from {current}. State {line_split[0]} does not exist."     # Verificam daca primul state din instructiune exista
                if line_split[2] not in d["State"]:
                    return f"Error in line {line} from {current}. State {line_split[2]} does not exist."     # Verificam daca al doilea state din instructiune exista
                if line_split[1] not in d["Symbols"]:
                    return f"Error in line {line} from {current}. Symbol {line_split[1]} does not exist."        # Verificam daca simbolul din instructiune exista
                d[current][(line_split[0], line_split[1])] = line_split[2]
    # Verificam daca toate campurile necesare rularii programului se afla in input
    if "State" not in d:
        return f"Missing 'State' field from input"
    if "Start_State" not in d:
        return f"Missing 'Start_State' field from input"
    if "Accept_States" not in d:
        return f"Missing 'Accept_States' field from input"
    if "Rules" not in d:
        return f"Missing 'Rules' field from input"
    if "Tests" not in d:
        return f"Missing 'Tests' field from input"
    return d

def validate(d):
    for test in d["Tests"]:
        current_state = d["Start_State"][0]
        for symbol in test:
            if (current_state, symbol) in d["Rules"]:
                    current_state = d["Rules"][(current_state, symbol)]
            else:
                return f"Invalid data in rule {(current_state, symbol)}"
        if current_state in d["Accept_States"]:
            print (f"{test}: Succes")
        else:
            print (f"{test}: Failed")

d={}
d = citire("joc2.in")
# d = citire("joc.in")

print(d)

validate(d)
