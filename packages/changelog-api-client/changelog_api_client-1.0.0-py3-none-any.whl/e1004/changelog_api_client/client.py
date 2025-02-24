from dataclasses import dataclass
from datetime import date
from typing import Self
from uuid import UUID

from realerikrani.baseclient import BaseClient

from .model import Change, Version, VersionsPage


@dataclass
class ChangelogClient:
    http_client: BaseClient

    def create_version(self: Self, version_number: str) -> Version:
        url = f"{self.http_client.url}/versions"
        response = self.http_client.post(
            url, data={"version_number": version_number}
        ).json()
        return Version.make(response["version"])

    def delete_version(self: Self, version_number: str) -> Version:
        url = f"{self.http_client.url}/versions/{version_number}"
        response = self.http_client.delete(url).json()
        return Version.make(response["version"])

    def release_version(self: Self, version_number: str, released_at: date) -> Version:
        url = f"{self.http_client.url}/versions/{version_number}"
        response = self.http_client.patch(
            url, data={"released_at": released_at.isoformat()}
        ).json()
        return Version.make(response["version"])

    def read_versions(
        self: Self, page_size: int | None, page_token: str | None
    ) -> VersionsPage:
        url = f"{self.http_client.url}/versions"

        if page_size:
            url += f"?page_size={page_size}"
        if page_token and page_size:
            url += f"&page_token={page_token}"
        elif page_token:
            url += f"?page_token={page_token}"

        response = self.http_client.get(url).json()
        return VersionsPage(
            versions=[Version.make(v) for v in response["versions"]],
            prev_token=response["previous_token"],
            next_token=response["next_token"],
        )

    def create_change(
        self: Self, version_number: str, kind: str, body: str, author: str
    ) -> Change:
        url = f"{self.http_client.url}/versions/{version_number}/changes"
        response = self.http_client.post(
            url, data={"kind": kind, "body": body, "author": author}
        ).json()
        return Change.make(response["change"])

    def delete_change(self: Self, version_number: str, change_id: UUID) -> Change:
        url = f"{self.http_client.url}/versions/{version_number}/changes/{change_id}"
        response = self.http_client.delete(url).json()
        return Change.make(response["change"])

    def read_changes(self: Self, version_number: str) -> list[Change]:
        url = f"{self.http_client.url}/versions/{version_number}/changes"
        response = self.http_client.get(url).json()
        return [Change.make(c) for c in response["changes"]]

    def move_change_to_other_version(
        self: Self, from_version_number: str, to_version_number: str, change_id: UUID
    ) -> Change:
        url = (
            f"{self.http_client.url}/versions/{from_version_number}/changes/{change_id}"
        )
        response = self.http_client.patch(
            url, data={"version_number": to_version_number}
        ).json()
        return Change.make(response["change"])
