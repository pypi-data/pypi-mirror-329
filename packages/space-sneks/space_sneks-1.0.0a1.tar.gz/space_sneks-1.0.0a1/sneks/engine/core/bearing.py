class Bearing:
    """
    Represents the directional speeds of a snek. The speeds are represented
    as integers to show the vertical and horizontal speeds in cells per
    game tick.

    Sneks start with a bearing of `(0, 0)`. For example, if the action from
    `get_next_action()` is `Action.UP`, the snek will increase the speed vertically
    by one, so on the next game step the bearing will be `(0, 1)`, and the snek will
    have moved one cell.
    """

    up: int  #:
    right: int  #:

    def __init__(self, up: int = 0, right: int = 0) -> None:
        self.up = up
        self.right = right

    def __repr__(self) -> str:
        return f"({self.right}, {self.up})"
