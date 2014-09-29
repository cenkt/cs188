# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        score = sum((max([4 / manhattanDistance(foodPos, newPos) for foodPos in newFood.asList()] + [0]),
                     successorGameState.getScore()))
        from math import pow

        for index, ghost in enumerate(newGhostStates):
            dist_to_ghost = util.manhattanDistance(newPos, ghost.getPosition())
            if newScaredTimes[index] <= 0:
                score -= pow(max(7 - dist_to_ghost, 0), 2)  # run away. the closer to ghost, the lower the score
            else:
                score += pow(max(8 - dist_to_ghost, 0), 2)  # go towards the ghosts
        return score


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 7)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        # the agent-number of Pac-Man is always 0
        PACMAN = 0
        AGENT_COUNT = gameState.getNumAgents()
        is_pacman = lambda agent_number: agent_number % AGENT_COUNT == PACMAN

        def pacman(depth, gameState, agentNumber=PACMAN):

            legal = gameState.getLegalActions(PACMAN)
            if 0 == depth or not legal or gameState.isWin():
                return self.evaluationFunction(gameState), None
            return max([(ghost(depth, gameState.generateSuccessor(PACMAN, action))[0], action) for action in legal])

        def ghost(depth, gameState, agentNumber=1):
            legal = gameState.getLegalActions(agentNumber)
            if not legal or gameState.isLose():
                return self.evaluationFunction(gameState), None
            else:
                action_scores = []
                for action in legal:
                    newGameState = gameState.generateSuccessor(agentNumber, action)
                    if is_pacman(agentNumber + 1):
                        score, _ = pacman(depth - 1, newGameState, PACMAN)
                    else:
                        score, _ = ghost(depth, newGameState, agentNumber + 1)
                    action_scores.append((score, action))
                return min(action_scores)  # tuple (min_score, action)

        return pacman(self.depth, gameState, 0)[1]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 8)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        PACMAN = 0
        AGENT_COUNT = gameState.getNumAgents()
        is_pacman = lambda agent_number: agent_number % AGENT_COUNT == PACMAN
        avg = lambda l: float(sum(l) / float(len(l))) if l else 0

        def pacman(depth, gameState, agent_number=PACMAN):
            # maximizer
            legal = gameState.getLegalActions(PACMAN)
            if 0 == depth or not legal or gameState.isWin():
                return self.evaluationFunction(gameState), None
            return max([(ghost(depth, gameState.generateSuccessor(PACMAN, action))[0], action) for action in legal])

        def ghost(depth, gameState, agent_number=1):
            # minimizer
            legal = gameState.getLegalActions(agent_number)
            if not legal or gameState.isLose():
                return self.evaluationFunction(gameState), None
            else:
                action_scores = []
                for action in legal:
                    newGameState = gameState.generateSuccessor(agent_number, action)
                    if is_pacman(agent_number + 1):
                        score, _ = pacman(depth - 1, newGameState, PACMAN)
                    else:
                        score, _ = ghost(depth, newGameState, agent_number + 1)
                    action_scores.append(score)
                return avg(action_scores), None  # tuple (mean score, None)

        return pacman(self.depth, gameState, 0)[1]


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 9).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    score = currentGameState.getScore()
    position = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()
    foodStates = currentGameState.getFood()
    capsuleStates = currentGameState.getCapsules()


    dist_between = util.manhattanDistance # shortcut

    #
    # contribution of food. the closer to food cluster the better
    #

    half_circum = sum(foodStates.packBits()[:2])
    # ~ the reciprocal distance
    foodEvaluation = sum([half_circum/(dist_between(position, foodPos)+1)/3.5 for foodPos in foodStates.asList()])


    #
    # contribution of ghosts
    #

    area = foodStates.packBits()[:2][0] * foodStates.packBits()[:2][1]
    # uses area to normalize the reciprocal square distance between pacman and edible ghost
    scared_ghost_distance_timer = [min(20, area/(dist_between(position, ghost.getPosition()) + 2) ** 2) for ghost in ghostStates
                                   if ghost.scaredTimer > 0]
    # the further the dangerous ghost the better
    danger_ghost_distance_time = [min(dist_between(position, ghost.getPosition()), 3.5) for ghost in ghostStates if
                                  ghost.scaredTimer <= 0]
    ghost_evaluation = sum(scared_ghost_distance_timer) - sum(danger_ghost_distance_time)


    #
    # contribution of capsule positions
    #

    # look up dictionaries
    cpd = capsule_pacman_dist_reward = {
        0: 10,
        1: 5,
        2: 2,
        3: 1
    }

    cgp = capsule_ghost_dist_panelty = {
        0: 10,
        1: 8,
        2: 2
    }

    ghost_num = len(ghostStates)
    # pacman: the closer to cap the better
    capEvaluation = sum([cpd.get(dist_between(position, capsule), 0) for capsule in capsuleStates])
    # capsule: the further away from ghost the better
    for capsule in capsuleStates:
        for ghost in ghostStates:
            capEvaluation -= cgp.get(dist_between(ghost.getPosition(), capsule), 0)/ghost_num*2

    score += float(ghost_evaluation) + float(foodEvaluation) + 1.9*float(capEvaluation)  # linear combination
    return score

# Abbreviation
better = betterEvaluationFunction

