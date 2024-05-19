# Kevin Vuong
# 8 puzzle program that includes three heuristics: Number of misplaced tiles, total Manhattan Distance, and total Euclidean Distance

import math
import time

class Puzzle:
    def __init__(self, start_state, end_state):
        self.current_state = start_state
        self.end_state = end_state
    
    def print_puzzle(self, state):
        for row in state:
            print(" ".join(map(str, row)))
    
    def heuristics_one (self, state): # Number of misplaced tiles
        misplaced_tiles = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != self.end_state[i][j]:
                    misplaced_tiles += 1
        return misplaced_tiles

    def heuristics_two (self, state): # Total Manhattan Distance
        manhattan_distance = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0:
                    goal_i, goal_j = divmod(state[i][j]-1, 3) # Get the goal number like (7-1)/2 -> goal_i = 2 and goal_j = 0
                    manhattan_distance += abs(goal_i - i) + abs(goal_j - j) # Using the Manhattan Distance Formula and update the distance total
        return manhattan_distance
    
    def heuristics_three(self, state): # Total Euclidean Distance
        total_distance = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0:
                    goal_i, goal_j = divmod(state[i][j]-1, 3) # Get the goal number like (7-1)/2 -> goal_x = 2 and goal_y = 0
                    euclidean_distance = math.sqrt((goal_i - i)**2 + (goal_j - j)**2) # Using the Euclidean Distance Formula
                    total_distance += euclidean_distance # Update total distance
        return total_distance

def get_user_input(): # Get the user's input (initial state)
  print ("\nEnter the initial state of the puzzle (3 rows of 3 numbers, use 0 for blank):")
  puzzle = []
  for i in range(3):
    row = input().strip().split()
    puzzle.append([int(x) for x in row])
  return puzzle

def get_inversion_count(state): # Get the inversion count to determine if two states can be reach
    flattened_state = [item for sublist in state for item in sublist if item != 0]  # Flatten the state into a 1D list
    inversion_count = 0
    for i in range(len(flattened_state)):
        for j in range(i + 1, len(flattened_state)):
            if flattened_state[i] > flattened_state[j]:
                inversion_count += 1
    return inversion_count

def possible_moves(state): # Get all possible moves that the blank tile can move
    moves = []
    # Row and Columns for blank tile
    blank_row = 0
    blank_col = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                blank_row, blank_col = i, j # Finding where the blank (0) is in the puzzle
                break

    # Generate possible moves
    if blank_row > 0:  # Move blank tile up
        new_state = [row[:] for row in state]  # Create a copy of the current state
        temp = new_state[blank_row][blank_col]
        #Swap places
        new_state[blank_row][blank_col] = new_state[blank_row - 1][blank_col]
        new_state[blank_row - 1][blank_col] = temp
        moves.append(new_state)

    if blank_row < 2:  # Move blank tile down
        new_state = [row[:] for row in state]
        temp = new_state[blank_row][blank_col]
        #Swap places
        new_state[blank_row][blank_col] = new_state[blank_row + 1][blank_col]
        new_state[blank_row + 1][blank_col] = temp
        moves.append(new_state)

    if blank_col > 0:  # Move blank tile left
        new_state = [row[:] for row in state]
        temp = new_state[blank_row][blank_col]
        #Swap places
        new_state[blank_row][blank_col] = new_state[blank_row][blank_col - 1]
        new_state[blank_row][blank_col - 1] = temp
        moves.append(new_state)

    if blank_col < 2:  # Move blank tile right
        new_state = [row[:] for row in state]
        temp = new_state[blank_row][blank_col]
        #Swap places
        new_state[blank_row][blank_col] = new_state[blank_row][blank_col + 1]
        new_state[blank_row][blank_col + 1] = temp
        moves.append(new_state)

    return moves

def best_first_search(start_state, end_state, heuristic_choice):
    puzzle = Puzzle(start_state, end_state)
    frontier = None # frontier will include initial heuristics, current state, step count
    if heuristic_choice == 1:
        frontier = [(puzzle.heuristics_one(puzzle.current_state), start_state, 0)]
    elif heuristic_choice == 2:
        frontier = [(puzzle.heuristics_two(puzzle.current_state), start_state, 0)] 
    else:
        frontier = [(puzzle.heuristics_three(puzzle.current_state), start_state, 0)]  
    visited = set()

    while frontier:
        frontier.sort() # Sort where the minimal heuristic will be first
        h, puzzle.current_state, steps = frontier.pop(0)  # Extract heuristic, state, and steps

        # Did this to see the fewer steps at first 
        """
        if steps < 5:
            puzzle.print_puzzle(puzzle.current_state) # Print out the puzzle
        """

        puzzle.print_puzzle(puzzle.current_state) # Print out the puzzle
        print ("Heuristic Cost: ", h, "\n")
        
        if puzzle.current_state == end_state: # Reach Goal
            print("Goal state reached in", steps, "steps!\n")
            puzzle.print_puzzle(puzzle.current_state) # Print out the puzzle
            return

        visited.add(tuple(map(tuple, puzzle.current_state)))
        # Generate child states
        if steps < 1000:
            for move in possible_moves(puzzle.current_state):
                if tuple(map(tuple, move)) not in visited: # To avoid repetitive steps or infinite loops with the same steps
                    if heuristic_choice == 1:
                        frontier.append((puzzle.heuristics_one(move), move, steps + 1))  # Increment steps and go to the next frontier
                    elif heuristic_choice == 2:
                        frontier.append((puzzle.heuristics_two(move), move, steps + 1))  # Increment steps and go to the next frontier
                    else:
                        frontier.append((puzzle.heuristics_three(move), move, steps + 1))  # Increment steps and go to the next frontier

    print("Goal state not reachable!")

def a_star_search(start_state, end_state, heuristic_choice):
    puzzle = Puzzle(start_state, end_state)
    frontier = None # frontier will include initial heuristics, current state, step count, cost
    if heuristic_choice == 1:
        frontier = [(puzzle.heuristics_one(puzzle.current_state), start_state, 0, 0)]
    elif heuristic_choice == 2:
        frontier = [(puzzle.heuristics_two(puzzle.current_state), start_state, 0, 0)] 
    else:
        frontier = [(puzzle.heuristics_three(puzzle.current_state), start_state, 0, 0)]  
    visited = set()

    while frontier:
        frontier.sort()
        total, puzzle.current_state, steps, cost = frontier.pop(0)

        # Did this to see the fewer steps at first 
        """
        if steps < 5:
            puzzle.print_puzzle(puzzle.current_state) # Print out the puzzle
        """

        puzzle.print_puzzle(puzzle.current_state)
        print ("Depth: ", steps)
        print ("Cost: ", total, "\n")
        
        if puzzle.current_state == end_state: # Goal Reached
            print("Goal state reached in", steps, "steps!\n")
            puzzle.print_puzzle(puzzle.current_state) # Print out the puzzle
            return
        visited.add(tuple(map(tuple, puzzle.current_state)))

        if steps < 1000:
            for move in possible_moves(puzzle.current_state):
                if tuple(map(tuple, move)) not in visited: # To avoid repetitive steps or infinite loops with the same steps
                    new_cost = steps + 1
                    if heuristic_choice == 1:
                        frontier.append((new_cost + puzzle.heuristics_one(move), move, steps + 1, new_cost))  # Increment steps and new_cost and go to the next frontier
                    elif heuristic_choice == 2:
                        frontier.append((new_cost + puzzle.heuristics_two(move), move, steps + 1, new_cost))  # Increment steps and go to the next frontier
                    else:
                        frontier.append((new_cost + puzzle.heuristics_three(move), move, steps + 1, new_cost))  # Increment steps and go to the next frontier

if __name__ == '__main__':
    running = True
    while running:
        choices = input("\nPlease Select the Options Below:\n1.) Best-First-Search\n2.) A*\n3.) Quit Program\nEx. If you want to do BFS, then select 1\n")
        if int(choices) == 3:
            break
        
        # Get the type of heuristic
        heuristic_choice = None
        while heuristic_choice not in [1, 2, 3]:
            heuristic_choice = int(input("\nPlease Select Which Heuristic to Use:\n1.) Number of misplaced tiles\n2.) Manhattan Distance\n3.) Euclidean Distance\n"))

        initial_state = get_user_input()
        end_goal = [
            [1, 2 ,3],
            [4, 5, 6],
            [7, 8, 0]
        ]
    
        initial_inversion = get_inversion_count(initial_state)
        goal_inversion = get_inversion_count(end_goal)

        print ("Initial Inversion: ", initial_inversion)

        if (initial_inversion % 2 == goal_inversion % 2):
            print("Both states are reachable")
            if int(choices) == 1:
                start = time.time()
                best_first_search(initial_state, end_goal, heuristic_choice)
                end = time.time()
                print ("Execution Time(s): ", end-start)
            if int(choices) == 2:
                start = time.time()
                a_star_search(initial_state, end_goal, heuristic_choice)
                end = time.time()
                print ("Execution Time(s): ", end-start)
        else:
            print ("Both states aren't reachable")