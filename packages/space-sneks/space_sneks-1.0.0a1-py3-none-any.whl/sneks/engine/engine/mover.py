import abc
from collections import deque
from dataclasses import dataclass

from sneks.engine.core.bearing import Bearing
from sneks.engine.core.cell import Cell
from sneks.engine.core.direction import Direction
from sneks.engine.engine.cells import get_absolute_by_offset, get_absolute_neighbor
from sneks.engine.engine.velocity import Velocity
from sneks.engine.interface.snek import Snek


@dataclass(frozen=True)
class NormalizedScore:
    crashes: float
    distance: float
    raw: "Score"

    def total(self) -> float:
        return self.crashes + self.distance

    def __repr__(self):
        return (
            f"crashes': {self.crashes:.4f}, distance': {self.distance:.4f} "
            f"crashes: {self.raw.crashes:2d}, distance: {self.raw.distance:.2f} "
            f"name: {self.raw.name}"
        )


@dataclass(frozen=True)
class Score:
    name: str
    crashes: int
    distance: float

    def normalize(self, min_score: "Score", max_score: "Score") -> NormalizedScore:
        return NormalizedScore(
            crashes=(min_score.crashes - self.crashes)
            / max(1, (min_score.crashes - max_score.crashes)),
            distance=(self.distance - min_score.distance)
            / max(1.0, (max_score.distance - min_score.distance)),
            raw=self,
        )


class BaseMover(abc.ABC):
    def move(self) -> None:
        raise NotImplementedError


class Mover(BaseMover):
    name: str
    color: tuple[int, int, int]
    snek: Snek
    max_age: int = 0
    crashes: int = 0
    distance: float = 0.0
    tail: deque[Cell]
    head: Cell
    velocity: Velocity

    def __init__(self, name: str, head: Cell, snek: Snek, color: tuple[int, int, int]):
        self.name = name
        self.color = color
        self.snek = snek

        self.reset(head=head)

    def reset(self, head: Cell) -> None:
        self.head = head
        self.tail = deque()
        self.velocity = Velocity()
        self.tail.append(head)

    def get_head(self) -> Cell:
        return self.head

    def move(self):
        next_action = self.snek.get_next_action()
        self.velocity.add(next_action)

        next_head = self.get_head()

        ups = abs(self.velocity.azimuth.up)
        rights = abs(self.velocity.azimuth.right)

        while ups > 0 or rights > 0:
            if ups > 0:
                next_direction = (
                    Direction.UP if self.velocity.azimuth.up > 0 else Direction.DOWN
                )
                next_head = get_absolute_neighbor(next_head, next_direction)
                self.tail.append(next_head)
                ups -= 1
            if rights > 0:
                next_direction = (
                    Direction.RIGHT
                    if self.velocity.azimuth.right > 0
                    else Direction.LEFT
                )
                next_head = get_absolute_neighbor(next_head, next_direction)
                self.tail.append(next_head)
                rights -= 1

        while len(self.tail) > 3 * max(
            1, abs(self.velocity.azimuth.up) + abs(self.velocity.azimuth.right)
        ):
            self.tail.popleft()
        self.distance += self.head.get_distance(next_head)
        self.head = next_head

    def get_score(self) -> Score:
        return Score(
            name=self.name,
            crashes=self.crashes,
            distance=self.distance,
        )


class Asteroid(BaseMover):
    cells: set[Cell]
    tail: set[Cell]
    azimuth: Bearing

    def __init__(self, *, cells: list[Cell], azimuth: Bearing) -> None:
        self.cells = set(cells)
        self.tail = set()
        self.azimuth = azimuth

    def move(self) -> None:
        self.cells = {
            get_absolute_by_offset(
                cell=cell, x_offset=self.azimuth.right, y_offset=self.azimuth.up
            )
            for cell in self.cells
        }

        self.tail = set()

        if abs(self.azimuth.up) == 2:
            self.tail.update(
                get_absolute_by_offset(
                    cell=cell, x_offset=0, y_offset=-1 if self.azimuth.up >= 0 else 1
                )
                for cell in self.cells
            )

        if abs(self.azimuth.right) == 2:
            self.tail.update(
                get_absolute_by_offset(
                    cell=cell, x_offset=-1 if self.azimuth.right >= 0 else 1, y_offset=0
                )
                for cell in self.cells
            )
