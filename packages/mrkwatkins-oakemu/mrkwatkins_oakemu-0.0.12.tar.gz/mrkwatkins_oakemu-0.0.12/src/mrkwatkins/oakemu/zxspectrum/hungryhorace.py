from enum import IntEnum

from MrKWatkins.OakEmu import StateSerializer as DotNetStateSerializer  # noqa
from MrKWatkins.OakEmu.Machines.ZXSpectrum.Games import HungryHorace as DotNetHungryHorace  # noqa
from MrKWatkins.OakEmu.Machines.ZXSpectrum.Screen import ScreenType as DotNetZXSpectrumScreenType  # noqa

from mrkwatkins.oakemu.zxspectrum.game import Game
from mrkwatkins.oakemu.zxspectrum.screen import ScreenType


class HungryHoraceAction(IntEnum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class HungryHorace(Game):
    def __init__(self, screen_type: ScreenType = ScreenType.FAST):
        self._hungry_horace = DotNetHungryHorace(DotNetZXSpectrumScreenType(screen_type))
        super().__init__(self._hungry_horace, HungryHoraceAction)

    @property
    def lives(self) -> int:
        return self._hungry_horace.Lives

    @lives.setter
    def lives(self, value: int):
        self._hungry_horace.Lives = value

    def start_episode(self) -> None:
        self._game.StartEpisode()

    @property
    def stop_on_death(self) -> int:
        return self._hungry_horace.StopOnDeath

    @stop_on_death.setter
    def stop_on_death(self, value: int):
        self._hungry_horace.StopOnDeath = value

    def __getstate__(self):
        state = {
            "_hungry_horace": bytes(DotNetStateSerializer.Save(self._hungry_horace)),
        }
        return state

    def __setstate__(self, state):
        self._hungry_horace = DotNetHungryHorace()
        DotNetStateSerializer.Restore[DotNetHungryHorace](self._hungry_horace, state["_hungry_horace"])

        super().__init__(self._hungry_horace, HungryHoraceAction, False)
