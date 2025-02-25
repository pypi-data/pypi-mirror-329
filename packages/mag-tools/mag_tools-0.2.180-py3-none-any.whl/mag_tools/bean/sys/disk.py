from dataclasses import dataclass
from typing import Optional

import wmi

from mag_tools.model.disk_type import DiskType
from mag_tools.utils.security.digest import Digest


@dataclass
class Disk:
    """
    磁盘参数类
    """
    computer_id: Optional[str] = None    # 所属计算机的标识
    serial_number: Optional[str] = None   # 序列号
    disk_type: Optional[DiskType] = None # 磁盘类型
    model: Optional[str] = None     # 型号
    media_type: Optional[str] = None    # 介质类型
    manufacturer: Optional[str] = None  # 制造商
    capacity: Optional[int] = None    # 总容量，单位为G

    @property
    def hash(self):
        return Digest.md5(f'{self.serial_number}{self.disk_type}{self.model}{self.manufacturer}{self.capacity}')

    @classmethod
    def get_info(cls):
        physical_disks = []
        c = wmi.WMI()
        for disk in c.Win32_DiskDrive():
            manufacturer, dick_type = cls.__parse(disk.Model)

            info = cls(serial_number=disk.DeviceID,
                       disk_type=dick_type,
                       model=disk.Model,
                       capacity=int(disk.Size) // 1000**3,
                       media_type=disk.MediaType,
                       manufacturer=manufacturer)
            physical_disks.append(info)

        return physical_disks

    def __str__(self):
        """
        返回磁盘参数的字符串表示
        """
        attributes = [f"{attr.replace('_', ' ').title()}: {getattr(self, attr)}" for attr in vars(self) if
                      getattr(self, attr) is not None]
        return ", ".join(attributes)

    @classmethod
    def __parse(cls, model):
        items = model.split()
        manufacturer = items[0] if len(items) > 0 else None
        dick_type = DiskType.of_code(items[1]) if len(items) > 1 else None

        return manufacturer, dick_type