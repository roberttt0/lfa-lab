def load_pda_config(filename):
    states = set()
    input_alphabet = set()
    stack_alphabet = set()
    initial_state = ''
    initial_stack_symbol = ''
    final_states = set()
    transitions = {}

    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    for line in lines:
        if line.startswith('STATES:'):
            states = set(line.split(':')[1].strip().split(','))
        elif line.startswith('INPUT_ALPHABET:'):
            input_alphabet = set(line.split(':')[1].strip().split(','))
        elif line.startswith('STACK_ALPHABET:'):
            stack_alphabet = set(line.split(':')[1].strip().split(','))
        elif line.startswith('INITIAL_STATE:'):
            initial_state = line.split(':')[1].strip()
        elif line.startswith('INITIAL_STACK_SYMBOL:'):
            initial_stack_symbol = line.split(':')[1].strip()
        elif line.startswith('FINAL_STATES:'):
            final_states = set(line.split(':')[1].strip().split(','))
        elif '->' in line:
            parse_transition(line, transitions)

    return {
        'states': states,
        'input_alphabet': input_alphabet,
        'stack_alphabet': stack_alphabet,
        'initial_state': initial_state,
        'initial_stack_symbol': initial_stack_symbol,
        'final_states': final_states,
        'transitions': transitions
    }


def parse_transition(line, transitions):
    left, right = line.split('->')
    left = left.strip().strip('()')
    right = right.strip().strip('()')

    current_state, input_symbol, stack_top = [x.strip() for x in left.split(',')]
    if input_symbol == 'ε':
        input_symbol = None

    next_state, stack_replacement = [x.strip() for x in right.split(',')]
    if stack_replacement == 'ε':
        stack_replacement = ''

    key = (current_state, input_symbol, stack_top)
    if key not in transitions:
        transitions[key] = []
    transitions[key].append((next_state, stack_replacement))


def simulate_pda(pda, input_string, pos, current_state, stack):
    if pos == len(input_string):
        if current_state in pda['final_states']:
            return True

        if stack:
            stack_top = stack[-1]
            key = (current_state, None, stack_top)
            if key in pda['transitions']:
                for next_state, stack_replacement in pda['transitions'][key]:
                    new_stack = stack[:-1] + list(reversed(stack_replacement))
                    if simulate_pda(pda, input_string, pos, next_state, new_stack):
                        return True
        return False

    current_symbol = input_string[pos]
    if stack:
        stack_top = stack[-1]
        key = (current_state, current_symbol, stack_top)
        if key in pda['transitions']:
            for next_state, stack_replacement in pda['transitions'][key]:
                new_stack = stack[:-1] + list(reversed(stack_replacement))
                if simulate_pda(pda, input_string, pos + 1, next_state, new_stack):
                    return True

    if stack:
        stack_top = stack[-1]
        key = (current_state, None, stack_top)
        if key in pda['transitions']:
            for next_state, stack_replacement in pda['transitions'][key]:
                new_stack = stack[:-1] + list(reversed(stack_replacement))
                if simulate_pda(pda, input_string, pos, next_state, new_stack):
                    return True

    return False


def accept(pda, input_string):
    return simulate_pda(pda, input_string, 0, pda['initial_state'], [pda['initial_stack_symbol']])


def print_pda_config(pda):
    print("Configuratia PDA")
    print(f"Stari: {pda['states']}")
    print(f"Alfabet de input: {pda['input_alphabet']}")
    print(f"Alfabet stiva: {pda['stack_alphabet']}")
    print(f"Stare initiala: {pda['initial_state']}")
    print(f"Simbol initial stiva: {pda['initial_stack_symbol']}")
    print(f"Stari finale: {pda['final_states']}")
    print("Tranzitii:")
    for key, values in pda['transitions'].items():
        state, symbol, stack_sym = key
        symbol_str = symbol if symbol else 'ε'
        for next_state, replacement in values:
            replacement_str = replacement if replacement else 'ε'
            print(f"  ({state}, {symbol_str}, {stack_sym}) -> ({next_state}, {replacement_str})")
    print()


def main():
    pda = load_pda_config('pda_config.txt')
    print_pda_config(pda)

    test_strings = ['ab', 'aabb', 'aaabbb', 'aaaabbbb', 'a', 'b', 'ba', 'aab', 'abb', 'abab', '']
    print("Testare PDA")
    print("Limbajul recunoscut: L = {a^n b^n | n ≥ 1}")
    print()

    for test_string in test_strings:
        display = 'ε (string vid)' if test_string == '' else test_string
        result = "ACCEPTAT" if accept(pda, test_string) else "RESPINS"
        print(f"String: '{display}' -> {result}")


if __name__ == "__main__":
    main()
