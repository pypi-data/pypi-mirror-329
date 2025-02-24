from typing import List

import jieba
from datasketch import MinHash


def tokenize(text: str, stopwords=None) -> List[str]:
    """
    分词并移除停用词
    """
    if stopwords is None:
        stopwords = []
    words = jieba.lcut(text)
    # 统计单字符数据 长度，防止结巴分词分不了的单词 将数据分为单个字符
    one_char_size = len([i for i in words if len(i) == 1])
    all_size = len(words)
    # 如果单字符个数超过一定比例 就直接用空格分词
    if all_size != 0 and one_char_size / all_size > 0.6:
        words = [i for i in text.split() if i.strip()]

    # 过滤停用词和空字符
    words = [w for w in words if w not in stopwords and w.strip()]
    return words


def create_minhash(words: List[str], num_perm=128) -> MinHash:
    """
    为分词结果创建 MinHash
    """
    minhash = MinHash(num_perm=num_perm)
    for word in words:
        minhash.update(word.encode("utf-8"))
    return minhash
