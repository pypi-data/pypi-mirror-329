from __future__ import annotations
from enum import Enum

type Resample = Resample_Count | Resample_Spacing | Resample_MaxSpacing

class DeviationMode(Enum):
    Point = 0
    Plane = 1

class SelectOp(Enum):
    Add=0
    Remove=1
    Keep=2