
def vacuum_cleaner_dfs(start_state):
    stack = [start_state]
    visited = set()

    while stack:
        state = stack.pop()

        if state in visited:
            continue
        visited.add(state)

        print("Visiting State:", state)

        # Goal test: both rooms are clean
        if state[1] == 'Clean' and state[2] == 'Clean':
            print("Goal reached!")
            return

        # Generate possible actions
        vacuum_location, room_a, room_b = state

        # Action: Clean
        if vacuum_location == 'A' and room_a == 'Dirty':
            new_state = ('A', 'Clean', room_b)
            stack.append(new_state)
        elif vacuum_location == 'B' and room_b == 'Dirty':
            new_state = ('B', room_a, 'Clean')
            stack.append(new_state)

        # Action: Move
        if vacuum_location == 'A':
            new_state = ('B', room_a, room_b)
            stack.append(new_state)
        elif vacuum_location == 'B':
            new_state = ('A', room_a, room_b)
            stack.append(new_state)

# Initial state: vacuum in A, A is Dirty, B is Dirty
initial_state = ('A', 'Dirty', 'Dirty')

vacuum_cleaner_dfs(initial_state)
