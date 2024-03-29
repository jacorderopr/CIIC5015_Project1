# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from util import Stack, Queue, PriorityQueue

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    # getSuccessors gives your: (successor, action, step_cost)
    stack = Stack()
    visited = set()
    stack.push( (problem.getStartState(), [])) # stack contains: (current_coords, path: list)


    while not stack.isEmpty():
        current_coords, path = stack.pop()
        # print(f"current_coords: {current_coords} , path: {path}")
        if current_coords not in visited:
            visited.add(current_coords)
        if problem.isGoalState(current_coords):
            # need to return the path taken
            print(f"length of solution: {len(path)}")
            return path
        for neighbor_coords, directionTaken, _ in problem.getSuccessors(current_coords):
            if neighbor_coords not in visited:
                stack.push((neighbor_coords, path + [directionTaken]))

    return []


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = Queue()
    visited = set()
    start_coords = problem.getStartState()
    queue.push( (start_coords, []) )
    visited.add(start_coords)

    while not queue.isEmpty():
        current_coords, current_path = queue.pop()
        if problem.isGoalState(current_coords):
            return current_path

        for neighbor_coords, directionTaken, _ in problem.getSuccessors(current_coords):
            if neighbor_coords not in visited:
                visited.add(neighbor_coords)
                queue.push( (neighbor_coords, current_path + [directionTaken]) )
    return []
def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # Dijkstra's algorithm - now we must consider costs
    priorityQueue = PriorityQueue() # def push(self, item, priority):
    visited = set()
    start_coords = problem.getStartState()
    priorityQueue.push((start_coords, 0,  []), 0) # cost to get to start is 0
    explored_costs = dict()
    explored_costs[start_coords] = 0
    while not priorityQueue.isEmpty():
        current_coords, current_cost, current_path = priorityQueue.pop()
        if problem.isGoalState(current_coords):
            return current_path
        if current_coords in visited:
            continue # skip because we have already been here
        visited.add(current_coords)

        for neighbor_coords, directionTaken, costToNeighbor in problem.getSuccessors(current_coords):
            if neighbor_coords in visited:
                continue
            totalCost = current_cost + costToNeighbor
            if totalCost < explored_costs.get(neighbor_coords, float("inf")):
                explored_costs[neighbor_coords] = totalCost
                priorityQueue.push( (neighbor_coords, totalCost, current_path + [directionTaken]), totalCost)

    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# a star search with heuristic
def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    # idea: use manhattanHeuristic to calculate distance between the neighbor coord and the goal and then prioritize the lower distance
    # use explored_costs dict
    priorityQueue = PriorityQueue()
    visited = set()
    explored_costs = dict()

    start_coords = problem.getStartState()
    priorityQueue.push( (start_coords, 0, []), 0)

    while not priorityQueue.isEmpty():
        coords, cost, path = priorityQueue.pop()

        if problem.isGoalState(coords):
            return path
        if coords in visited:
            continue
        visited.add(coords)

        for neighbor_coords, directionTaken, costToNeighbor in problem.getSuccessors(coords):
            if neighbor_coords in visited:
                continue
            heuristic_cost = cost + costToNeighbor + heuristic(neighbor_coords, problem)
            # print(f"for neighbor_coords: {neighbor_coords} heuristic cost is : {heuristic_cost}")
            if heuristic_cost < explored_costs.get(neighbor_coords, float("inf")):
                explored_costs[neighbor_coords] = heuristic_cost
                priorityQueue.push( (neighbor_coords, cost + costToNeighbor, path + [directionTaken]), heuristic_cost)
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
