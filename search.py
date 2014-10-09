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
import logic

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

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostSearchProblem)
        """
        util.raiseNotDefined()

    def terminalTest(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionSearchProblem
        """
        util.raiseNotDefined()

    def result(self, state, action):
        """
        Given a state and an action, returns resulting state and step cost, which is
        the incremental cost of moving to that successor.
        Returns (next_state, cost)
        """
        util.raiseNotDefined()

    def actions(self, state):
        """
        Given a state, returns available actions.
        Returns a list of actions
        """        
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

    def getWidth(self):
        """
        Returns the width of the playable grid (does not include the external wall)
        Possible x positions for agents will be in range [1,width]
        """
        util.raiseNotDefined()

    def getHeight(self):
        """
        Returns the height of the playable grid (does not include the external wall)
        Possible y positions for agents will be in range [1,height]
        """
        util.raiseNotDefined()

    def isWall(self, position):
        """
        Return true if position (x,y) is a wall. Returns false otherwise.
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


def atLeastOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that at least one of the expressions in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    if len(expressions) == 1 :
        return expressions[0]
    a = expressions[0]
    for place in range(1, len(expressions)) :
        a = logic.Expr('|', a, expressions[place])
    return a
#test
def atMostOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that at most one of the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    if len(expressions) == 1 :
        return logic.Expr('|', logic.Expr('~', expressions[0]), expressions[0])
    a = logic.Expr('|', logic.Expr('~', expressions[0]), logic.Expr('~', expressions[1]))
    for place in range(len(expressions) - 1) :
        for place1 in range(place + 1, len(expressions)) :
            if not (place == 0 and place1 == 1) :
                a = logic.Expr('&', a, logic.Expr('|', logic.Expr('~', expressions[place]), logic.Expr('~', expressions[place1])))
    return a

def exactlyOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that exactly one of the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    if len(expressions) == 1 :
        return expressions[0]
    a = logic.Expr('&', atMostOne(expressions), atLeastOne(expressions))
    return a

def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"
    sequence = list()
    time = 0
    proceed = 1
    while True :
        success = 0
        for place in range(len(actions)) :
            if model.has_key(logic.PropSymbolExpr(actions[place], time)) and model[logic.PropSymbolExpr(actions[place], time)] :
                sequence.append(actions[place])
                success = 1
            if place == len(actions) - 1 and success == 0 :
                proceed = 0
        time = time + 1
        if proceed == 0 :
            break
    return sequence

def positionLogicPlan(problem):
    """
    Given an instance of a PositionSearchProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    expression = list()
    for x in range(1, problem.getWidth() + 1) :
        for y in range(1, problem.getHeight() + 1) :
            if (x, y) == problem.getStartState() :
                expression.append(logic.PropSymbolExpr("P", problem.getStartState()[0], problem.getStartState()[1], 0))
            else :
                expression.append(logic.Expr("~", logic.PropSymbolExpr("P", x, y, 0)))
    for steps in range(50) :
        for x in range(1, problem.getWidth() + 1) :
            for y in range(1, problem.getHeight() + 1) :
                position = (x, y)
                time = steps
                step1 = logic.PropSymbolExpr("P", position[0], position[1], time + 1)
                sequence = list()
                for action in problem.actions(position) :
                    if action == "North" :
                        move = "South"
                    elif action == "West" :
                        move = "East"
                    elif action == "South" :
                        move = "North"
                    else :
                        move = "West"
                    step2 = logic.PropSymbolExpr(move, time)
                    step3 = logic.PropSymbolExpr("P", problem.result(position, action)[0][0], problem.result(position, action)[0][1], time)
                    step4 = logic.Expr("&", step2, step3)
                    sequence.append(step4)
                if len(sequence) > 0 :
                    expression.append(logic.to_cnf(logic.Expr("<=>", step1, atLeastOne(sequence))))
        actions1 = list()
        time = steps
        actions1.append(logic.PropSymbolExpr("North", time))
        actions1.append(logic.PropSymbolExpr("West", time))
        actions1.append(logic.PropSymbolExpr("South", time))
        actions1.append(logic.PropSymbolExpr("East", time))
        expression.append(exactlyOne(actions1))
        expression.append(logic.PropSymbolExpr("P", problem.getGoalState()[0], problem.getGoalState()[1], steps))
        if logic.pycoSAT(expression) != False :
            return extractActionSequence(logic.pycoSAT(expression), ['North', 'East', 'South', 'West'])
        expression.pop()
    return 0

def foodLogicPlan(problem):
    """
    Given an instance of a FoodSearchProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    expression = list()
    for x in range(1, problem.getWidth() + 1) :
        for y in range(1, problem.getHeight() + 1) :
            if (x, y) == problem.getStartState()[0] :
                expression.append(logic.PropSymbolExpr("P", problem.getStartState()[0][0], problem.getStartState()[0][1], 0))
            else :
                expression.append(logic.Expr("~", logic.PropSymbolExpr("P", x, y, 0)))
    for steps in range(50) :
        for x in range(1, problem.getWidth() + 1) :
            for y in range(1, problem.getHeight() + 1) :
                position = ((x, y), problem.getStartState()[1])
                time = steps
                step1 = logic.PropSymbolExpr("P", position[0][0], position[0][1], time + 1)
                sequence = list()
                for action in problem.actions(position) :
                    if action == "North" :
                        move = "South"
                    elif action == "West" :
                        move = "East"
                    elif action == "South" :
                        move = "North"
                    else :
                        move = "West"
                    step2 = logic.PropSymbolExpr(move, time)
                    step3 = logic.PropSymbolExpr("P", problem.result(position, action)[0][0][0], problem.result(position, action)[0][0][1], time)
                    step4 = logic.Expr("&", step2, step3)
                    sequence.append(step4)
                if len(sequence) > 0 :
                    expression.append(logic.to_cnf(logic.Expr("<=>", step1, atLeastOne(sequence))))
        actions1 = list()
        time = steps
        actions1.append(logic.PropSymbolExpr("North", time))
        actions1.append(logic.PropSymbolExpr("West", time))
        actions1.append(logic.PropSymbolExpr("South", time))
        actions1.append(logic.PropSymbolExpr("East", time))
        expression.append(exactlyOne(actions1))
        actions2 = list()
        for x in range(1, problem.getWidth() + 1) :
            for y in range(1, problem.getHeight() + 1) :
                if problem.getStartState()[1][x][y] :
                    for time in range(steps + 1) :
                        actions2.append(logic.PropSymbolExpr("P", x, y, time))
                    expression.append(atLeastOne(actions2))
                    actions2 = list()
        if logic.pycoSAT(expression) != False :
            return extractActionSequence(logic.pycoSAT(expression), ['North', 'East', 'South', 'West'])
        for x in range(problem.getStartState()[1].count()) :
            expression.pop()
    print("ERROR")
    return 0

def foodGhostLogicPlan(problem):
    """
    Given an instance of a FoodGhostSearchProblem, return a list of actions that help Pacman
    eat all of the food and avoid patrolling ghosts.
    Ghosts only move east and west. They always start by moving East, unless they start next to
    and eastern wall. 
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan
fglp = foodGhostLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)



