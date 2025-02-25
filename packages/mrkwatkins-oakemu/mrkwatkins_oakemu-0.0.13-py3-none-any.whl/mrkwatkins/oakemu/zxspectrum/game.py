import typing
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from enum import EnumType, IntEnum
from os import PathLike
from pathlib import Path

import numpy as np
from MrKWatkins.OakEmu import StateSerializer as DotNetStateSerializer  # noqa
from MrKWatkins.OakEmu.Machines.ZXSpectrum import Keys as DotNetKeys  # noqa
from MrKWatkins.OakEmu.Machines.ZXSpectrum.Games import Game as DotNetGame  # noqa
from System import Exception as DotNetException  # noqa

from mrkwatkins.oakemu.zxspectrum.keys import Keys
from mrkwatkins.oakemu.zxspectrum.stepresult import StepResult
from mrkwatkins.oakemu.zxspectrum.zxspectrum import ZXSpectrum

PlayArea = namedtuple("PlayArea", ["left", "top", "width", "height"])


class Game(metaclass=ABCMeta):  # noqa: B024
    def __init__(self, game: DotNetGame, action_type: EnumType, initialize: bool = True):
        if not issubclass(action_type, IntEnum):
            raise TypeError("action is not an IntEnum.")

        if initialize:
            game.InitializeAsync().Wait()

        self._game = game
        self._zx = ZXSpectrum(game.Spectrum)
        self._action_type = action_type
        self._actions = [e for e in action_type]

    @property
    def spectrum(self) -> ZXSpectrum:
        return self._zx

    @property
    def name(self) -> str:
        return self._game.Name

    @property
    def play_area(self) -> PlayArea:
        play_area = self._game.PlayArea
        return PlayArea(int(play_area.Left), int(play_area.Top), int(play_area.Width), int(play_area.Height))

    @property
    def actions(self) -> list:
        return self._actions

    @property
    def action(self):
        return self._action_type(self._game.ActionIndex)

    @action.setter
    def action(self, action):
        self._game.ActionIndex = int(action)

    def reset(self, seed: int | None = None) -> None:
        self._game.Reset(seed)

    def execute_step(self, action) -> StepResult:
        return StepResult(self._game.ExecuteStep(int(action)))

    def get_random_action(self):
        return self._game.GetRandomAction()

    def keys_to_action(self, keys: Keys):
        return self._action_type(self._game.KeysToActionIndex(DotNetKeys(int(keys))))

    def action_to_keys(self, action):
        return Keys(int(self._game.ActionIndexToKeys(int(action))))

    def get_play_area_pixel_colour_screenshot(
        self,
    ) -> np.ndarray[typing.Any, np.dtype[np.float64]]:
        pixel_colours = bytes(self._game.GetPlayAreaScreenshot().ToPixelColourBytes())
        image_array = np.frombuffer(pixel_colours, dtype=np.uint8)
        play_area = self._game.PlayArea
        return image_array.reshape((int(play_area.Height), int(play_area.Width)))

    def get_play_area_rgb_screenshot(self) -> np.ndarray[typing.Any, np.dtype[np.float64]]:
        rgb = bytes(self._game.GetPlayAreaScreenshot().ToRgb24())
        image_array = np.frombuffer(rgb, dtype=np.uint8)
        play_area = self._game.PlayArea
        return image_array.reshape((int(play_area.Height), int(play_area.Width), 3))

    def dump(self, path: str | PathLike, exception: Exception | None = None):
        dot_net_exception = exception if isinstance(exception, DotNetException) else None
        dump = self._game.Dump(dot_net_exception)
        dump_path = str(Path(path))
        dump.SaveHtml(dump_path)

    @abstractmethod
    def __setstate__(self, state):
        pass
