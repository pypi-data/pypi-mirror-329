from enum import Enum


class UpdateAuthorizationDTOPermission(str, Enum):
    ADMIN = "Admin"
    READ = "Read"
    WRITE = "Write"

    def __str__(self) -> str:
        return str(self.value)
