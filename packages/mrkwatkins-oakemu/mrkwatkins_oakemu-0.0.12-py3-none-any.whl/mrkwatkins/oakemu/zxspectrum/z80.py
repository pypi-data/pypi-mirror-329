from MrKWatkins.OakEmu.Cpus.Z80 import Z80Emulator as DotNetZ80Emulator  # noqa
from MrKWatkins.OakEmu import StateSerializer as DotNetStateSerializer  # noqa

from mrkwatkins.oakemu.zxspectrum.registers import Registers


class Z80:
    def __init__(self, z80_emulator: DotNetZ80Emulator):
        if not isinstance(z80_emulator, DotNetZ80Emulator):
            raise TypeError("z80_emulator is not a MrKWatkins.OakEmu.Cpus.Z80.Z80Emulator.")

        self._z80_emulator = z80_emulator
        self._registers = Registers(self._z80_emulator.Registers)

    @property
    def registers(self):
        return self._registers

    def __getstate__(self):
        state = {
            "_z80_emulator": bytes(DotNetStateSerializer.Save(self._z80_emulator)),
        }
        return state

    def __setstate__(self, state):
        self._z80_emulator = DotNetZ80Emulator()
        DotNetStateSerializer.Restore[DotNetZ80Emulator](self._z80_emulator, state["_z80_emulator"])

        self._registers = Registers(self._z80_emulator.Registers)
