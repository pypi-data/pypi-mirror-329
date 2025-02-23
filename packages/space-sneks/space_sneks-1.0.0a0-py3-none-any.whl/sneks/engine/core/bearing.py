class Bearing:
    """
    TODO
    """

    up: int  #:
    right: int  #:

    def __init__(self, up: int = 0, right: int = 0) -> None:
        self.up = up
        self.right = right

    def __repr__(self) -> str:
        return f"({self.right}, {self.up})"

    def copy(self) -> "Bearing":
        return Bearing(up=self.up, right=self.right)
