import sys
from os import path

from pythonnet import load

sys.path.append(path.join(path.dirname(__file__), "assemblies"))

load("coreclr")

import clr  # noqa: E402

clr.AddReference("MrKWatkins.OakAsm.IO.ZXSpectrum")  # noqa
clr.AddReference("MrKWatkins.OakEmu.Machines.ZXSpectrum")  # noqa
clr.AddReference("MrKWatkins.OakEmu.Machines.ZXSpectrum.Games")  # noqa
