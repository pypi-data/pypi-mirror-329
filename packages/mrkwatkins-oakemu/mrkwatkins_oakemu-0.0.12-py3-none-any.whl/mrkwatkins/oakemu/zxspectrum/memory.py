from MrKWatkins.OakEmu import Memory as DotNetMemory  # noqa
from MrKWatkins.OakEmu import StateSerializer as DotNetStateSerializer  # noqa


class Memory:
    def __init__(self, memory: DotNetMemory):
        self._memory = memory

    def __getitem__(self, index):
        if index < 0 or index > 65535:
            raise IndexError(f"index {index} is not in the range 0 - 65535")

        return self._memory[index]

    def __setitem__(self, index, value):
        if index < 0 or index > 65535:
            raise IndexError(f"Index {index} is not in the range 0 - 65535")
        if value < 0 or value > 255:
            raise OverflowError(f"value {value} is not in the range 0 - 255")

        self._memory[index] = value

    def __getstate__(self):
        state = {
            "_memory": bytes(DotNetStateSerializer.Save(self._memory)),
        }
        return state

    def __setstate__(self, state):
        self._memory = DotNetMemory()
        DotNetStateSerializer.Restore[DotNetMemory](self._memory, state["_memory"])
