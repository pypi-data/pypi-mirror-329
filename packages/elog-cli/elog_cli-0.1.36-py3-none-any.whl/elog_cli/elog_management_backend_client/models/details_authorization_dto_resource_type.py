from enum import Enum


class DetailsAuthorizationDTOResourceType(str, Enum):
    ALL = "All"
    GROUP = "Group"
    LOGBOOK = "Logbook"

    def __str__(self) -> str:
        return str(self.value)
