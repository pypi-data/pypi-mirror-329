# 某些业务中的字符串处理 算是特定场景的工具
import re


def clean_organ_postcode(organ):
    """
    格式化组织名称字符串，移除括号内容并删除独立的6位数字（邮政编码），然后清理标点。

    备注: 该方法替换java 里面的 formatOrgan

    参数:
        organ (str): 输入的组织名称字符串，可能包含括号、分号和邮政编码。

    返回:
        str: 格式化并清理后的组织名称字符串（无独立6位数字）。
    """
    # 如果输入为空，设为空字符串以避免后续操作报错
    if not organ:
        organ = ""

    # 删除方括号和圆括号中的内容（包括括号本身）
    organ = re.sub(r"\[.*?\]", "", organ)  # 非贪婪匹配方括号内容
    organ = re.sub(r"\(.*?\)", "", organ)  # 非贪婪匹配圆括号内容

    # 定义正则表达式，匹配独立的6位数字
    # \b 表示单词边界，确保6位数字是独立的（前后不是字母、数字或下划线）
    organ = re.sub(r"\b[0-9]{6}\b", "", organ)

    # 初始化结果列表，用于存储处理后的组织名称部分
    format_organ = []
    # 按分号分割字符串，生成组织名称的各个部分
    organ_parts = organ.split(";")

    # 遍历每个部分，追加到结果列表
    for temp_organ in organ_parts:
        # 去除首尾多余空格后追加（避免因移除邮编导致的空字符串）
        cleaned_part = temp_organ.strip()
        # 如果首尾是标点符号，则移除
        # 定义标点符号的正则表达式（这里包括常见标点）
        punctuation = r"^[!,.?;:#$%^&*+-]+|[!,.?;:#$%^&*+-]+$"
        cleaned_part = re.sub(punctuation, "", cleaned_part)
        if cleaned_part:  # 只追加非空部分
            format_organ.append(cleaned_part)

    # 用分号连接结果，转换为大写并清理标点
    format_organ = ";".join(format_organ)

    # 返回最终结果并去除首尾空格
    return format_organ.strip()



def get_first_organ(organ):
    if not organ:
        return ""
    organ_list = organ.strip().split(";")
    for organ_one in organ_list:
        organ_one = clean_organ_postcode(organ_one)
        if organ_one:
            return organ_one

    return ""


def get_first_author(author: object) -> object:
    if not author:
        return ""
    au_list = author.strip().split(";")
    for au in au_list:
        au = re.sub("\\[.*?]", "", au)
        au = re.sub("\\(.*?\\)", "", au)
        if au:
            return au
    return ""
