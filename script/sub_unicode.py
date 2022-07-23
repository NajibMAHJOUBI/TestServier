
import re


def sub_unicode(s: str) -> str:
    return re.sub(r'(\\xc3)|(\\x28)', '', s)
