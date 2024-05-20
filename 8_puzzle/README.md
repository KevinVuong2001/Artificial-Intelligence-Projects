# 8 Puzzle Problem

## Context 
The goal of this puzzle problem is to move the puzzle piece around to the point where we get an end goal. For example (0 is consider as our blank space): <br />
1 2 0   &emsp;    &emsp; 1 2 3<br />
4 5 3   &nbsp; -> &nbsp; 4 5 6<br />
7 8 6   &emsp;    &emsp; 7 8 0<br />

The process is mainly determining where to move our blank tile (0) where it's the most optimal. We would calculate the heuristic cost for each action and go with the least cost. It can move up, down, left, and right.

## Instructions
1. Run the command `python3 8_puzzle.py`
2. It will then prompt the following options from (1, 2, 3):
    - 1: Best-First-Search
    - 2: A* Search
    - 3: Quit Program
3. Then, it will prompt the following options for type heuristics:
    - 1: Number of Misplaced Tiles
    - 2: Total Manhattan Distance
    - 3: Total Euclidean Distance
4. After that, it will prompt the user to enter in the initial state
    - Enter 3 numbers each row and use 0 as blank
    - Example: <br /> 
        1 2 0 <br />
        4 5 3 <br />
        7 8 6 <br />
5.  Results would be either:
    - If the initial state and the end state are reachable (both inversions have to be both even or odd)
        - It will display: 
            - the process of moving the puzzle
            - execution time
            - number of steps needed to get to the end goal/state
    - If they are not reachable we cannot run the 8 puzzle problem

## Walkthrough Example
### Context: A* search with Manhattan Distance as the Heuristic 
### Initial Setup: 
![alt text](Initial_Setup.png) <br />
### Process/Result:  
![alt text](Result.png) <br />