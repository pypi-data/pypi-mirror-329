from dataclasses import dataclass, field
from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from mag_tools.exception.app_exception import AppException
from mag_tools.model.service_status import ServiceStatus

T = TypeVar('T')


@dataclass
class Results(Generic[T]):
    code: Optional[ServiceStatus] = None
    message: Optional[str] = None
    data: Optional[List[T]] = field(default_factory=list)
    total_count: Optional[int] = None
    timestamp: Optional[datetime] = field(default_factory=datetime.now)

    @staticmethod
    def exception(ex: Exception):
        message = str(ex) if ex.args else str(ex.__cause__)
        return Results(code=ServiceStatus.INTERNAL_SERVER_ERROR, message=message)

    @staticmethod
    def success(data: Optional[List[T]] = None):
        return Results(message="OK", data=data)

    @staticmethod
    def fail(message: str):
        return Results(message=message)

    @property
    def is_success(self) -> bool:
        return self.code == ServiceStatus.OK.code

    @property
    def size(self) -> int:
        return len(self.data)

    @property
    def first(self) -> Optional[T]:
        return self.data[0] if self.data and len(self.data) > 0 else None

    def check(self) -> None:
        if not self.is_success:
            raise AppException(self.message)

    def get(self, idx: int) -> Optional[T]:
        self.check()
        return self.data[idx] if idx < self.size else None
    #
    # def to_dict(self):
    #     return {
    #         'code': self.code.code,
    #         'message': self.message,
    #         'timestamp': self.timestamp,
    #         'data': self.data,
    #         'totalCount': self.total_count
    #     }