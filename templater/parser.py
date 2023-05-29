import datetime
from .classes import UserInfo, Item, Plan, NamedList


async def user_parser(text: str) -> UserInfo:
    arguments = text.split('\n')
    if len(arguments) != 7:
        raise ValueError

    date = datetime.date(*reversed([int(x) for x in arguments[2].split('.')]))
    return UserInfo(
        arguments[0],
        int(arguments[1]),
        date,
        arguments[3],
        arguments[4],
        arguments[5],
        date.year,
        arguments[6]
    )


async def item_parser(text: str) -> Item:
    arguments = text.split('/sep')
    if len(arguments) != 2:
        raise ValueError

    return Item(*arguments)


async def plan_parser(text: str) -> Plan:
    arguments = text.split('/sep')
    if len(arguments) != 2:
        raise ValueError

    return Plan(
        arguments[0],
        datetime.date(*reversed([int(x) for x in arguments[1].split('.')]))
    )


async def named_list_parser(text: str) -> NamedList:
    arguments = text.split('\n')
    if len(arguments) < 1:
        raise ValueError

    items = []
    if len(arguments) != 1:
        items = arguments[1:]

    return NamedList(
        arguments[0],
        items
    )


async def base_parser(text: str) -> str:
    for char in ['\\', '$', '&', '%', '#', '_', '{', '}', '~,' '^']:
        text = text.replace(char, '\\' + char)
    words = text.split()
    res = []
    for word in words:
        if word.startswith('http'):
            res.append(word)

    for word in res:
        text = text.replace(word, f'\\href{{{word}}}{{{word}}}')
    return text
