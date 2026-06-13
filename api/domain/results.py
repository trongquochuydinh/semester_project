from dataclasses import dataclass


@dataclass(frozen=True)
class MessageResult:
    message: str
