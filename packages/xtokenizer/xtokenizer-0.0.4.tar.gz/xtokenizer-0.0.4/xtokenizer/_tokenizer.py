import gc
import pickle
import torch
from torch.nn import Embedding
from pathlib import Path
from itertools import tee
from typing import Union, List, Collection

from .utils import UTF8, read_file, read_corpus_files, batch_cut, batch_pad_mask, cut, batch_pad, pad, \
	filter_stop_words, pad_mask, load_embedding
from .stats import token_counter


class BaseTokenizer:
	"""
	如果碰到未登录词会报错，不能padding，记住 min_freq = 0，否则易报错；如果没有特殊要求，请使用其子类SimpleTokenizer
	"""
	# SAVE_SEP = '\t'
	RESERVED_TOKENS = []
	
	def __init__(self, path: Union[str, Path] = None, texts: Collection[str] = None,
	             cut_texts: Union[Collection[Collection[str]], Collection[str]] = None, vocab: Collection[str] = None,
	             min_freq=0, special_tokens: Collection[str] = None, lang='cn', cut_type='word',
	             word_freq: bool = False,
	             stop_words: Collection[str] = None, keep_punctuation=False, cut_fn=None):
		"""
		:param path: 语料文件路径，可以是文件也可以是文件夹， 如：'./train.txt'. 如果是文件夹，会读取文件夹下的所有目录和文件.
		:param texts: 语料，每个元素是一句话，如：['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ...]
		:param cut_texts: 语料，每个元素是是分词后的一句话，如：[['上课', '时', '学生', '手机', '响', '个', '不停'], ['家长', '拿', '发票', '让', '老师', '赔']]
		:param vocab: 词表，如：['上课', '学生', '手机', '不停', '，', '老师']
		:param min_freq: 最小词频，小于词词频的词会被忽略，默认是0，所有的词都保留
		:param special_tokens: 保留token, 如 '<pad>', '<unk>'等
		:param lang: 语言 'cn'和'en'
		:param cut_type: 分词类型，只支持'word'和‘char'两种类型
		:param word_freq: 是否统计词频
		:param stop_words: 停用词
		:param keep_punctuation: 是否保留标点符号
		:param cut_fn
		"""
		self.lang = lang
		self.cut_type = cut_type
		self.stop_words = stop_words,
		self.keep_punctuation = keep_punctuation
		if cut_fn is None and lang == 'cn' and cut_type == 'word':
			import jieba
			import logging
			jieba.setLogLevel(logging.INFO)
			self.cut_fn = jieba.lcut
		else:
			self.cut_fn = cut_fn
		
		self.special_tokens = self.RESERVED_TOKENS
		if special_tokens:
			self.special_tokens.extend([token for token in special_tokens if token not in self.RESERVED_TOKENS])
		
		if vocab:
			if stop_words:
				for word in stop_words:
					if word in vocab:
						vocab.remove(word)
			
			if cut_fn is None and lang == 'cn' and cut_type == 'word':
				for word in vocab:
					jieba.add_word(word)
			
			for token in {token for token in self.special_tokens if token in vocab}:
				vocab.remove(token)
			
			self.vocab = self.special_tokens + vocab if isinstance(vocab, List) else list(vocab)
			self.word_to_idx = {k: i for i, k in enumerate(self.vocab)}
			del vocab
			gc.collect()
		
		else:
			if path is not None and texts is None and cut_texts is None:
				texts = read_corpus_files(path)
			
			if texts is not None:
				cut_texts = batch_cut(texts, lang=lang, cut_type=cut_type, keep_punctuation=keep_punctuation,
				                      cut_fn=self.cut_fn)
				del texts
			
			if cut_texts is not None:
				if isinstance(cut_texts, Collection) and isinstance(cut_texts[0], str):
					cut_texts = batch_cut(cut_texts, lang='en', keep_punctuation=keep_punctuation)
				if stop_words:
					cut_texts = filter_stop_words(cut_texts, stop_words)
				counter = token_counter(cut_texts)
				sorted_token_freq = sorted(counter.items(), key=lambda kv: kv[1], reverse=True)
				self.vocab = self.special_tokens.copy()
				if min_freq > 0:
					filter_tokens = filter(lambda kv: kv[1] >= min_freq and kv[0] not in self.vocab,
					                       sorted_token_freq)
				else:
					filter_tokens = filter(lambda kv: kv[0] not in self.vocab, sorted_token_freq)
				
				if word_freq:
					filter_tokens, filter_tokens_copy = tee(filter_tokens, 2)
					self.word_freq = list(filter_tokens_copy)
				self.vocab += list(map(lambda kv: kv[0], filter_tokens))
				self.word_to_idx = {k: i for i, k in enumerate(self.vocab)}
				del sorted_token_freq, counter, cut_texts
				gc.collect()
			
			else:
				raise ValueError('参数file, texts, vocab不能同时为None.')
		
		self.special_token_ids = list(map(self._do_encode, self.special_tokens))
	
	@classmethod
	def from_file(cls, path: Union[str, Path], encoding=UTF8, pattern='*', func=read_file, min_freq: int = None,
	              special_tokens: Collection[str] = None, lang='cn', cut_type='word', word_freq=False,
	              stop_words: Collection[str] = None, keep_punctuation=False, cut_fn=None):
		"""
		:param path: 语料文件，可以是文件也可以是文件夹， 如：'./train.txt'. 如果是文件夹，会读取文件夹下的所有目录和文件.
		:param encoding: 编码
		:param pattern: 文件后缀，当file是文件夹的时候，会根据此后缀过滤文件
		:param func: 具体读取文件的处理函数，默认是read_file，可替换。注意：其函数签名为 function_name(path: str, encoding: str) -> texts: Collection[str]
		:param min_freq: 最小词频，小于词词频的词会被忽略，默认是0，所有的词都保留
		:param special_tokens: 保留token, 如 '<pad>', '<unk>'等
		:param lang: 语言 'cn'和'en'
		:param cut_type: 分词类型，只支持'word'和‘char'两种类型
		:param word_freq: 是否统计词频
		:param stop_words: 停用词
		:param keep_punctuation: 是否保留标点符号
		:param cut_fn
		"""
		texts = read_corpus_files(path, encoding, pattern, func)
		if min_freq is None:
			return cls(texts=texts, special_tokens=special_tokens, lang=lang, cut_type=cut_type,
			           word_freq=word_freq, stop_words=stop_words, keep_punctuation=keep_punctuation, cut_fn=cut_fn)
		return cls(texts=texts, min_freq=min_freq, special_tokens=special_tokens, lang=lang, cut_type=cut_type,
		           word_freq=word_freq, stop_words=stop_words, keep_punctuation=keep_punctuation, cut_fn=cut_fn)
	
	@classmethod
	def from_texts(cls, texts: Collection[str], min_freq: int = None, special_tokens: Collection[str] = None, lang='cn',
	               cut_type='word', word_freq=False, stop_words: Collection[str] = None, keep_punctuation=False,
	               cut_fn=None):
		"""
		:param texts: 语料，每个元素是一句话，如：['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ....]
		:param min_freq: 最小词频，小于词词频的词会被忽略，默认是0，所有的词都保留
		:param special_tokens: 保留token, 如 '<pad>', '<unk>'等
		:param lang: 语言 'cn'和'en'
		:param cut_type: 分词类型，只支持'word'和‘char'两种类型
		:param word_freq: 是否统计词频
		:param stop_words: 停用词
		:param keep_punctuation: 是否保留标点符号
		:param cut_fn
		"""
		if min_freq is None:
			return cls(texts=texts, special_tokens=special_tokens, lang=lang, cut_type=cut_type,
			           word_freq=word_freq, stop_words=stop_words, keep_punctuation=keep_punctuation, cut_fn=cut_fn)
		return cls(texts=texts, min_freq=min_freq, special_tokens=special_tokens, lang=lang, cut_type=cut_type,
		           word_freq=word_freq, stop_words=stop_words, keep_punctuation=keep_punctuation, cut_fn=cut_fn)
	
	@classmethod
	def from_cut_texts(cls, cut_texts: Collection[Collection[str]], min_freq: int = None,
	                   special_tokens: Collection[str] = None, lang='cn', cut_type='word', word_freq=False,
	                   stop_words: Collection[str] = None, keep_punctuation=False, cut_fn=None):
		"""
		:param cut_texts: 分词后的语料，每个元素是一句话，如：[['上课', '时', '学生', '手机', '响', '个', '不停'], ['家长', '拿', '发票', '让', '老师', '赔']]
		:param min_freq: 最小词频，小于词词频的词会被忽略，默认是0，所有的词都保留
		:param special_tokens: 保留token, 如 '<pad>', '<unk>'等
		:param lang: 语言 'cn'和'en'
		:param cut_type: 分词类型，只支持'word'和‘char'两种类型
		:param word_freq: 是否统计词频
		:param stop_words: 停用词
		:param keep_punctuation: 是否保留标点符号
		:param cut_fn
		"""
		if min_freq is None:
			return cls(cut_texts=cut_texts, special_tokens=special_tokens, lang=lang, cut_type=cut_type,
			           word_freq=word_freq, stop_words=stop_words, keep_punctuation=keep_punctuation, cut_fn=cut_fn)
		return cls(cut_texts=cut_texts, min_freq=min_freq, special_tokens=special_tokens, lang=lang, cut_type=cut_type,
		           word_freq=word_freq, stop_words=stop_words, keep_punctuation=keep_punctuation, cut_fn=cut_fn)
	
	@classmethod
	def from_vocab(cls, vocab: Collection[str], special_tokens: Collection[str] = None, lang='cn', cut_type='word',
	               stop_words: Collection[str] = None, keep_punctuation=False, cut_fn=None):
		"""
		:param vocab: 词表，如：['上课', '学生', '手机', '不停', '，', '老师']
		:param special_tokens: 保留token, 如 '<pad>', '<unk>'等
		:param lang: 语言 'cn'和'en'
		:param cut_type: 分词类型，只支持'word'和‘char'两种类型
		:param stop_words: 停用词
		:param keep_punctuation: 是否保留标点符号
		:param cut_fn
		"""
		return cls(vocab=vocab, special_tokens=special_tokens, lang=lang, cut_type=cut_type, stop_words=stop_words,
		           keep_punctuation=keep_punctuation, cut_fn=cut_fn)
	
	@property
	def vocab_size(self):
		return len(self.vocab)
	
	@property
	def real_vocab(self):
		"""
		:return: 除去特殊字符的词表
		"""
		special_token_len = len(self.special_tokens)
		idx = special_token_len - 1
		if self.special_tokens[idx] == self.vocab[idx]:
			return self.vocab[len(self.special_tokens):]
		
		for i in range(idx):
			if self.special_tokens[i] != self.vocab[i]:
				idx = i
				break
		return self.vocab[idx:len(self.vocab) + idx - special_token_len]
	
	def encode(self, sentence: Union[str, Collection[str]], max_length: int = None, truncation=True,
	           is_split_into_words: bool = False):
		"""
		:param sentence: '上课时学生手机响个不停，老师一怒之下把手机摔了'
		:param max_length:
		:param truncation:
		:param is_split_into_words: 是否已经分词
		:return:
		"""
		tokens = self._encode(sentence, is_split_into_words)
		if truncation and max_length:
			return tokens[:max_length]
		return tokens
	
	def _encode(self, sentence: Union[str, Collection[str]], is_split_into_words):
		"""
		:param sentence: '上课时学生手机响个不停，老师一怒之下把手机摔了'
		:param is_split_into_words: 是否已经分词
		:return:
		"""
		if is_split_into_words:
			if isinstance(sentence, str):
				words = cut(sentence, lang='en', keep_punctuation=self.keep_punctuation)
			elif isinstance(sentence, Collection):
				words = sentence
		else:
			if isinstance(sentence, str):
				words = cut(sentence, self.lang, self.cut_type, keep_punctuation=self.keep_punctuation,
				            cut_fn=self.cut_fn)
			else:
				raise ValueError("当参数is_split_into_words为False时，参数'sentence'只能是str类型")
		
		if self.stop_words:
			return self.do_encode_with_stop_words(words)
		else:
			return self.do_encode(words)
	
	def batch_encode(self, sentences: Union[str, Collection[str], Collection[Collection[str]]], max_length: int = None,
	                 truncation=True, is_split_into_words: bool = False):
		"""
		:param sentences: ['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ....]
		:param max_length:
		:param truncation:
		:param is_split_into_words: 是否已经分词
		:return:
		"""
		if isinstance(sentences, str) or (is_split_into_words and isinstance(sentences[0], str)):
			return self.encode(sentences, max_length, truncation, is_split_into_words)
		
		tokens = self._batch_encode(sentences, is_split_into_words)
		if truncation and max_length:
			return [x[:max_length] for x in tokens]
		return list(tokens)
	
	def _batch_encode(self, sentences: Union[Collection[str], Collection[Collection[str]]], is_split_into_words):
		"""
		:param sentences: ['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ....]
		:param is_split_into_words: 是否已经分词
		:return:
		"""
		if isinstance(sentences, Collection):
			if is_split_into_words:
				if self.stop_words:
					return map(self.do_encode_with_stop_words, sentences)
				return map(self.do_encode, sentences)
			else:
				batch_cuts = batch_cut(sentences, lang=self.lang, cut_type=self.cut_type,
				                       keep_punctuation=self.keep_punctuation, cut_fn=self.cut_fn)
				if self.stop_words:
					return map(self.do_encode_with_stop_words, batch_cuts)
				return map(self.do_encode, batch_cuts)
		
		raise ValueError('参数"sentence"类型错误')
	
	def __call__(self, sentences: Union[Collection[str], Collection[Collection]], max_length: int = None,
	             truncation=True,
	             is_split_into_words: bool = False):
		return self.batch_encode(sentences, max_length, truncation, is_split_into_words)
	
	def do_encode(self, words: Union[str, Collection[str]]):
		"""
		把词转换成数字
		:param words: '学生' 或 ['学生', '手机', '老师']
		:return:
		"""
		if isinstance(words, str):
			return self._do_encode(words)
		return list(filter(lambda x: x is not None, map(self._do_encode, words)))
	
	def do_encode_with_stop_words(self, words: Union[str, Collection[str]]):
		"""
		把词转换成数字
		:param words: '学生' 或 ['学生', '手机', '老师']
		:return:
		"""
		if isinstance(words, str):
			return self._do_encode_with_stop_words(words)
		return list(filter(lambda x: x is not None, map(self._do_encode_with_stop_words, words)))
	
	def _do_encode(self, word: str):
		return self.word_to_idx[word]
	
	def _do_encode_with_stop_words(self, cut_token: str):
		return self.word_to_idx[cut_token] if cut_token not in self.stop_words else None
	
	def decode(self, tokens: Union[int, Collection[int]], return_special_tokens=False, return_sentence=False):
		"""
		:param tokens: [2, 19, 27, 3, 0, 0]
		:param return_special_tokens: 是否返回'<pad>', '<unk>', '<bos>', '<eos>'等特殊字符
		:param return_sentence: 返回的是一句话还是词序列
		:return: 由return_sentence决定，返回的是 '上课时学生手机响个不停‘, 还是 ['上课', '时', '学生', '手机', ’响个, '不停']
		"""
		if isinstance(tokens, int):
			return self.vocab[tokens]
		
		if return_sentence:
			return ''.join(self._decode(tokens, return_special_tokens))
		return list(self._decode(tokens, return_special_tokens))
	
	def batch_decode(self, batch_tokens: Collection[Collection[int]], return_special_tokens=False,
	                 return_sentence=False):
		"""
		:param batch_tokens: [[2, 19, 27, 3, 0, 0], [2, 10, 3, 0, 0, 0]]
		:param return_special_tokens: 是否返回'<pad>', '<unk>', '<bos>', '<eos>'等特殊字符
		:param return_sentence: 返回的是一句话还是词序列
		:return: 由return_sentence决定，返回的是 '上课时学生手机响个不停‘, 还是 ['上课', '时', '学生', '手机', ’响个, '不停']
		"""
		if isinstance(batch_tokens[0], int):
			return self.decode(batch_tokens, return_special_tokens, return_sentence)
		return list(map(lambda x: self.decode(x, return_special_tokens, return_sentence), batch_tokens))
	
	def add_special_tokens(self, special_tokens: Collection[str]):
		for token in special_tokens:
			if token in self.special_tokens:
				continue
			self.special_tokens.append(token)
			self.word_to_idx[token] = len(self.vocab)
			if token not in self.vocab:
				self.vocab.append(token)
		self.special_token_ids = list(map(self._do_encode, self.special_tokens))
	
	def add_words(self, words: Union[str, Collection[str]]):
		if isinstance(words, str):
			self.word_to_idx[words] = len(self.vocab)
			self.vocab.append(words)
		else:
			for word in words:
				if word in self.vocab:
					continue
				self.word_to_idx[word] = len(self.vocab)
				self.vocab.append(word)
	
	def add_stop_words(self, stop_words: Collection[str]):
		if not stop_words:
			return
		
		if self.stop_words is None:
			self.stop_words = stop_words if isinstance(self.stop_words, List) else list(stop_words)
			for word in stop_words:
				if word in self.vocab:
					self.vocab.remove(word)
		else:
			if not isinstance(self.stop_words, List):
				self.stop_words = list(self.stop_words)
			
			for word in stop_words:
				if word in self.stop_words:
					continue
				self.stop_words.append(word)
				if word in self.vocab:
					self.vocab.remove(word)
		
		self.word_to_idx = {k: i for i, k in enumerate(self.vocab)}
	
	def save(self, path: str = None):
		path = path or f'{self.__class__.__name__}.bin'
		obj = {
			'name': f'{self.__class__.__name__}',
			'lang': self.lang,
			'cut_type': self.cut_type,
			'keep_punctuation': self.keep_punctuation,
			'special_tokens': self.special_tokens,
			'stop_words': self.stop_words,
			'vocab': self.vocab
		}
		with open(path, 'wb') as f:
			pickle.dump(obj, f)
	
	@classmethod
	def load(cls, path: str = None, cut_fn=None):
		path = path or f'{cls.__name__}.bin'
		with open(path, 'rb') as f:
			obj = pickle.load(f)
		
		tokenizer_name = obj['name']
		assert cls.__name__ == tokenizer_name, f"Expected {tokenizer_name}, but found {cls.__name__}"
		return cls(vocab=obj['vocab'], special_tokens=obj['special_tokens'], lang=obj['lang'], cut_type=obj['cut_type'],
		           stop_words=obj['stop_words'], keep_punctuation=obj['keep_punctuation'], cut_fn=cut_fn)
	
	def _decode(self, tokens: Collection[int], return_special_tokens):
		if return_special_tokens:
			return map(lambda i: self.vocab[i], tokens)
		
		if self.special_tokens:
			return map(lambda i: self.vocab[i], filter(lambda i: i not in self.special_token_ids, tokens))
		
		return map(lambda i: self.vocab[i], tokens)
	
	def __len__(self):
		return self.vocab_size
	
	def __getitem__(self, index):
		return self.vocab[index]


class PaddingTokenizer(BaseTokenizer):
	"""
	如果碰到未登录词会用'<unk>'代替，能padding, '<pad>'和'<unk>'相同
	"""
	UNK = '<UNK>'
	PAD_ID = UNK_ID = 0
	RESERVED_TOKENS = [UNK]
	
	def __init__(self, path: Union[str, Path] = None, texts: Collection[str] = None,
	             cut_texts: Collection[Collection[str]] = None,
	             vocab: Collection[str] = None, min_freq=0, special_tokens: Collection[str] = None, lang='cn',
	             cut_type='word', word_freq: bool = False, stop_words: Collection[str] = None, keep_punctuation=False,
	             cut_fn=None):
		"""
		:param path: 语料文件路径，可以是文件也可以是文件夹， 如：'./train.txt'. 如果是文件夹，会读取文件夹下的所有目录和文件.
		:param texts: 语料，每个元素是一句话，如：['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ...]
		:param cut_texts: 语料，每个元素是是分词后的一句话，如：[['上课', '时', '学生', '手机', '响', '个', '不停'], ['家长', '拿', '发票', '让', '老师', '赔']]
		:param vocab: 词表，如：['上课', '学生', '手机', '不停', '，', '老师']
		:param min_freq: 最小词频，小于词词频的词会被忽略，默认是0，所有的词都保留
		:param special_tokens: 保留token, 如 '<pad>', '<unk>'等
		:param lang: 语言 'cn'和'en'
		:param cut_type: 分词类型，只支持'word'和‘char'两种类型
		:param word_freq: 是否统计词频
		:param stop_words: 停用词
		:param keep_punctuation: 是否保留标点符号
		:param cut_fn
		"""
		super().__init__(path=path, texts=texts, cut_texts=cut_texts, vocab=vocab, min_freq=min_freq,
		                 special_tokens=special_tokens, lang=lang, cut_type=cut_type, word_freq=word_freq,
		                 stop_words=stop_words, keep_punctuation=keep_punctuation, cut_fn=cut_fn)
	
	def encode(self, sentence: str, max_length: int = None, truncation=True, padding=True, padding_side='right',
	           is_split_into_words: bool = False, return_sequence_length=False):
		"""
		:param sentence: '上课时学生手机响个不停，老师一怒之下把手机摔了'
		:param max_length:
		:param truncation:
		:param padding:
		:param padding_side:
		:param is_split_into_words: 是否已经分词
		:param return_sequence_length: 是否返回序列实际长度
		:return: ([id:int], sequence_length:int) if return_sequence_length is True, else [id:int]
		"""
		tokens = self._encode(sentence, is_split_into_words)
		if padding:
			return self.pad(tokens, max_length, truncation, padding_side, return_sequence_length)
		
		if truncation and max_length:
			tokens = tokens[:max_length]
		
		if return_sequence_length:
			return tokens, len(tokens)
		return tokens
	
	def batch_encode(self, sentences: Union[Collection[str], Collection[List]], max_length: int = None, truncation=True,
	                 padding=True, padding_side='right', is_split_into_words: bool = False,
	                 return_sequence_length=False):
		"""
		:param sentences: ['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ....]
		:param max_length:
		:param truncation:
		:param padding:
		:param padding_side:
		:param is_split_into_words: 是否已经分词
		:param return_sequence_length: 是否返回序列实际长度
		:return:
			if return_sequence_length is True:
				([[id:int]], [sequence_length:int]) if tokens is batch, else ([id:int], sequence_length:int)
			
			if return_sequence_length is False:
				[[id:int]] if tokens is batch, else [id:int]
				
		"""
		if isinstance(sentences, str) or (is_split_into_words and isinstance(sentences[0], str)):
			return self.encode(sentences, max_length, truncation, padding, padding_side,
			                   is_split_into_words, return_sequence_length)
		
		tokens = self._batch_encode(sentences, is_split_into_words)
		if padding:
			return self.pad(tokens, max_length, truncation, padding_side, return_sequence_length)
		
		tokens = list(tokens)
		if truncation and max_length:
			tokens = [x[:max_length] for x in tokens]
		
		if return_sequence_length:
			return tokens, [len(x) for x in tokens]
		return tokens
	
	def pad(self, tokens: Union[map, Collection[int], Collection[Collection[int]]], max_length: int = None,
	        truncation=True,
	        padding_side='right', return_sequence_length=False):
		"""
		:param tokens: [2, 19, 27, 3] 或 [[2, 19, 27, 3], [2, 10, 3]]
		:param max_length:
		:param truncation:
		:param padding_side:
		:param return_sequence_length: 是否返回序列实际长度
		:return:
			if return_sequence_length is True:
				([[id:int]], [sequence_length:int]) if tokens is batch, else ([id:int], sequence_length:int)
			
			if return_sequence_length is False:
				[[id:int]] if tokens is batch, else [id:int]
				
		"""
		if isinstance(tokens, map) or isinstance(tokens[0], Collection):
			if return_sequence_length:
				return batch_pad(tokens, max_length, truncation, True, padding_side, False, False, self.PAD_ID, None,
				                 None)
			return batch_pad(tokens, max_length, truncation, True, padding_side, False, False, self.PAD_ID, None, None)[
				0]
		
		if return_sequence_length:
			return pad(tokens, max_length, truncation, True, padding_side, False, False, self.PAD_ID, None, None)
		return pad(tokens, max_length, truncation, True, padding_side, False, False, self.PAD_ID, None, None)[0]
	
	def __call__(self, sentences: Union[Collection[str], Collection[Collection]], max_length: int = None,
	             truncation=True,
	             padding=True, padding_side='right', is_split_into_words: bool = False,
	             return_sequence_length=False):
		return self.batch_encode(sentences, max_length, truncation, padding, padding_side, is_split_into_words,
		                         return_sequence_length)
	
	def _do_encode(self, cut_token: str):
		return self.word_to_idx.get(cut_token, self.UNK_ID)
	
	def _do_encode_with_stop_words(self, cut_token: str):
		return self.word_to_idx.get(cut_token, self.UNK_ID) if cut_token not in self.stop_words else None


class SimpleTokenizer(PaddingTokenizer):
	"""
	如果碰到未登录词会用'<unk>'代替，能padding, '<pad>'和'<unk>'不同
	"""
	PAD, UNK = '<PAD>', '<UNK>'
	PAD_ID, UNK_ID = 0, 1
	RESERVED_TOKENS = [PAD, UNK]
	
	def __init__(self, path: Union[str, Path] = None, texts: Collection[str] = None,
	             cut_texts: Collection[Collection[str]] = None,
	             vocab: Collection[str] = None, min_freq=10, special_tokens: Collection[str] = None, lang='cn',
	             cut_type='word', word_freq: bool = False, stop_words: Collection[str] = None, keep_punctuation=False,
	             cut_fn=None):
		"""
		:param path: 语料文件路径，可以是文件也可以是文件夹， 如：'./train.txt'. 如果是文件夹，会读取文件夹下的所有目录和文件.
		:param texts: 语料，每个元素是一句话，如：['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ...]
		:param cut_texts: 语料，每个元素是是分词后的一句话，如：[['上课', '时', '学生', '手机', '响', '个', '不停'], ['家长', '拿', '发票', '让', '老师', '赔']]
		:param vocab: 词表，如：['上课', '学生', '手机', '不停', '，', '老师']
		:param min_freq: 最小词频，小于词词频的词会被忽略，默认是0，所有的词都保留
		:param special_tokens: 保留token, 如 '<pad>', '<unk>'等
		:param lang: 语言 'cn'和'en'
		:param cut_type: 分词类型，只支持'word'和‘char'两种类型
		:param word_freq: 是否统计词频
		:param stop_words: 停用词
		:param keep_punctuation: 是否保留标点符号
		:param cut_fn
		"""
		super().__init__(path=path, texts=texts, cut_texts=cut_texts, vocab=vocab, min_freq=min_freq,
		                 special_tokens=special_tokens, lang=lang, cut_type=cut_type, word_freq=word_freq,
		                 stop_words=stop_words, keep_punctuation=keep_punctuation, cut_fn=cut_fn)


class Tokenizer(PaddingTokenizer):
	"""
	如果碰到未登录词会用'<unk>'代替，能padding, 有encode_plus, batch_encode_plus, 返回 {'input_tokens': list, 'mask_tokens': list}
	"""
	PAD, UNK, BOS, EOS = '<PAD>', '<UNK>', '<BOS>', '<EOS>'
	PAD_ID, UNK_ID, BOS_ID, EOS_ID = 0, 1, 2, 3
	RESERVED_TOKENS = [PAD, UNK, BOS, EOS]
	
	def __init__(self, path: Union[str, Path] = None, texts: Collection[str] = None,
	             cut_texts: Collection[Collection[str]] = None,
	             vocab: Collection[str] = None, min_freq=10, special_tokens: Collection[str] = None, lang='cn',
	             cut_type='word', word_freq: bool = False, stop_words: Collection[str] = None, keep_punctuation=False,
	             cut_fn=None):
		"""
		:param path: 语料文件路径，可以是文件也可以是文件夹， 如：'./train.txt'. 如果是文件夹，会读取文件夹下的所有目录和文件.
		:param texts: 语料，每个元素是一句话，如：['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ...]
		:param cut_texts: 语料，每个元素是是分词后的一句话，如：[['上课', '时', '学生', '手机', '响', '个', '不停'], ['家长', '拿', '发票', '让', '老师', '赔']]
		:param vocab: 词表，如：['上课', '学生', '手机', '不停', '，', '老师']
		:param min_freq: 最小词频，小于词词频的词会被忽略，默认是0，所有的词都保留
		:param special_tokens: 保留token, 如 '<pad>', '<unk>'等
		:param lang: 语言 'cn'和'en'
		:param cut_type: 分词类型，只支持'word'和‘char'两种类型
		:param word_freq: 是否统计词频
		:param stop_words: 停用词
		:param keep_punctuation: 是否保留标点符号
		:param cut_fn
		"""
		super().__init__(path=path, texts=texts, cut_texts=cut_texts, vocab=vocab, min_freq=min_freq,
		                 special_tokens=special_tokens, lang=lang, cut_type=cut_type, word_freq=word_freq,
		                 stop_words=stop_words, keep_punctuation=keep_punctuation, cut_fn=cut_fn)
	
	def encode(self, sentence: str, max_length: int = None, truncation=True, padding=True, padding_side='right',
	           bos=True, eos=True, is_split_into_words: bool = False, return_sequence_length=False):
		"""
		:param sentence: '上课时学生手机响个不停，老师一怒之下把手机摔了'
		:param max_length:
		:param truncation:
		:param padding:
		:param padding_side:
		:param bos:
		:param eos:
		:param is_split_into_words: 是否已经分词
		:param return_sequence_length: 是否返回序列实际长度
		:return: ([id:int], sequence_length:int) if return_sequence_length is True, else [id:int]
		"""
		tokens = self._encode(sentence, is_split_into_words)
		if padding or bos or eos:
			return self.pad(tokens, max_length, truncation, padding, padding_side, return_sequence_length, bos, eos)
		
		if truncation and max_length:
			tokens = tokens[:max_length]
		
		if return_sequence_length:
			return tokens, len(tokens)
		return tokens
	
	def batch_encode(self, sentences: Union[Collection[str], Collection[Collection]], max_length: int = None,
	                 truncation=True, padding=True, padding_side='right', bos=True, eos=True,
	                 is_split_into_words: bool = False, return_sequence_length=False):
		"""
		:param sentences: ['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ....]
		:param max_length:
		:param truncation:
		:param padding:
		:param padding_side:
		:param bos:
		:param eos:
		:param is_split_into_words: 是否已经分词
		:param return_sequence_length: 是否返回序列实际长度
		:return:
			if return_sequence_length is True:
				([[id:int]], [sequence_length:int]) if tokens is batch, else ([id:int], sequence_length:int)
			
			if return_sequence_length is False:
				[[id:int]] if tokens is batch, else [id:int]
		"""
		if isinstance(sentences, str) or (is_split_into_words and isinstance(sentences[0], str)):
			return self.encode(sentences, max_length, truncation, padding, padding_side, bos, eos,
			                   is_split_into_words, return_sequence_length)
		
		tokens = self._batch_encode(sentences, is_split_into_words)
		if padding or bos or eos:
			return self.pad(tokens, max_length, truncation, padding, padding_side, return_sequence_length, bos, eos)
		
		tokens = list(tokens)
		if truncation and max_length:
			tokens = [x[:max_length] for x in tokens]
		
		if return_sequence_length:
			return tokens, [len(x) for x in tokens]
		return tokens
	
	def pad(self, tokens: Union[map, Collection[int], Collection[Collection[int]]], max_length: int = None,
	        truncation=True, padding=True, padding_side='right', return_sequence_length=False, bos=True, eos=True):
		"""
		:param tokens: [2, 19, 27, 3] 或 [[2, 19, 27, 3], [2, 10, 3]]
		:param max_length:
		:param truncation:
		:param padding
		:param padding_side:
		:param return_sequence_length: 是否返回序列实际长度
		:param bos:
		:param eos:
		:return:
			if return_sequence_length is True:
				([[id:int]], [sequence_length:int]) if tokens is batch, else ([id:int], sequence_length:int)
			
			if return_sequence_length is False:
				[[id:int]] if tokens is batch, else [id:int]
		"""
		if isinstance(tokens, map) or isinstance(tokens[0], Collection):
			if return_sequence_length:
				return batch_pad(tokens, max_length, truncation, padding, padding_side, bos, eos, self.PAD_ID,
				                 self.BOS_ID, self.EOS_ID)
			return batch_pad(tokens, max_length, truncation, padding, padding_side, bos, eos, self.PAD_ID,
			                 self.BOS_ID, self.EOS_ID)[0]
		if return_sequence_length:
			return pad(tokens, max_length, truncation, padding, padding_side, bos, eos, self.PAD_ID, self.BOS_ID,
			           self.EOS_ID)
		return \
			pad(tokens, max_length, truncation, padding, padding_side, bos, eos, self.PAD_ID, self.BOS_ID, self.EOS_ID)[
				0]
	
	def encode_plus(self, sentence: Union[str, Collection[str], Collection[Collection]], max_length: int = None,
	                truncation=True, padding=True, padding_side='right', bos=False, eos=False,
	                return_mask=False, is_split_into_words=False):
		"""
		:param sentence: '上课时学生手机响个不停，老师一怒之下把手机摔了' 或 ['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ....]
		:param max_length:
		:param truncation:
		:param padding:
		:param padding_side:
		:param bos:
		:param eos:
		:param return_mask: 是否返回 mask_tokens
		:param is_split_into_words: 是否已经分词
		:return:
		"""
		if isinstance(sentence, str):
			tokens = self._encode(sentence, is_split_into_words)
			return self.pad_plus(tokens, max_length, truncation, padding, padding_side, bos, eos, return_mask)
		
		raise ValueError('参数"sentence"类型错误')
	
	def batch_encode_plus(self, sentences: Union[str, Collection[str], Collection[Collection]], max_length: int = None,
	                      truncation=True, padding=True, padding_side='right', bos=False, eos=False,
	                      return_mask=False, is_split_into_words=False):
		"""
		:param sentences: ['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ....]
		:param max_length:
		:param truncation:
		:param padding:
		:param padding_side:
		:param bos:
		:param eos:
		:param return_mask: 是否返回 mask_tokens
		:param is_split_into_words: 是否已经分词
		:return:
		"""
		if isinstance(sentences, str) or (is_split_into_words and isinstance(sentences[0], str)):
			return self.encode_plus(sentences, max_length, truncation, padding, padding_side, bos, eos,
			                        return_mask, is_split_into_words)
		if isinstance(sentences, Collection):
			tokens = self._batch_encode(sentences, is_split_into_words)
			return self.pad_plus(tokens, max_length, truncation, padding, padding_side, bos, eos, return_mask)
		
		raise ValueError('参数"sentence"类型错误')
	
	def pad_plus(self, tokens: Union[map, Collection[int], Collection[Collection[int]]], max_length: int = None,
	             truncation=True, padding=True, padding_side='right', bos=False, eos=False, return_mask=False):
		"""
		:param tokens: [2, 19, 27, 3] 或 [[2, 19, 27, 3], [2, 10, 3]]
		:param max_length:
		:param truncation:
		:param padding
		:param padding_side:
		:param bos:
		:param eos:
		:param return_mask:
		:return:
		"""
		if isinstance(tokens, map) or isinstance(tokens[0], Collection):
			if return_mask:
				return batch_pad_mask(tokens, max_length, truncation, padding, padding_side, bos, eos,
				                      self.PAD_ID, self.BOS_ID, self.EOS_ID)
			return {'input_tokens': batch_pad(tokens, max_length, truncation, padding, padding_side, bos, eos,
			                                  self.PAD_ID, self.BOS_ID, self.EOS_ID)[0]}
		
		if return_mask:
			return pad_mask(tokens, max_length, truncation, padding, padding_side, bos, eos,
			                self.PAD_ID, self.BOS_ID, self.EOS_ID)
		return {'input_tokens': pad(tokens, max_length, truncation, padding, padding_side, bos, eos,
		                            self.PAD_ID, self.BOS_ID, self.EOS_ID)[0]}
	
	def __call__(self, sentence: Union[str, Collection[str]], max_length: int = None, truncation=True, padding=True,
	             padding_side='right', bos=False, eos=False, return_mask=False,
	             is_split_into_words=False):
		return self.encode_plus(sentence, max_length, truncation, padding, padding_side, bos, eos, return_mask,
		                        is_split_into_words)


class BosTokenizer(PaddingTokenizer):
	"""
	如果碰到未登录词会用'<unk>'代替，能padding, 只有BOS没有EOS
	"""
	PAD, UNK, BOS = '<PAD>', '<UNK>', '<BOS>'
	PAD_ID, UNK_ID, BOS_ID = 0, 1, 2
	RESERVED_TOKENS = [PAD, UNK, BOS]
	
	def __init__(self, path: Union[str, Path] = None, texts: Collection[str] = None,
	             cut_texts: Collection[Collection[str]] = None,
	             vocab: Collection[str] = None, min_freq=10, special_tokens: Collection[str] = None, lang='cn',
	             cut_type='word', word_freq: bool = False, stop_words: Collection[str] = None, keep_punctuation=False,
	             cut_fn=None):
		"""
		:param path: 语料文件路径，可以是文件也可以是文件夹， 如：'./train.txt'. 如果是文件夹，会读取文件夹下的所有目录和文件.
		:param texts: 语料，每个元素是一句话，如：['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ...]
		:param cut_texts: 语料，每个元素是是分词后的一句话，如：[['上课', '时', '学生', '手机', '响', '个', '不停'], ['家长', '拿', '发票', '让', '老师', '赔']]
		:param vocab: 词表，如：['上课', '学生', '手机', '不停', '，', '老师']
		:param min_freq: 最小词频，小于词词频的词会被忽略，默认是0，所有的词都保留
		:param special_tokens: 保留token, 如 '<pad>', '<unk>'等
		:param lang: 语言 'cn'和'en'
		:param cut_type: 分词类型，只支持'word'和‘char'两种类型
		:param word_freq: 是否统计词频
		:param stop_words: 停用词
		:param keep_punctuation: 是否保留标点符号
		:param cut_fn
		"""
		super().__init__(path=path, texts=texts, cut_texts=cut_texts, vocab=vocab, min_freq=min_freq,
		                 special_tokens=special_tokens, lang=lang, cut_type=cut_type, word_freq=word_freq,
		                 stop_words=stop_words, keep_punctuation=keep_punctuation, cut_fn=cut_fn)
	
	def encode(self, sentence: str, max_length: int = None, truncation=True, padding=True, padding_side='right',
	           bos=True, is_split_into_words: bool = False, return_sequence_length=False):
		"""
		:param sentence: '上课时学生手机响个不停，老师一怒之下把手机摔了'
		:param max_length:
		:param truncation:
		:param padding:
		:param padding_side:
		:param bos:
		:param is_split_into_words: 是否已经分词
		:param return_sequence_length: 是否返回序列实际长度
		:return: ([id:int], sequence_length:int) if return_sequence_length is True, else [id:int]
		"""
		tokens = self._encode(sentence, is_split_into_words)
		if padding or bos:
			return self.pad(tokens, max_length, truncation, padding, padding_side, return_sequence_length, bos)
		
		if truncation and max_length:
			tokens = tokens[:max_length]
		
		if return_sequence_length:
			return tokens, len(tokens)
		return tokens
	
	def batch_encode(self, sentences: Union[Collection[str], Collection[Collection]], max_length: int = None,
	                 truncation=True, padding=True, padding_side='right', bos=True,
	                 is_split_into_words: bool = False, return_sequence_length=False):
		"""
		:param sentences: ['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ....]
		:param max_length:
		:param truncation:
		:param padding:
		:param padding_side:
		:param bos:
		:param is_split_into_words: 是否已经分词
		:param return_sequence_length: 是否返回序列实际长度
		:return:
			if return_sequence_length is True:
				([[id:int]], [sequence_length:int]) if tokens is batch, else ([id:int], sequence_length:int)

			if return_sequence_length is False:
				[[id:int]] if tokens is batch, else [id:int]
		"""
		if isinstance(sentences, str) or (is_split_into_words and isinstance(sentences[0], str)):
			return self.encode(sentences, max_length, truncation, padding, padding_side, bos,
			                   is_split_into_words, return_sequence_length)
		
		tokens = self._batch_encode(sentences, is_split_into_words)
		if padding or bos:
			return self.pad(tokens, max_length, truncation, padding, padding_side, return_sequence_length, bos)
		
		tokens = list(tokens)
		if truncation and max_length:
			tokens = [x[:max_length] for x in tokens]
		
		if return_sequence_length:
			return tokens, [len(x) for x in tokens]
		return tokens
	
	def pad(self, tokens: Union[map, Collection[int], Collection[Collection[int]]], max_length: int = None,
	        truncation=True, padding=True, padding_side='right', return_sequence_length=False, bos=True):
		"""
		:param tokens: [2, 19, 27, 3] 或 [[2, 19, 27, 3], [2, 10, 3]]
		:param max_length:
		:param truncation:
		:param padding
		:param padding_side:
		:param return_sequence_length: 是否返回序列实际长度
		:param bos:
		:param eos:
		:return:
			if return_sequence_length is True:
				([[id:int]], [sequence_length:int]) if tokens is batch, else ([id:int], sequence_length:int)

			if return_sequence_length is False:
				[[id:int]] if tokens is batch, else [id:int]
		"""
		if isinstance(tokens, map) or isinstance(tokens[0], Collection):
			if return_sequence_length:
				return batch_pad(tokens, max_length, truncation, padding, padding_side, bos, False, self.PAD_ID,
				                 self.BOS_ID)
			return \
				batch_pad(tokens, max_length, truncation, padding, padding_side, bos, False, self.PAD_ID, self.BOS_ID)[
					0]
		if return_sequence_length:
			return pad(tokens, max_length, truncation, padding, padding_side, bos, False, self.PAD_ID, self.BOS_ID)
		return pad(tokens, max_length, truncation, padding, padding_side, bos, False, self.PAD_ID, self.BOS_ID)[0]


class EosTokenizer(PaddingTokenizer):
	"""
	如果碰到未登录词会用'<unk>'代替，能padding,  只有EOS没有BOS
	"""
	PAD, UNK, EOS = '<PAD>', '<UNK>', '<EOS>'
	PAD_ID, UNK_ID, EOS_ID = 0, 1, 2
	RESERVED_TOKENS = [PAD, UNK, EOS]
	
	def __init__(self, path: Union[str, Path] = None, texts: Collection[str] = None,
	             cut_texts: Collection[Collection[str]] = None,
	             vocab: Collection[str] = None, min_freq=10, special_tokens: Collection[str] = None, lang='cn',
	             cut_type='word', word_freq: bool = False, stop_words: Collection[str] = None, keep_punctuation=False,
	             cut_fn=None):
		"""
		:param path: 语料文件路径，可以是文件也可以是文件夹， 如：'./train.txt'. 如果是文件夹，会读取文件夹下的所有目录和文件.
		:param texts: 语料，每个元素是一句话，如：['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ...]
		:param cut_texts: 语料，每个元素是是分词后的一句话，如：[['上课', '时', '学生', '手机', '响', '个', '不停'], ['家长', '拿', '发票', '让', '老师', '赔']]
		:param vocab: 词表，如：['上课', '学生', '手机', '不停', '，', '老师']
		:param min_freq: 最小词频，小于词词频的词会被忽略，默认是0，所有的词都保留
		:param special_tokens: 保留token, 如 '<pad>', '<unk>'等
		:param lang: 语言 'cn'和'en'
		:param cut_type: 分词类型，只支持'word'和‘char'两种类型
		:param word_freq: 是否统计词频
		:param stop_words: 停用词
		:param keep_punctuation: 是否保留标点符号
		:param cut_fn
		"""
		super().__init__(path=path, texts=texts, cut_texts=cut_texts, vocab=vocab, min_freq=min_freq,
		                 special_tokens=special_tokens, lang=lang, cut_type=cut_type, word_freq=word_freq,
		                 stop_words=stop_words, keep_punctuation=keep_punctuation, cut_fn=cut_fn)
	
	def encode(self, sentence: str, max_length: int = None, truncation=True, padding=True, padding_side='right',
	           eos=True, is_split_into_words: bool = False, return_sequence_length=False):
		"""
		:param sentence: '上课时学生手机响个不停，老师一怒之下把手机摔了'
		:param max_length:
		:param truncation:
		:param padding:
		:param padding_side:
		:param eos:
		:param is_split_into_words: 是否已经分词
		:param return_sequence_length: 是否返回序列实际长度
		:return: ([id:int], sequence_length:int) if return_sequence_length is True, else [id:int]
		"""
		tokens = self._encode(sentence, is_split_into_words)
		if padding or eos:
			return self.pad(tokens, max_length, truncation, padding, padding_side, return_sequence_length, eos)
		
		if truncation and max_length:
			tokens = tokens[:max_length]
		
		if return_sequence_length:
			return tokens, len(tokens)
		return tokens
	
	def batch_encode(self, sentences: Union[Collection[str], Collection[Collection]], max_length: int = None,
	                 truncation=True, padding=True, padding_side='right', eos=True,
	                 is_split_into_words: bool = False, return_sequence_length=False):
		"""
		:param sentences: ['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ....]
		:param max_length:
		:param truncation:
		:param padding:
		:param padding_side:
		:param eos:
		:param is_split_into_words: 是否已经分词
		:param return_sequence_length: 是否返回序列实际长度
		:return:
			if return_sequence_length is True:
				([[id:int]], [sequence_length:int]) if tokens is batch, else ([id:int], sequence_length:int)

			if return_sequence_length is False:
				[[id:int]] if tokens is batch, else [id:int]
		"""
		if isinstance(sentences, str) or (is_split_into_words and isinstance(sentences[0], str)):
			return self.encode(sentences, max_length, truncation, padding, padding_side, eos,
			                   is_split_into_words, return_sequence_length)
		
		tokens = self._batch_encode(sentences, is_split_into_words)
		if padding or eos:
			return self.pad(tokens, max_length, truncation, padding, padding_side, return_sequence_length, eos)
		
		tokens = list(tokens)
		if truncation and max_length:
			tokens = [x[:max_length] for x in tokens]
		
		if return_sequence_length:
			return tokens, [len(x) for x in tokens]
		return tokens
	
	def pad(self, tokens: Union[map, Collection[int], Collection[Collection[int]]], max_length: int = None,
	        truncation=True, padding=True, padding_side='right', return_sequence_length=False, eos=True):
		"""
		:param tokens: [2, 19, 27, 3] 或 [[2, 19, 27, 3], [2, 10, 3]]
		:param max_length:
		:param truncation:
		:param padding
		:param padding_side:
		:param return_sequence_length: 是否返回序列实际长度
		:param eos:
		:return:
			if return_sequence_length is True:
				([[id:int]], [sequence_length:int]) if tokens is batch, else ([id:int], sequence_length:int)

			if return_sequence_length is False:
				[[id:int]] if tokens is batch, else [id:int]
		"""
		if isinstance(tokens, map) or isinstance(tokens[0], Collection):
			if return_sequence_length:
				return batch_pad(tokens, max_length, truncation, padding, padding_side, False, eos, self.PAD_ID,
				                 None, self.EOS_ID)
			return batch_pad(tokens, max_length, truncation, padding, padding_side, False, eos, self.PAD_ID,
			                 None, self.EOS_ID)[0]
		if return_sequence_length:
			return pad(tokens, max_length, truncation, padding, padding_side, False, eos, self.PAD_ID, None,
			           self.EOS_ID)
		return pad(tokens, max_length, truncation, padding, padding_side, False, eos, self.PAD_ID, None, self.EOS_ID)[0]


class AutoTokenizer:
	TOKENIZER_DICT = {
		"BaseTokenizer": BaseTokenizer,
		"PaddingTokenizer": PaddingTokenizer,
		"SimpleTokenizer": SimpleTokenizer,
		"Tokenizer": Tokenizer,
		"BosTokenizer": BosTokenizer,
		"EosTokenizer": EosTokenizer,
	}
	
	@staticmethod
	def load(path, cut_fn=None):
		with open(path, 'rb') as f:
			obj = pickle.load(f)
		
		tokenizer_name = obj['name']
		tokenizer = AutoTokenizer.TOKENIZER_DICT.get(tokenizer_name)
		assert tokenizer is not None, f"{tokenizer_name} is not a valid tokenizer"
		return tokenizer(vocab=obj['vocab'], special_tokens=obj['special_tokens'], lang=obj['lang'],
		                 cut_type=obj['cut_type'], stop_words=obj['stop_words'],
		                 keep_punctuation=obj['keep_punctuation'], cut_fn=cut_fn)


class TokenEmbedding:
	"""
	可以传入已经训练好的embedding文件路径，也可以embedding数据, encode返回的是 {'input_tokens': list} 或 {'input_tokens': list, 'mask_tokens': list}
	"""
	
	def __init__(self, file: Union[str, Path] = None, vocab: Collection[str] = None,
	             embedding: Collection[Collection[float]] = None,
	             special_tokens: Collection[str] = None, lang='cn', cut_type='word', func=load_embedding,
	             is_large_file=False, keep_punctuation=True, cut_fn=None):
		"""
		:param file: embedding文件路径， 如：'./sgns.weibo.word.bz2'
		:param vocab: 词表，如：['上课', '学生', '手机', '不停', '，', '老师']，与embedding必须同时传入
		:param embedding: [[0.2548, -0.6879, 0.2578],[0.2548, -0.6879, 0.2578],[0.2548, -0.6879, 0.2578]]与vocab必须同时传入
		:param special_tokens: 保留token, 如 '<pad>', '<unk>'等
		:param lang: 语言 'cn'和'en'
		:param cut_type: 分词类型，只支持'word'和‘char'两种类型
		:param func: 具体读取文件的处理函数，load_embedding，可替换。
			   注意：其函数签名为 function_name(path: str, is_large_file: bool) -> (vocab: list[str], embedding: list[list[float]])
		:param is_large_file: 是否是大文件
		:param keep_punctuation: 是否保留标点符号
		:param cut_fn
		"""
		if file:
			if isinstance(file, str):
				file = Path(file)
			assert file.is_file(), 'file必须是具体文件,不能是文件夹'
			vocab, embedding = func(file, is_large_file)
		elif not vocab or not embedding:
			raise ValueError('参数"path"为空的情况下，"vocab"和"embedding"不能为空.')
		self.tokenizer = Tokenizer(vocab=vocab, special_tokens=special_tokens, lang=lang, cut_type=cut_type,
		                           keep_punctuation=keep_punctuation, cut_fn=cut_fn)
		special_tokens = self.tokenizer.special_tokens.copy()
		special_tokens.reverse()
		self.embed_dim = len(embedding[0])
		for token in special_tokens:
			embedding = [[self.tokenizer.do_encode(token)] * self.embed_dim] + embedding
		self.embedding = Embedding.from_pretrained(torch.tensor(embedding, dtype=torch.float))
		del embedding
		gc.collect()
	
	@property
	def vocab_size(self):
		return self.tokenizer.vocab_size
	
	@property
	def real_vocab(self):
		return self.tokenizer.real_vocab
	
	def encode(self, sentence: str, max_length: int = None, truncation=True, padding=True, padding_side='right',
	           bos=False, eos=False, is_split_into_words: bool = False, return_sequence_length=False):
		"""
		:param sentence: '上课时学生手机响个不停，老师一怒之下把手机摔了'
		:param max_length:
		:param truncation:
		:param padding:
		:param padding_side:
		:param bos:
		:param eos:
		:param is_split_into_words: 是否已经分词
		:param return_sequence_length: 是否返回序列实际长度
		:return: ([id:int], sequence_length:int) if return_sequence_length is True, else [id:int]
		"""
		return self.tokenizer.encode(sentence, max_length, truncation, padding, padding_side, bos, eos,
		                             is_split_into_words, return_sequence_length)
	
	def batch_encode(self, sentences: Union[Collection[str], Collection[Collection]], max_length: int = None,
	                 truncation=True,
	                 padding=True, padding_side='right', bos=False, eos=False,
	                 is_split_into_words: bool = False, return_sequence_length=False):
		"""
		:param sentences: ['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ....]
		:param max_length:
		:param truncation:
		:param padding:
		:param padding_side:
		:param bos:
		:param eos:
		:param is_split_into_words: 是否已经分词
		:param return_sequence_length: 是否返回序列实际长度
		:return:
			if return_sequence_length is True:
				([[id:int]], [sequence_length:int]) if tokens is batch, else ([id:int], sequence_length:int)
			
			if return_sequence_length is False:
				[[id:int]] if tokens is batch, else [id:int]
		"""
		return self.tokenizer.batch_encode(sentences, max_length, truncation, padding, padding_side, bos, eos,
		                                   is_split_into_words, return_sequence_length)
	
	def decode(self, tokens: Collection[int], return_special_tokens=False, return_sentence=False):
		"""
		:param tokens: [2, 19, 27, 3, 0, 0]
		:param return_special_tokens: 是否返回'<pad>', '<unk>', '<bos>', '<eos>'等特殊字符
		:param return_sentence: 返回的是一句话还是词序列
		:return: 由return_sentence决定，返回的是 '上课时学生手机响个不停‘, 还是 ['上课', '时', '学生', '手机', ’响个, '不停']
		"""
		return self.tokenizer.decode(tokens, return_special_tokens, return_sentence)
	
	def batch_decode(self, tokens: Collection[Collection[int]], return_special_tokens=False, return_sentence=False):
		"""
		:param tokens: [[2, 19, 27, 3, 0, 0], [2, 10, 3, 0, 0, 0]]
		:param return_special_tokens: 是否返回'<pad>', '<unk>', '<bos>', '<eos>'等特殊字符
		:param return_sentence: 返回的是一句话还是词序列
		:return: 由return_sentence决定，返回的是 '上课时学生手机响个不停‘, 还是 ['上课', '时', '学生', '手机', ’响个, '不停']
		"""
		return self.tokenizer.batch_decode(tokens, return_special_tokens, return_sentence)
	
	def pad(self, tokens: Union[map, Collection[int], Collection[Collection[int]]], max_length: int, truncation=True,
	        padding=True, padding_side='right', bos=False, eos=False):
		"""
		:param tokens: [2, 19, 27, 3] 或 [[2, 19, 27, 3], [2, 10, 3]]
		:param max_length:
		:param truncation:
		:param padding:
		:param padding_side:
		:param bos:
		:param eos:
		:return:
		"""
		return self.tokenizer.pad(tokens, max_length, truncation, padding, padding_side, bos, eos)
	
	def encode_plus(self, sentence: Union[str, Collection[str], Collection[Collection]], max_length: int = None,
	                truncation=True, padding=True, padding_side='right', bos=False, eos=False,
	                return_mask=False, is_split_into_words=False):
		"""
		:param sentence: '上课时学生手机响个不停，老师一怒之下把手机摔了' 或 ['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ....]
		:param max_length:
		:param truncation:
		:param padding:
		:param padding_side:
		:param bos:
		:param eos:
		:param return_mask: 是否返回 mask_tokens
		:param is_split_into_words: 是否已经分词
		:return:
		"""
		return self.tokenizer.encode_plus(sentence, max_length, truncation, padding, padding_side, bos, eos,
		                                  return_mask, is_split_into_words)
	
	def batch_encode_plus(self, sentences: Union[str, Collection[str], Collection[Collection]], max_length: int = None,
	                      truncation=True, padding=True, padding_side='right', bos=False, eos=False,
	                      return_mask=False, is_split_into_words=False):
		"""
		:param sentences: ['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ....]
		:param max_length:
		:param truncation:
		:param padding:
		:param padding_side:
		:param bos:
		:param eos:
		:param return_mask: 是否返回 mask_tokens
		:param is_split_into_words: 是否已经分词
		:return:
		"""
		return self.tokenizer.batch_encode_plus(sentences, max_length, truncation, padding, padding_side, bos,
		                                        eos, return_mask, is_split_into_words)
	
	def pad_plus(self, tokens: Union[map, Collection[int], Collection[Collection[int]]], max_length: int,
	             truncation=True,
	             padding=True, padding_side='right', bos=False, eos=False, return_mask=False):
		"""
		:param tokens: [2, 19, 27, 3] 或 [[2, 19, 27, 3], [2, 10, 3]]
		:param max_length:
		:param truncation:
		:param padding:
		:param padding_side:
		:param bos:
		:param eos:
		:param return_mask:
		:return:
		"""
		return self.tokenizer.pad_plus(tokens, max_length, truncation, padding, padding_side, bos, eos, return_mask)
	
	def __call__(self, sentence: Union[str, Collection[str], Collection[Collection]], max_length: int = None,
	             truncation=True,
	             padding=True, padding_side='right', bos=False, eos=False, is_split_into_words: bool = False):
		input_tokens = self.batch_encode(sentence, max_length, truncation, padding, padding_side, bos, eos,
		                                 is_split_into_words)
		return self.embedding(torch.tensor(input_tokens, dtype=torch.long))
	
	@classmethod
	def from_file(cls, file: Union[str, Path], func=load_embedding, is_large_file=False, special_tokens=[], lang='cn',
	              cut_type='word', keep_punctuation=True, cut_fn=None):
		"""
		:param file: embedding文件， 如：'./sgns.weibo.word.bz2'. 注意：必须是单一文件，不能是文件夹。
		:param func: 具体读取文件的处理函数，load_embedding，可替换。注意：其函数签名为 function_name(path: str, is_large_file: bool) -> [vocab], [[embedding]]
		:param is_large_file: 是否是大文件
		:param special_tokens: 保留token, 如 '<pad>', '<unk>'等
		:param lang: 语言 'cn'和'en'
		:param cut_type: 分词类型，只支持'word'和‘char'两种类型
		:param keep_punctuation: 是否保留标点符号
		:param cut_fn
		"""
		return cls(file=file, special_tokens=special_tokens, lang=lang, cut_type=cut_type, func=func,
		           is_large_file=is_large_file, keep_punctuation=keep_punctuation, cut_fn=cut_fn)
	
	@classmethod
	def from_vocab_embedding(cls, vocab: Collection[str], embedding: Collection[Collection[float]], large_file=False,
	                         special_tokens: Collection[str] = None, lang='cn', cut_type='word', keep_punctuation=True,
	                         cut_fn=None):
		"""
		:param vocab: 词表，如：['上课', '学生', '手机', '不停', '，', '老师']
		:param embedding: [[0.2548, -0.6879, 0.2578],[0.2548, -0.6879, 0.2578],[0.2548, -0.6879, 0.2578]]
		:param large_file: 是否是大文件
		:param special_tokens: 保留token, 如 '<pad>', '<unk>'等
		:param lang: 语言 'cn'和'en'
		:param cut_type: 分词类型，只支持'word'和‘char'两种类型
		:param keep_punctuation: 是否保留标点符号
		:param cut_fn
		"""
		return cls(vocab=vocab, embedding=embedding, large_file=large_file, special_tokens=special_tokens,
		           lang=lang, cut_type=cut_type, keep_punctuation=keep_punctuation, cut_fn=cut_fn)
