from dataclasses import dataclass
import typing
import datetime


@dataclass
class UserInfo:
    student: str
    group: int
    date: datetime.date
    advisor: str
    advisor_title: str
    advisor_affiliation: str
    year: int
    title: str


@dataclass
class Item:
    name: str
    text: str


@dataclass
class Plan:
    action: str
    date: datetime.date


@dataclass
class NamedList:
    name: str
    items: typing.List[str]
