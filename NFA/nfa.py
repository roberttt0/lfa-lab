def epsilon_closure(states):
    return states

def nfa_accepts(nfa, word):
    current_states = {nfa["start_state"]}
    for symbol in word:
        next_states = set()
        for state in current_states:
            key = (state, symbol)
            if key in nfa["transitions"]:
                next_states.update(nfa["transitions"][key])
        current_states = next_states
        if not current_states:
            return False
    return bool(current_states & nfa["final_states"])


def parse_nfa_from_file(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    alphabet = set()
    states = set()
    start_state = None
    final_states = set()
    transitions = dict()
    words = []
    reading_section = None

    for line in lines:
        if line.startswith("Sigma:"):
            reading_section = "sigma"
        elif line.startswith("States:"):
            reading_section = "states"
        elif line.startswith("Start:"):
            start_state = line.split(":")[1].strip()
        elif line.startswith("Final:"):
            final_states = set(line.split(":")[1].strip().split())
        elif line.startswith("Transitions:"):
            reading_section = "transitions"
        elif line.startswith("Words:"):
            reading_section = "words"
        else:
            if reading_section == "sigma":
                alphabet.update(line.split())
            elif reading_section == "states":
                states.update(line.split())
            elif reading_section == "transitions":
                parts = line.split()
                if len(parts) == 3:
                    src, sym, dest = parts
                    key = (src, sym)
                    if key not in transitions:
                        transitions[key] = set()
                    transitions[key].add(dest)
            elif reading_section == "words":
                words.append(line.strip())

    nfa = {
        "states": states,
        "alphabet": alphabet,
        "start_state": start_state,
        "final_states": final_states,
        "transitions": transitions
    }

    return nfa, words


if __name__ == "__main__":
    nfa, words = parse_nfa_from_file("nfa_input.txt")

    for word in words:
        result = "ACCEPTED" if nfa_accepts(nfa, word) else "REJECTED"
        print(f"Word '{word}': {result}")
