from enum import Enum
import re

TAG_REGEX = re.compile(r'\w+')


class TextMode(str, Enum):
    HTML = 'html'
    CODE = 'code'
    TEXT = 'text'

    DEFAULT = TEXT
