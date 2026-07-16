#
#this function returns the Minimum Excludant rule determines the current board's status. If
def mex(v_set): # the parameter v_set is the set of all the Nim-Value which is also known as the grundy-Value. If the Nim Value is 0, then it is P-positon and it the nim-value>0 then it is N-position. 
    g = 0 # Counter (g) is first at 0. 
    while g in v_set: # Checks if 0 is in the set of reachable Values. Only if it is, then the value is incremented to 1,2 and so on. The loop only runs if this counter g is in the set of reachable values. 
        g += 1 # Here we are going through all the nonnegative values that g possible can be. 
    return g

memo_cache = {} # Format: { game_state_tuple: nim_value }. The memo_cache variabel is a global dictionary 

def get_nim_value(state):  #State is a tuple that represents teh current arrangement of the game board. Eg. (1,2,2)
  #the variable state is a tuple as the key of a dictionary cannot be mutable data type
    # 1. DP Cache Check: Have we already solved this exact position?
    if state in memo_cache:
        return memo_cache[state]
    
    # 2. Base Case: If the game is over, the position has a value of 0
    if sum(state) == 0:
        return 0
        
    # 3. Find all valid next positions from the current state
    next_states = generate_next_states(state)
    
    # 4. Recursively find the Nim-values of all reachable next states
    reachable_values = {get_nim_value(s) for s in next_states} #By using a set rather than a list, Python automatically eliminates duplicate values.
    
    # 5. Apply the Mex operation to find the current state's value
    current_value = mex(reachable_values) #
    
    # 6. Save the calculated value to our cache and return it
    memo_cache[state] = current_value
    return current_value

def find_best_move(state):
    """
    Looks at the current state. If it's a winning position, 
    it finds and returns the exact move that leaves the opponent with a Nim-value of 0.
    """
    current_val = get_nim_value(state)
    
    # If the current position is a P-position (0), any move you make keeps you losing
    # assuming perfect play from your opponent. We'll just return the first legal move.
    if current_val == 0:
        next_states = generate_next_states(state)
        return next_states[0] if next_states else None
        
    # If it's an N-position (>0), find the move that forces a Nim-value of 0
    next_states = generate_next_states(state)
    for s in next_states:
        if get_nim_value(s) == 0:
            return s # This is the perfect mathematical move!
            
    return None    
def generate_next_states(state):
    """
    Generates all legal next game states from the current Nim state.
    A player can choose any non-empty heap and remove any number of counters from it.
    """
    next_states = []
    # Loop through each heap by its index
    for i in range(len(state)):
        # Try reducing the current heap's value to any smaller non-negative number
        for remaining in range(state[i]):
            # Create a copy of the list to modify
            new_state = list(state)
            new_state[i] = remaining
            # Always sort and convert back to a tuple for consistency
            next_states.append(tuple(sorted(new_state)))
            
    # Remove duplicate states using a set, then return as a list
    return list(set(next_states))