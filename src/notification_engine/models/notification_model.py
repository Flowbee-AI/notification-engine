from pydantic import BaseModel


class NotificationObj(BaseModel):
    contents: dict[str, str]
    headings: dict[str, str]
    data: dict[str, str]
    external_ids: list[str]
