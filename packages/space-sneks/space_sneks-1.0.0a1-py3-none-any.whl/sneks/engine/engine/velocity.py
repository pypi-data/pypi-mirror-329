from sneks.engine.config.instantiation import config
from sneks.engine.core.action import Action
from sneks.engine.core.bearing import Bearing


class Velocity:
    azimuth: Bearing

    def __init__(self):
        self.azimuth = Bearing()

    def add(self, action: Action) -> None:
        match action:
            case Action.UP:
                self.azimuth.up = min(
                    config.game.directional_speed_limit, self.azimuth.up + 1
                )
            case Action.DOWN:
                self.azimuth.up = max(
                    -1 * config.game.directional_speed_limit, self.azimuth.up - 1
                )
            case Action.LEFT:
                self.azimuth.right = max(
                    -1 * config.game.directional_speed_limit, self.azimuth.right - 1
                )
            case Action.RIGHT:
                self.azimuth.right = min(
                    config.game.directional_speed_limit, self.azimuth.right + 1
                )

    def copy_azimuth(self) -> "Bearing":
        return Bearing(up=self.azimuth.up, right=self.azimuth.right)
