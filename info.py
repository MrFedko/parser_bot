from dataclasses import dataclass


@dataclass
class Bots:
    name: str
    token: str
    chat_id: str
    yandex: str
    two_gis: str


parser_bot = Bots('name_of_bot', 'token_bot', 'channel id',
                  "yandex link",
                  "2gis link")
