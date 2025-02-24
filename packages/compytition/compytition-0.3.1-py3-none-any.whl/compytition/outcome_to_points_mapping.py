from .outcome import Outcome


class OutcomeToPointsMapping(dict[Outcome, int]):
    """
    A class used to map outcomes to points.

    This class is a dictionary subclass that maps outcomes to points. The outcomes are the keys, and the points are the values.

    Methods
    -------
    __init__(self, ranking: dict[Any, int | str | Rank])
        Initializes the Ranking with a dictionary of ranks.
    """

    def __init__(self, *, win: int = 3, draw: int = 1, lose: int = 0):
        """
        Initializes the OutcomeToPointsMapping with the given points for each outcome.

        Parameters
        ----------

        win : int, optional
            The number of points awarded for a win outcome. Default is 3.
        draw : int, optional
            The number of points awarded for a draw outcome. Default is 1.
        lose : int, optional
            The number of points awarded for a lose outcome. Default is 0.
        """

        self.update({
            Outcome.WIN: win,
            Outcome.LOSE: lose,
            Outcome.DRAW: draw
        })