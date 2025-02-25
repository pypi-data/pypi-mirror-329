from enum import IntEnum

from MrKWatkins.OakEmu import StateSerializer as DotNetStateSerializer  # noqa
from MrKWatkins.OakEmu.Machines.ZXSpectrum.Games import ManicMiner as DotNetManicMiner  # noqa
from MrKWatkins.OakEmu.Machines.ZXSpectrum.Screen import ScreenType as DotNetZXSpectrumScreenType  # noqa

from mrkwatkins.oakemu.zxspectrum.game import Game
from mrkwatkins.oakemu.zxspectrum.screen import ScreenType


class ManicMinerAction(IntEnum):
    NONE = 0
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    JUMP_UP = 3
    JUMP_LEFT = 4
    JUMP_RIGHT = 5


class ManicMiner(Game):
    def __init__(self, screen_type: ScreenType = ScreenType.FAST):
        self._manic_miner = DotNetManicMiner(DotNetZXSpectrumScreenType(screen_type))
        super().__init__(self._manic_miner, ManicMinerAction)

    @property
    def cavern(self) -> int:
        return self._manic_miner.Cavern

    @cavern.setter
    def cavern(self, value: int):
        self._manic_miner.Cavern = value

    @property
    def cavern_name(self) -> str:
        return self._manic_miner.CavernName

    @property
    def lives(self) -> int:
        return self._manic_miner.Lives

    @lives.setter
    def lives(self, value: int):
        self._manic_miner.Lives = value

    @property
    def air_supply(self) -> int:
        return int(self._manic_miner.AirSupply)

    @property
    def stop_on_death(self) -> int:
        return self._manic_miner.StopOnDeath

    @stop_on_death.setter
    def stop_on_death(self, value: int):
        self._manic_miner.StopOnDeath = value

    @property
    def stop_on_completed_cavern(self) -> int:
        return self._manic_miner.StopOnCompletedCavern

    @stop_on_completed_cavern.setter
    def stop_on_completed_cavern(self, value: int):
        self._manic_miner.StopOnCompletedCavern = value

    def __getstate__(self):
        state = {
            "_manic_miner": bytes(DotNetStateSerializer.Save(self._manic_miner)),
        }
        return state

    def __setstate__(self, state):
        self._manic_miner = DotNetManicMiner()
        DotNetStateSerializer.Restore[DotNetManicMiner](self._manic_miner, state["_manic_miner"])

        super().__init__(self._manic_miner, ManicMinerAction, False)
