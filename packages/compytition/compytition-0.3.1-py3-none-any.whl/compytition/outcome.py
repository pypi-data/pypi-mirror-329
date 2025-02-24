from enum import Enum


class Outcome(Enum):
    """
    Represents the outcome of an event.

    Attributes
    ----------
    WIN : Outcome
        Represents a win outcome.
    LOSE : Outcome
        Represents a lose outcome.
    DRAW : Outcome
        Represents a draw outcome.
    """
    WIN = 1
    LOSE = 2
    DRAW = 3
    
    W = WIN
    L = LOSE
    D = DRAW