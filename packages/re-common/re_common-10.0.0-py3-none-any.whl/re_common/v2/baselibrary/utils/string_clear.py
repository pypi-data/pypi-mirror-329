import re
import regex

from re_common.v2.baselibrary.utils.stringutils import qj2bj, bj2qj, get_diacritic_variant


class StringClear(object):

    def __init__(self, obj_str):
        self.obj_str = obj_str

    def None_to_str(self):
        if self.obj_str is None:
            self.obj_str = ''
        return self

    def to_str(self):
        self.obj_str = str(self.obj_str)
        return self

    def qj_to_bj(self):
        # 全角变半角
        self.obj_str = qj2bj(self.obj_str)
        return self

    def bj_to_qj(self):
        # 半角变全角
        self.obj_str = bj2qj(self.obj_str)
        return self

    def lower(self):
        self.obj_str = self.obj_str.lower()
        return self

    def upper(self):
        self.obj_str = self.obj_str.upper()
        return self

    def collapse_spaces(self):
        # 移除多余空格,连续多个空格变一个
        self.obj_str = re.sub(r"\s+", " ", self.obj_str)
        return self

    def clear_all_spaces(self):
        # 去除所有空格
        self.obj_str = re.sub("\\s+", "", self.obj_str)
        return self

    def clean_symbols(self):
        """
        清理已知的符号
        """
        self.obj_str = regex.sub(
            "[\\p{P}+~$`^=|<>～`$^+=|<>￥×\\\\*#$^|+%&~!,:.;'/{}()\\[\\]?<> 《》”“-（）。≤《〈〉》—、·―–‐‘’“”″…¨〔〕°■『』℃ⅠⅡⅢⅣⅤⅥⅦⅩⅪⅫ]",
            "",
            self.obj_str)  # \\p{P} 标点符号 后面的是一些其他符号， 也可以用 \p{S} 代替 但是这个很广 可能有误伤
        return self

    def remove_special_chars(self):
        # 移除特殊字符，仅保留字母、数字、空格和汉字 \w 已经包括所有 Unicode 字母 下划线 _ 会被保留
        self.obj_str = re.sub(r"[^\w\s]", "", self.obj_str)
        return self

    def remove_underline(self):
        # 下划线在 \w 中 所以这里独立封装
        self.obj_str = re.sub("[_]", "", self.obj_str)
        return self

    def remove_diacritics(self):
        # 去除音标 转换成字母
        self.obj_str = get_diacritic_variant(self.obj_str)
        return self

    def remove_brackets(self):
        # 移除 方括号里面的内容
        self.obj_str = re.sub("\\[.*?]", "", self.obj_str)
        return self

    def remove_parentheses(self):
        # 移除圆括号的内容
        self.obj_str = re.sub("\\(.*?\\)", "", self.obj_str)
        return self

    def get_str(self):
        return self.obj_str


def rel_clear(str_obj):
    # 为融合数据定制的 清理规则
    return (StringClear(str_obj)
            .None_to_str()  # 空对象转str 防止空对象
            .to_str()  # 防止其他类型传入
            .qj_to_bj()  # 全角转半角
            .remove_special_chars()  # 移除特殊字符，仅保留字母、数字、空格和汉字 \w 已经包括所有 Unicode 字母 下划线 _ 会被保留
            .collapse_spaces()  # 移除多余空格,连续多个空格变一个
            .lower()  # 小写
            .get_str()  # 获取str
            .strip())  # 去掉空格
