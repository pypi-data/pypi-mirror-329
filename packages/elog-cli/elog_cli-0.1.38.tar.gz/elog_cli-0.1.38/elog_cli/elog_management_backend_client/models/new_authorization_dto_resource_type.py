from enum import Enum


class NewAuthorizationDTOResourceType(str, Enum):
    ALL = "All"
    GROUP = "Group"
    LOGBOOK = "Logbook"

    def __str__(self) -> str:
        return str(self.value)
