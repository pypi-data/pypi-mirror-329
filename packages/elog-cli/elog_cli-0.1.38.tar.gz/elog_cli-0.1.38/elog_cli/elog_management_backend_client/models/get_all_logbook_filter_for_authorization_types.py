from enum import Enum


class GetAllLogbookFilterForAuthorizationTypes(str, Enum):
    ADMIN = "Admin"
    READ = "Read"
    WRITE = "Write"

    def __str__(self) -> str:
        return str(self.value)
