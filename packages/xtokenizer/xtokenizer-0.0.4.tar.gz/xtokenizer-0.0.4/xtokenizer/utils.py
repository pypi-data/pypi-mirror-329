import os
import re
import operator
import numpy as np
import pandas as pd
from pathlib import Path
from functools import reduce
from itertools import tee, chain
from typing import List, Union, Iterable, Collection, Tuple
from concurrent.futures import as_completed, ProcessPoolExecutor

UTF8 = "utf-8"
REMOVE_CHARS = "[·’!\"\#$%&'()＃！（）*+,-./:;<=>?\@，。：?￥★、…．＞【】［］《》？“”‘’\[\\]^_`{|}~]+"
REMOVE_CHARS_PATTERN = re.compile(REMOVE_CHARS)
EN_PATTERN = re.compile("[^A-Za-z]+")
EN_CHAR_PATTERN = re.compile(r"([\W])")
CN_CHAR_PATTERN = re.compile(r"([\u4e00-\u9fa5])")


def convert_labels(labels) -> Tuple[np.ndarray, list]:
    """
    :param labels: 待转换的标签，可以是list，也可以是Series，如：['a', 'b', 'c'] 或 pd.Series(['a', 'b', 'c'])
    :return (labels, classes)
    """
    if isinstance(labels, pd.Series):
        labels = labels.astype("category").cat
        return labels.codes.to_numpy(), labels.categories.tolist()
    elif isinstance(labels, np.ndarray):
        classes = np.unique(labels).sort()
        label_mapping = {label: idx for idx, label in enumerate(classes)}
        labels_codes = np.array([label_mapping[label] for label in labels])
        return labels_codes, classes.tolist()
    elif isinstance(labels, list):
        classes = list(set(labels)).sort()
        label_mapping = {label: idx for idx, label in enumerate(classes)}
        labels_codes = np.array([label_mapping[label] for label in labels])
        return labels_codes, classes
    else:
        # 处理polars的Series
        import polars as pl

        if isinstance(labels, pl.Series):
            if not isinstance(labels.dtype, pl.String):
                labels = labels.cast(str)
            labels = labels.cast(pl.Categorical).cat
            return (
                labels.to_local().to_physical().to_numpy().astype(np.int32),
                labels.get_categories().to_list(),
            )
        else:
            raise ValueError(f'参数"labels"类型错误: {type(labels)}')


def get_text_length(
    text: str, lang="cn", cut_type="word", keep_punctuation=False, cut_fn=None
) -> int:
    if cut_fn is None and lang == "cn" and cut_type == "word":
        import jieba
        import logging

        jieba.setLogLevel(logging.INFO)
        cut_fn = jieba.lcut
    cuts = cut(text, lang, cut_type, keep_punctuation, cut_fn=cut_fn)
    return len(cuts)


def get_texts_max_length(
    texts: List[str], lang="cn", cut_type="word", keep_punctuation=False, cut_fn=None
) -> int:
    if cut_fn is None and lang == "cn" and cut_type == "word":
        import jieba
        import logging

        jieba.setLogLevel(logging.INFO)
        cut_fn = jieba.lcut
    batch_cuts = batch_cut(texts, lang, cut_type, keep_punctuation, cut_fn=cut_fn)
    return max(map(lambda s: len(s), batch_cuts))


def get_df_text_labels(
    df, text_col: str, label_col: str, min_length: int = None, max_length: int = None
):
    """Returns (texts, labels, classes)"""

    if min_length or max_length:
        df["length"] = df[text_col].apply(lambda x: get_text_length(x))
    if min_length:
        df = df[df["length"] >= min_length]
    if max_length:
        df = df[df["length"] <= max_length]

    _labels, _classes = convert_labels(df[label_col])
    if isinstance(df, pd.DataFrame):
        _texts = df[text_col].values
    else:
        _texts = df[text_col].to_list()
    return _texts, _labels, _classes


# -----------------------------------------------------------Read file-------------------------------------------------
def read_file(path: Union[str, Path], encoding=UTF8):
    """
    读取文件内容
    :param path: 文件名，不能是文件夹
    :param encoding: 编码
    :return: 包含非空文本行的生成器，如 ['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ...]
    """
    # if Path(path).stat().st_size <= 10000: #1048576000: # 小于等于1G
    with open(path, encoding=encoding) as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()]


def read_large_file(path: Union[str, Path], encoding=UTF8):
    with open(path, encoding=encoding) as f:
        for line in f:
            line = line.strip()
            if line:
                yield line


async def async_read_file(path: Union[str, Path], encoding=UTF8):
    return read_file(path, encoding)


def read_corpus_files(
    path: Union[str, Path],
    encoding=UTF8,
    pattern="*",
    func=read_file,
    async_func=async_read_file,
):
    """
    读取文件或文件夹下所有符合条件的文件
    :param path: 文件或文件夹， 如：'./train.txt'. 如果是文件夹，会读取文件夹下的所有目录和文件.
    :param encoding: 编码
    :param pattern: 当path是文件夹的时候，会根据此后缀过滤文件
    :param func: 具体读取文件的读函数，默认是read_file，可替换。注意：其函数签名为 function_name(path: str, encoding: str) -> corpus: Iterable[str]
    :param async_func: 传入文件夹时的读函数，用协程读取每个文件，默认是async_read_file，可替换。注意：其函数签名为 async function_name(path: str, encoding: str) -> corpus: Iterable[str]
    :return: 非空文本行，如 ['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ...]
    """
    if isinstance(path, str):
        path = Path(path)

    if path.is_file():
        return func(path, encoding)

    import asyncio

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(async_func(file, encoding)) for file in path.rglob(pattern)
    ]  # 这里不能用map，否则读不出数据
    wait_coro = asyncio.wait(tasks)
    loop.run_until_complete(wait_coro)
    all_lines = (task.result() for task in tasks)
    loop.close()

    return reduce(operator.iconcat, all_lines, [])


def load_embedding(path: str, is_large_file=False):
    if path.endswith(".bz2"):
        return load_embedding_from_bz2(path, is_large_file)
    return load_embedding_nomal(path, is_large_file)


def load_embedding_from_bz2(path: str, is_large_file=False):
    import bz2

    if is_large_file:
        with bz2.open(path, "r") as f:
            tokens, vecs = _get_token_vecs(f, require_decode_token=True)
        return list(tokens), list(vecs)

    with bz2.open(path, "r") as f:
        lines = f.readlines()
    return _handle_lines(lines, require_decode_token=True)


def load_embedding_nomal(path: str, is_large_file=False):
    if is_large_file:
        with open(path, "r", encoding=UTF8) as f:
            tokens, vecs = _get_token_vecs(f, require_decode_token=False)
        return list(tokens), list(vecs)

    with open(path, "r", encoding=UTF8) as f:
        lines = f.readlines()
    return _handle_lines(lines, require_decode_token=False)


def _get_token_vecs(f, require_decode_token):
    token_vec = (
        _handle_line(line, require_decode_token)
        for line in f
        if len(line.rstrip().split()) > 2
    )
    return zip(*token_vec)


def _handle_lines(lines: Iterable[str], require_decode_token: bool, batch_size=8192):
    if len(lines[0].split()) <= 2:
        lines = lines[1:]

    length = len(lines)
    if length <= (batch_size << 2):
        token_vecs = list(
            map(lambda line: _handle_line(line, require_decode_token), lines)
        )
        tokens, vecs = zip(*token_vecs)
        return list(tokens), list(vecs)

    splits = [lines[i : i + batch_size] for i in range(0, length, batch_size)]
    n_jobs = min(len(splits), os.cpu_count() - 1)
    with ProcessPoolExecutor(n_jobs) as executor:
        results = [
            executor.submit(_order_handle_lines, i, split, require_decode_token)
            for i, split in enumerate(splits)
        ]
        results = [r.result() for r in as_completed(results)]
    results.sort(key=lambda x: x[0], reverse=False)
    results = [r[1] for r in results]
    token_vecs = list(chain(*results))  # [[str,],] => [str,]
    tokens, vecs = zip(*token_vecs)
    return list(tokens), list(vecs)


def _order_handle_lines(order: int, lines: Iterable[str], require_decode_token: bool):
    return order, list(
        map(lambda line: _handle_line(line, require_decode_token), lines)
    )


def _handle_line(line: str, require_decode_token: bool):
    def get_vec(elems):
        return list(map(float, elems))

    elems = line.rstrip().split()
    return elems[0].decode(UTF8) if require_decode_token else elems[0], get_vec(
        elems[1:]
    )


# --------------------------------------------------Token cut----------------------------------------------------------
def cut_char(sentence: str):
    """
    把句子按字分开，不破坏英文结构
    把所有的中文分开，同时希望英文和数字不能被拆分
    """
    parts = EN_CHAR_PATTERN.split(sentence)
    parts = filter(str.strip, parts)
    results = map(_cn_char_handle, parts)
    return list(chain(*results))


def batch_cut(
    text: Collection[str],
    lang="cn",
    cut_type="word",
    keep_punctuation=False,
    cut_fn=None,
):
    """
    多句话批量分词
    :param text: 多句话，即多行
    :param lang: 哪国语言，支持cn和en
    :param cut_type: 按词还是字分，支持word和char
    :param keep_punctuation: 是否保留标点符号
    :param cut_fn
    :return: 分词后的list(2维)
    """
    if lang == "cn":
        replace_char = ""
        if cut_type == "word":
            if keep_punctuation:

                def fn(s):
                    return cut_fn(s.strip())

            else:

                def fn(s):
                    return cut_fn(re.sub(REMOVE_CHARS_PATTERN, replace_char, s.strip()))

        else:
            if cut_fn is None:
                cut_fn = cut_char

            if keep_punctuation:

                def fn(s):
                    return cut_fn(s.strip())

            else:

                def fn(s):
                    return cut_fn(re.sub(REMOVE_CHARS_PATTERN, replace_char, s.strip()))

        return map(fn, text)
        # return [cut_char(re.sub(REMOVE_CHARS_PATTERN, '', line.strip())) for line in text]

    if lang == "en":
        replace_char = " "
        if cut_type == "word":

            def fn(s):
                return (
                    re.sub(REMOVE_CHARS_PATTERN, replace_char, s)
                    .strip()
                    .lower()
                    .split()
                )

        else:
            if keep_punctuation:

                def fn(s):
                    return list(s.strip().lower())

            else:

                def fn(s):
                    return list(re.sub(EN_PATTERN, replace_char, s).strip().lower())

        return map(fn, text)
        # return [fn(line) for line in text]

    raise NotImplementedError(f'暂时未实现"{lang}"的分词功能')


def cut(sentence: str, lang="cn", cut_type="word", keep_punctuation=False, cut_fn=None):
    """
    单句话分词
    :param sentence: 单句话，即一行
    :param lang: 哪国语言，支持cn和en
    :param cut_type: 按词还是字分，支持word和char
    :param keep_punctuation: 是否保留标点符号
    :param cut_fn
    :return: 分词后的list(1维)
    """
    import re

    if lang == "cn":
        replace_char = ""
        if cut_type == "word":
            if keep_punctuation:
                return list(cut_fn(sentence.strip()))
            else:
                return list(
                    cut_fn(re.sub(REMOVE_CHARS_PATTERN, replace_char, sentence.strip()))
                )
        else:
            if cut_fn is None:
                cut_fn = cut_char

            if keep_punctuation:
                return cut_fn(sentence.strip())
            else:
                return cut_fn(
                    re.sub(REMOVE_CHARS_PATTERN, replace_char, sentence.strip())
                )

    if lang == "en":
        replace_char = " "
        if cut_type == "word":
            return (
                re.sub(REMOVE_CHARS_PATTERN, replace_char, sentence)
                .strip()
                .lower()
                .split()
            )
        else:
            if keep_punctuation:
                return list(sentence.strip().lower())
            else:
                return list(re.sub(EN_PATTERN, replace_char, sentence).strip().lower())

    raise NotImplementedError(f'暂时未实现"{lang}"的分词功能')


def filter_stop_words(cut_corpus: Iterable[List[str]], stop_words: Collection[str]):
    return map(
        lambda line: [word for word in line if word not in stop_words], cut_corpus
    )
    # return map(lambda line: list(filter(lambda word: word not in stop_words, line)), cut_corpus)


# -------------------------------------------------pad function--------------------------------------------------------
def pad(
    ids: List[int],
    max_length: int = None,
    truncation=True,
    padding=True,
    padding_side="right",
    bos=False,
    eos=False,
    pad_id=0,
    bos_id=2,
    eos_id=3,
):
    """
    pad token list(1维)
    :return: padded list, valid_size size
    """
    assert padding_side in ("right", "left"), '参数padding_side只能是"right"或"left".'
    size = len(ids)
    if bos and eos:
        size += 2
        if max_length and truncation and size > max_length:
            return [bos_id] + ids[: max_length - 2] + [eos_id], max_length
        if padding and max_length and size < max_length:
            if padding_side == "right":
                return [bos_id] + ids + [eos_id] + [pad_id] * (max_length - size), size
            elif padding_side == "left":
                return [pad_id] * (max_length - size) + [bos_id] + ids + [eos_id], size
            raise ValueError(f'参数"padding_side"错误: {padding_side}')
        return [bos_id] + ids + [eos_id], size
    elif bos:
        size += 1
        if max_length and truncation and size > max_length:
            return [bos_id] + ids[: max_length - 2] + [eos_id], max_length
        if padding and max_length and size < max_length:
            if padding_side == "right":
                return [bos_id] + ids + [pad_id] * (max_length - size), size
            elif padding_side == "left":
                return [pad_id] * (max_length - size) + [bos_id] + ids, size
            raise ValueError(f'参数"padding_side"错误: {padding_side}')
        return [bos_id] + ids, size
    elif eos:
        size += 1
        if max_length and truncation and size > max_length:
            return ids[: max_length - 2] + [eos_id], max_length
        if padding and max_length and size < max_length:
            if padding_side == "right":
                return ids + [eos_id] + [pad_id] * (max_length - size), size
            elif padding_side == "left":
                return [pad_id] * (max_length - size) + ids + [eos_id], size
            raise ValueError(f'参数"padding_side"错误: {padding_side}')
        return ids + [eos_id], size
    else:
        if max_length and truncation and size > max_length:
            return ids[:max_length], max_length
        if padding and max_length and size < max_length:
            if padding_side == "right":
                return ids + [pad_id] * (max_length - size), size
            elif padding_side == "left":
                return [pad_id] * (max_length - size) + ids, size
            raise ValueError(f'参数"padding_side"错误: {padding_side}')
        return ids, size


def batch_pad(
    batch: Union[map, Iterable[Iterable[int]]],
    max_length: int = None,
    truncation=True,
    padding=True,
    padding_side="right",
    bos=False,
    eos=False,
    pad_id=0,
    bos_id=2,
    eos_id=3,
):
    """
    :param batch: (2维)
    :param max_length:
    :param truncation:
    :param padding_side:
    :param bos:
    :param eos:
    :param pad_id:
    :param bos_id:
    :param eos_id:
    :return:
    """
    if not max_length and (truncation or padding):
        batch, batch_copy = tee(batch, 2)
        max_length = max(map(len, batch_copy))
        if bos:
            max_length += 1
        if eos:
            max_length += 1
    ids, sizes = zip(
        *map(
            lambda ids: pad(
                ids,
                max_length,
                truncation,
                padding,
                padding_side,
                bos,
                eos,
                pad_id,
                bos_id,
                eos_id,
            ),
            batch,
        )
    )
    return list(ids), list(sizes)


def _pad_mask(
    ids: Iterable[int],
    max_length: int = None,
    truncation=True,
    padding=True,
    padding_side="right",
    bos=False,
    eos=False,
    pad_id=0,
    bos_id=2,
    eos_id=3,
):
    input_ids, real_size = pad(
        ids,
        max_length,
        truncation,
        padding,
        padding_side,
        bos,
        eos,
        pad_id,
        bos_id,
        eos_id,
    )
    size = len(input_ids)
    if size > real_size:
        if padding_side == "right":
            return input_ids, [1] * real_size + [0] * (size - real_size)
        return input_ids, [0] * (size - real_size) + [1] * real_size
    else:
        return input_ids, [1] * size


def pad_mask(
    ids: Iterable[int],
    max_length: int = None,
    truncation=True,
    padding=True,
    padding_side="right",
    bos=False,
    eos=False,
    pad_id=0,
    bos_id=2,
    eos_id=3,
):
    input_ids, mask_ids = _pad_mask(
        ids,
        max_length,
        truncation,
        padding,
        padding_side,
        bos,
        eos,
        pad_id,
        bos_id,
        eos_id,
    )
    return {"input_ids": input_ids, "mask_ids": mask_ids}


def batch_pad_mask(
    batch: Union[map, Iterable[Iterable[int]]],
    max_length: int = None,
    truncation=True,
    padding=True,
    padding_side="right",
    bos=False,
    eos=False,
    pad_id=0,
    bos_id=2,
    eos_id=3,
):
    if not max_length and (truncation or padding):
        batch, batch_copy = tee(batch, 2)
        max_length = max(map(len, batch_copy))
        if bos:
            max_length += 1
        if eos:
            max_length += 1
    ids = list(
        map(
            lambda ids: _pad_mask(
                ids,
                max_length,
                truncation,
                padding,
                padding_side,
                bos,
                eos,
                pad_id,
                bos_id,
                eos_id,
            ),
            batch,
        )
    )
    input_ids, mask_ids = zip(*ids)
    return {"input_ids": list(input_ids), "mask_ids": list(mask_ids)}


def _cn_char_handle(part):
    chars = CN_CHAR_PATTERN.split(part)
    return filter(str.strip, chars)
