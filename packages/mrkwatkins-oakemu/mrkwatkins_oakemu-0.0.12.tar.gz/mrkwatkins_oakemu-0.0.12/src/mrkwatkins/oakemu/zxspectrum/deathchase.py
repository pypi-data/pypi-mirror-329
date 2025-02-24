from enum import IntEnum

from MrKWatkins.OakEmu import StateSerializer as DotNetStateSerializer  # noqa
from MrKWatkins.OakEmu.Machines.ZXSpectrum.Games import Deathchase as DotNetDeathchase  # noqa
from MrKWatkins.OakEmu.Machines.ZXSpectrum.Screen import ScreenType as DotNetZXSpectrumScreenType  # noqa

from mrkwatkins.oakemu.zxspectrum.game import Game
from mrkwatkins.oakemu.zxspectrum.screen import ScreenType


class DeathchaseAction(IntEnum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    ACCELERATE = 3
    ACCELERATE_LEFT = 4
    ACCELERATE_RIGHT = 5
    DECELERATE = 6
    DECELERATE_LEFT = 7
    DECELERATE_RIGHT = 8
    FIRE = 9
    FIRE_LEFT = 10
    FIRE_RIGHT = 11
    FIRE_ACCELERATE = 12
    FIRE_ACCELERATE_LEFT = 13
    FIRE_ACCELERATE_RIGHT = 14


class Deathchase(Game):
    def __init__(self, screen_type: ScreenType = ScreenType.FAST):
        self._deathchase = DotNetDeathchase(DotNetZXSpectrumScreenType(screen_type))
        super().__init__(self._deathchase, DeathchaseAction)

    @property
    def lives(self) -> int:
        return self._deathchase.Lives

    @lives.setter
    def lives(self, value: int):
        self._deathchase.Lives = value

    def start_episode(self) -> None:
        self._game.StartEpisode()

    @property
    def stop_on_crash(self) -> int:
        return self._deathchase.StopOnCrash

    @stop_on_crash.setter
    def stop_on_crash(self, value: int):
        self._deathchase.StopOnCrash = value

    def __getstate__(self):
        state = {
            "_deathchase": bytes(DotNetStateSerializer.Save(self._deathchase)),
        }
        return state

    def __setstate__(self, state):
        self._deathchase = DotNetDeathchase()
        DotNetStateSerializer.Restore[DotNetDeathchase](self._deathchase, state["_deathchase"])

        super().__init__(self._deathchase, DeathchaseAction, False)
