# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
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
import sys
import copy

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

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.

    You are not required to implement this, but you may find it useful for Q5.
    """
    "*** YOUR CODE HERE ***"
    import collections
    visited = set()
    queue = collections.deque([problem.getStartState()])
    parent_of = {problem.getStartState(): (None, 0)}
    while queue:
        state = queue.popleft()
        if problem.isGoalState(state):
            path, moves = [state], []
            while True:
                last_state = path[-1]
                parent_state, move = parent_of[last_state]
                if parent_state:
                    moves.append(move)
                    path.append(parent_state)
                else:
                    moves.reverse()
                    return moves
        else:
            successor_state_movement_costs = problem.getSuccessors(state)
            visited.add(state)
            for new_state, move, cost in successor_state_movement_costs:
                if new_state not in visited:
                    queue.append(new_state)
                    parent_of[new_state] = (state, move)








def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def iterativeDeepeningSearch(problem):
    """
    Perform DFS with increasingly larger depth.

    Begin with a depth of 1 and increment depth by 1 at every step.
    """
    "*** YOUR CODE HERE ***"
    class State_ids:
        def __init__(self, successor_tuple, parent_state=None, depth=0):
            self.position, self.transition, _ = successor_tuple
            self.parent_state = parent_state
            self.depth = depth
            if parent_state is not None:
                self.depth = parent_state.depth + 1

        def backTrack(self):
            path = []
            state = self
            while state.parent_state is not None:
                    path.append(state.transition)
                    state = state.parent_state
            path.reverse()
            return path

    def dfs(problem, limit):
        visited, stack = set(), util.Stack()
        init_state = State_ids((problem.getStartState(), None, None))
        stack.push(init_state)
        while not stack.isEmpty():
            state = stack.pop()
            if problem.isGoalState(state.position):
                return state.backTrack()
            if state.depth < limit:
                for successor in filter(lambda s: s[0] not in visited, problem.getSuccessors(state.position)):
                    visited.add(successor[0])
                    stack.push(State_ids(successor, state))

    import itertools
    for limit in itertools.count():
        result = dfs(problem, limit)
        if result is not None:
            return result


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    class State_astar:
        def __init__(self, succrssor_tuple, parent=None, problem=problem, heuristic=heuristic):
            self.succrssor_tuple = succrssor_tuple
            self.position, self.transition, self.cost = succrssor_tuple
            self.problem = problem
            self.parent = parent
            self.heuristic = heuristic
            self.g = 0
            if parent is not None:
                self.g = parent.g_score() + self.cost

        def h_score(self):
            return self.heuristic(self.position, self.problem)

        def g_score(self):
            return self.g

        def f_score(self):
            return self.h_score() + self.g_score()

        def is_goal(self):
            return self.problem.isGoalState(self.position)

        def backTrack(self):
            path = []
            state = self
            while state.parent is not None:
                    path.append(state.transition)
                    state = state.parent
            path.reverse()
            return path

        @staticmethod
        def initial_state(_problem):
            return State_astar((_problem.getStartState(), None, 0), parent=None, problem=_problem)

    closed_set = set()
    open_set = util.PriorityQueue()
    open_set.push(State_astar.initial_state(problem), 0)

    while not open_set.isEmpty():
        current = open_set.pop()
        if current.is_goal():
            return current.backTrack()
        if current.position not in closed_set:
            closed_set.add(current.position)
            for neighbour in problem.getSuccessors(current.position):
                neighbour_state = State_astar(neighbour, current)
                open_set.push(neighbour_state, neighbour_state.f_score())


# Abbreviations
bfs = breadthFirstSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
