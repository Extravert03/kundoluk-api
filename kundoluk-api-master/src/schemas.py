import enum
from typing import Optional

from pydantic import BaseModel


class AuthCredentials(BaseModel):
    login: str
    password: str


class GeneratedToken(BaseModel):
    token: str


class JournalMarksRow(BaseModel):
    date: str
    has_attached_homework: bool
    mark: str
    caption: Optional[str]


class JournalMarks(BaseModel):
    mark_rows: tuple[JournalMarksRow, ...]
    student_id: int
    lesson_id: int
    student_name: str
    average: Optional[str] = None


class Quarter(str, enum.Enum):
    CURRENT = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    TOTAL = 5
