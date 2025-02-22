from enum import Enum


class AuthorizationDTOOwnerType(str, Enum):
    GROUP = "Group"
    TOKEN = "Token"
    USER = "User"

    def __str__(self) -> str:
        return str(self.value)
