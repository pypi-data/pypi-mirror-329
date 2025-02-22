from typing import TypedDict, Literal, NotRequired


class Score(TypedDict):
    fieldLabel: NotRequired[str]
    sortOrder: NotRequired[Literal["asc", "desc"]]
    fieldName: str
