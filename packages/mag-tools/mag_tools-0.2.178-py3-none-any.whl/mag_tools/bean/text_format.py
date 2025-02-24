from dataclasses import dataclass, field
from typing import Optional, Any

from mag_tools.bean.data_format import DataFormat
from mag_tools.model.justify_type import JustifyType

@dataclass
class TextFormat:
    number_per_line: Optional[int] = field(default=1, metadata={"description": "每行显示的数据个数"})
    justify_type: Optional[JustifyType] = field(default=None, metadata={"description": "对齐方式"})
    at_header: Optional[str] = field(default='', metadata={"description": "句首添加的字符串"})
    decimal_places: Optional[int] = field(default=2, metadata={"description": "小数位数"})
    decimal_places_of_zero: Optional[int] = field(default=1, metadata={"description": "小数为0时的小数位数"})
    pad_length: Optional[int] = field(default=None, metadata={"description": "字段显示长度，为 None 表示各字段自行定义"})
    scientific: bool = field(default=False, metadata={"description": "是否使用科学计数法"})

    def __str__(self):
        """
        返回 TextFormat 实例的字符串表示。
        :return: TextFormat 实例的字符串表示。
        """
        return f"TextFormat({', '.join(f'{key}={value}' for key, value in vars(self).items())})"

    def get_data_format(self, pad_length: int) -> DataFormat:
        map_= {
            "justify_type": self.justify_type,
            "decimal_places": self.decimal_places,
            "decimal_places_of_zero": self.decimal_places_of_zero,
            "pad_length": pad_length,
            "scientific": self.scientific
        }
        return DataFormat(**map_)

    def get_data_format_by_value(self, value: Any) -> Optional[DataFormat]:
        return self.get_data_format(len(str(value))) if value else None