import socket
from dataclasses import dataclass, field
from typing import List, Optional

from bean.sys.memory_module import MemoryModule
from mag_tools.bean.sys.cpu import Cpu
from mag_tools.bean.sys.disk import Disk
from mag_tools.bean.sys.memory import Memory
from mag_tools.bean.sys.mother_board import Motherboard
from mag_tools.model.computer_type import ComputerType


@dataclass
class Computer:
    """
    计算机类
    """
    type: ComputerType = field(default=None, metadata={"description": "计算机类型"})
    __uuid: Optional[str] = field(default=None, metadata={"description": "计算机标识"})
    name: Optional[str] = field(default=None, metadata={"description": "计算机名"})
    cpu: Optional[Cpu] = field(default=None, metadata={"description": "CPU信息"})
    memory: Optional[Memory] = field(default=None, metadata={"description": "内存信息"})
    memory_modules: List[MemoryModule] = field(default_factory=list, metadata={"description": "内存条信息"})
    disks: List[Disk] = field(default_factory=list, metadata={"description": "磁盘信息"})
    mother_board: Optional[Motherboard] = field(default_factory=list, metadata={"description": "主板信息"})
    description: Optional[str] = field(default_factory=list, metadata={"description": "描述"})

    @classmethod
    def get_info(cls):
        """
        获取当前系统的CPU、内存和磁盘信息，并返回一个Computer实例
        """
        pc = cls(type=ComputerType.DESKTOP,
                 name=socket.gethostname(),
                 cpu=Cpu.get_info(),
                 memory=Memory.get_info(),
                 memory_modules=MemoryModule.get_info(),
                 disks=Disk.get_info(),
                 mother_board=Motherboard.get_info())

        pc.cpu.computer_id = pc.uuid
        pc.mother_board.computer_id = pc.uuid

        for disk in pc.disks:
            disk.computer_id = pc.uuid
        for module in pc.memory_modules:
            module.computer_id = pc.uuid

        return pc

    @property
    def uuid(self) -> str:
        """
        返回计算机对象的ID
        """
        cpu_serial = self.cpu.serial_number if self.cpu else ""
        motherboard_serial = self.mother_board.serial_number if self.mother_board else ""

        self.__uuid = f"{cpu_serial}-{motherboard_serial}"
        return self.__uuid

    def __str__(self):
        """
        返回计算机参数的字符串表示
        """
        parts = [f"Computer(type='{self.type}'"]
        for attr, value in self.__dict__.items():
            if value is not None:
                parts.append(f"{attr}='{value}'")
        parts.append(")")
        return ", ".join(parts)

    def __hash__(self):
        """
        返回计算机对象的哈希值
        """
        cpu_serial = self.cpu.serial_number if self.cpu else ""
        motherboard_serial = self.mother_board.serial_number if self.mother_board else ""
        memory_serials = "".join(
            [module.serial_number for module in self.memory_modules]) if self.memory_modules else ""
        disk_serials = "".join([disk.serial_number for disk in self.disks])

        combined_serials = f"{cpu_serial}{motherboard_serial}{memory_serials}{disk_serials}"
        return hash(combined_serials)


if __name__ == "__main__":
    pc_ = Computer.get_info()
    print(pc_)
