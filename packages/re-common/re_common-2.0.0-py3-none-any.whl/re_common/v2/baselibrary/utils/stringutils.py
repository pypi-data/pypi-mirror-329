import unicodedata


def bj2qj(src):
    if src is None:
        return src

    DBC_SPACE = ' '
    SBC_SPACE = '　'
    DBC_CHAR_START = 33
    DBC_CHAR_END = 126
    CONVERT_STEP = 65248

    buf = []
    for char in src:
        if char == DBC_SPACE:
            buf.append(SBC_SPACE)
        elif DBC_CHAR_START <= ord(char) <= DBC_CHAR_END:
            buf.append(chr(ord(char) + CONVERT_STEP))
        else:
            buf.append(char)

    return ''.join(buf)

def qj2bj(src):
    """
    全角转半角
    :param src:
    :return:
    """
    if src is None:
        return src

    SBC_CHAR_START = 0xFF01
    SBC_CHAR_END = 0xFF5E
    CONVERT_STEP = 0xFEE0
    DBC_SPACE = ' '
    SBC_SPACE = '　'

    buf = []
    for char in src:
        if SBC_CHAR_START <= ord(char) <= SBC_CHAR_END:
            buf.append(chr(ord(char) - CONVERT_STEP))
        elif char == SBC_SPACE:
            buf.append(DBC_SPACE)
        else:
            buf.append(char)

    return ''.join(buf)


def get_diacritic_variant(char1):
    # 将字符转换为标准的 Unicode 形式
    normalized_char1 = unicodedata.normalize('NFD', char1)

    # 获取基本字符（去掉变音符号）
    base_char1 = ''.join(c for c in normalized_char1 if unicodedata.category(c) != 'Mn')

    # 判断基本字符是否相同
    return base_char1