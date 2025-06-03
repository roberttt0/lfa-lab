def turing_machine_duplicate(initial_string, N):
    tape = list(initial_string)
    head_position = 0
    state = "start"
    current_duplication = 0

    while current_duplication < N - 1:
        if state == "start":
            if head_position < len(tape):
                head_position += 1
            else:
                state = "copy"
                head_position = 0

        elif state == "copy":
            if head_position < len(initial_string):
                tape.append(initial_string[head_position])
                head_position += 1
            else:
                current_duplication += 1
                state = "start"
                head_position = 0

    return ''.join(tape)

initial_string = "abc"
N = 3
result = turing_machine_duplicate(initial_string, N)
print(f"Rezultatul duplicarii de {N} ori a '{initial_string}': {result}")