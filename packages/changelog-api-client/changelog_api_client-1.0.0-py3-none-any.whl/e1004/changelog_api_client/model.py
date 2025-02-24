from dataclasses import dataclass
from datetime import date
from typing import Literal
from uuid import UUID


@dataclass(slots=True)
class Version:
    created_at: date
    project_id: UUID
    number: str
    id: UUID
    released_at: date | None

    @classmethod
    def make(cls: type["Version"], data: dict) -> "Version":
        return cls(
            id=UUID(data["id"]),
            project_id=UUID(data["project_id"]),
            number=data["number"],
            created_at=date.fromisoformat(data["created_at"]),
            released_at=(
                date.fromisoformat(data["released_at"])
                if data["released_at"] is not None
                else None
            ),
        )


@dataclass(slots=True)
class VersionsPage:
    versions: list[Version]
    prev_token: str | None
    next_token: str | None


@dataclass(slots=True)
class Change:
    id: UUID
    version_id: UUID
    body: str
    kind: Literal["added", "changed", "deprecated", "removed", "fixed", "security"]
    author: str

    @classmethod
    def make(cls: type["Change"], data: dict) -> "Change":
        return cls(
            id=UUID(data["id"]),
            version_id=UUID(data["version_id"]),
            body=data["body"],
            kind=data["kind"],
            author=data["author"],
        )
