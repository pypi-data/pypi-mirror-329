from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List

from mag_tools.bean.data_format import DataFormat
from mag_tools.bean.text_format import TextFormat
from mag_tools.model.justify_type import JustifyType
from mag_tools.utils.data.string_format import StringFormat


@dataclass
class BaseData:
    _text_format: TextFormat = field(default_factory=lambda: TextFormat(
        number_per_line=4,
        justify_type=JustifyType.LEFT,
        at_header='',
        decimal_places=4,
        decimal_places_of_zero=1
    ), repr=False)
    _data_formats: Dict[str, DataFormat] = field(default_factory=dict, metadata={"description": "数据格式"}, repr=False)

    def __repr__(self):
        field_dict = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        field_str = ', '.join(f"{k}={v}" for k, v in field_dict.items())
        return f"{self.__class__.__name__}({field_str})"

    def set_pad_lengths(self, pad_lengths: dict[str, int]):
        for arg_name, value in pad_lengths.items():
            data_format = self.get_data_format(arg_name)
            if data_format is None:
                data_format = self._text_format.get_data_format_by_value(vars(self).get(arg_name))
                if data_format:
                    self._data_formats[arg_name] = data_format
            if data_format:
                data_format.pad_length = value

    def set_same_pad_length(self, pad_length:int):
        for data_format in self._data_formats.values():
            data_format.pad_length = pad_length

    def set_justify_type(self, justify_type: JustifyType):
        self._text_format.justify_type = justify_type
        for data_format in self._data_formats.values():
            data_format.justify_type = justify_type

    def set_decimal_places(self, decimal_places):
        self._text_format.decimal_places = decimal_places
        for data_format in self._data_formats.values():
            data_format.decimal_places = decimal_places

    def set_decimal_places_of_zero(self, decimal_places_of_zero):
        self._text_format.decimal_places_of_zero = decimal_places_of_zero
        for data_format in self._data_formats.values():
            data_format.decimal_places_of_zero = decimal_places_of_zero

    def set_number_per_line(self, number_per_line):
        self._text_format.number_per_line = number_per_line

    def set_at_header(self, at_header):
        self._text_format.at_header = at_header

    def set_scientific(self, scientific):
        self._text_format.scientific = scientific

    def get_text(self, arg_names: List[str], delimiter: Optional[str] = None) -> str:
        """
        根据参数名数组拼成一个字符串。
        :param arg_names: 类成员变量的名字数组
        :param delimiter: 分隔符
        :return: 拼接后的字符串
        """

        if delimiter is None:
            delimiter = ''

        strings = []
        need_space = False
        for arg_name in arg_names:
            data_format = self.get_data_format(arg_name)
            value_str = str(vars(self).get(arg_name))
            pad_length = max(len(value_str), data_format.pad_length or 0)
            need_space = need_space or pad_length == len(value_str)

            strings.append(StringFormat.pad_value(value_str, pad_length, data_format.justify_type))

        text = (' ' if need_space else '').join(strings)
        if delimiter:
            text = text.rstrip(delimiter)  # 删除末尾的分隔符
        return text

    def get_data_format(self, arg_name: str) -> DataFormat:
        if arg_name not in self._data_formats:
            for name, value in vars(self).items():
                if name not in ['_text_format', '_data_formats']:
                    data_format = self._text_format.get_data_format_by_value(value)
                    if data_format:
                        self._data_formats[name] = data_format

        return self._data_formats.get(arg_name)

    @property
    def to_map(self) -> Dict[str, Any]:
        return {
            k: repr(v) for k, v in self.__dict__.items()
            if not (k.startswith('__') and k.endswith('__')) and k not in {'_text_format', '_data_formats'}
        }

@dataclass
class TestData(BaseData):
    name: str = field(default=None, metadata={"description": "UUID"})
    age: int = field(default=None, metadata={"description": "UUID"})
    height: int = field(default=None, metadata={"description": "UUID"})


if __name__ == '__main__':
    data = TestData(name='xlcao', age=12, height=1)
    print(data)