from enum import Enum


class DeviceDetailsSortColumn(str, Enum):
    ID = "id"
    NAME = "name"
    TYPE = "type"
    TAGS = "tags"
    ENABLED = "enabled"

    def __str__(self) -> str:
        return str(self.value)
