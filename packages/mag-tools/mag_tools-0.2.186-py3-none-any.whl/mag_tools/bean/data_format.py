from dataclasses import dataclass
from typing import Optional
from mag_tools.model.justify_type import JustifyType

@dataclass
class DataFormat:
    justify_type: JustifyType = JustifyType.LEFT
    decimal_places: int = 2
    decimal_places_of_zero: int = 1
    pad_length: Optional[int] = None
    scientific: bool = False

    def __str__(self):
        """
        返回 DataFormat 实例的字符串表示。
        :return: DataFormat 实例的字符串表示。
        """
        return f"DataFormat({', '.join(f'{key}={value}' for key, value in vars(self).items())})"