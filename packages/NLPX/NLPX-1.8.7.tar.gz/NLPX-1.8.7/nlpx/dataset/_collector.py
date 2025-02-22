import torch
import numpy as np
from typing import Union, List, Tuple

from nlpx.llm import TokenizeVec
from nlpx.tokenize import BaseTokenizer, TokenEmbedding
from nlpx.tokenize.utils import get_texts_max_length


class TextVecCollator:
	
	def __init__(self, tokenize_vec: Union[TokenizeVec, TokenEmbedding], max_length: int = None, **kwargs):
		self.tokenize_vec = tokenize_vec
		self.max_length = max_length
		self.kwargs = kwargs
	
	def __call__(self, examples):
		texts, labels = zip(*examples)
		labels = torch.LongTensor(np.array(labels))
		
		if isinstance(self.tokenize_vec, TokenizeVec):
			max_length = get_texts_max_length(texts, cut_type='char') + 2
			max_length = min(max_length, self.max_length) if self.max_length and self.max_length > 0 else max_length
			return self.tokenize_vec.encode_plus(texts, max_length=max_length, padding='max_length',
			                                     truncation=True, add_special_tokens=True,
			                                     return_token_type_ids=True, return_attention_mask=True,
			                                     return_tensors='pt', **self.kwargs), labels
		elif isinstance(self.tokenize_vec, TokenEmbedding):
			max_length = get_texts_max_length(texts, cut_type=self.tokenize_vec.cut_type,
			                                  lang=self.tokenize_vec.lang, cut_fn=self.tokenize_vec.cut_fn)
			max_length = min(max_length, self.max_length) if self.max_length and self.max_length > 0 else max_length
			return self.tokenize_vec(texts, max_length, **self.kwargs), labels
		
		raise ValueError("Invalid tokenize_vec, it must be a TokenizeVec or TokenEmbedding.")


class TokenizeCollator:
	
	def __init__(self, tokenizer, max_length: int = None, **kwargs):
		self.tokenizer = tokenizer
		self.max_length = max_length
		self.kwargs = kwargs
	
	def __call__(self, examples):
		texts, labels = zip(*examples)
		labels = torch.LongTensor(np.array(labels))
		
		if isinstance(self.tokenizer, BaseTokenizer):
			max_length = get_texts_max_length(texts, cut_type=self.tokenizer.cut_type, lang=self.tokenizer.lang,
			                                  cut_fn=self.tokenizer.cut_fn)
			max_length = min(max_length, self.max_length) if self.max_length else max_length
			return torch.LongTensor(self.tokenizer.batch_encode(texts, max_length, **self.kwargs)), labels
		
		max_length = get_texts_max_length(texts, cut_type='char') + 2
		max_length = min(max_length, self.max_length) if self.max_length and self.max_length > 0 else max_length
		result = self.tokenizer.batch_encode_plus(texts, max_length=max_length, padding='max_length',
		                                          return_token_type_ids=True, return_attention_mask=True,
		                                          truncation=True, add_special_tokens=True, return_tensors='pt',
		                                          **self.kwargs)
		result['labels'] = labels
		return result


class PaddingTokenCollator:
	"""与TokenDataset配合使用, 只有token, label两列数数

	Examples
	--------
	>>> tokenizer = PaddingTokenizer(texts=texts)
	>>> X_train = tokenizer.batch_encode(texts, padding=False)
	>>> train_set = TokenDataset(X_train, y_train)
	>>> model_wrapper = ClassifyModelWrapper(classes=classes)
	>>> model_wrapper.train(model, train_set, early_stopping_rounds=5, show_progress=False,
	>>>                     collate_fn=PaddingTokenCollator(tokenizer.pad, return_sequence_length=True))
	"""
	
	def __init__(self, pad_func, max_length: int = None, truncation=True, padding_side='right',
	             return_sequence_length=False, bos=False, eos=False):
		self.pad_func = pad_func
		self.max_length = max_length
		self.truncation = truncation
		self.padding_side = padding_side
		self.return_sequence_length = return_sequence_length
		self.bos, self.eos = bos, eos
	
	def __call__(self, examples):
		tokens, labels = zip(*examples)
		labels = torch.LongTensor(np.array(labels))
		
		max_length = max(map(lambda x: len(x), tokens))
		max_length = min(max_length, self.max_length) if self.max_length and self.max_length > 0 else max_length
		params = {'truncation': self.truncation, 'padding_side': self.padding_side}
		if self.bos:
			params['bos'] = self.bos
		if self.eos:
			params['eos'] = self.eos
		
		if self.return_sequence_length:
			params['return_sequence_length'] = self.return_sequence_length
			ids, sequence_lengths = self.pad_func(tokens, max_length, **params)
			return torch.LongTensor(ids), torch.IntTensor(sequence_lengths), labels
		
		ids = self.pad_func(tokens, max_length, **params)
		if isinstance(ids, Tuple):
			ids = ids[0]
		return torch.LongTensor(ids), labels


class PaddingLongTensorCollector:
	""" 可以有多列数据 
	配合ListDataset使用
	"""
	
	def __init__(self, pad_func):
		self.pad_func = pad_func
	
	def __call__(self, batch):
		batch = (self.pad_func(x) if isinstance(x[0], List) else x for x in zip(*batch))
		return tuple(torch.tensor(x, dtype=torch.long) for x in batch)
	