import re


def is_all_english_chars(s):
    return bool(re.match(r'^[A-Za-z]+$', s))


def contains_chinese_chars(s):
    return bool(re.search(r'[\u3400-\u9fff]', s))
