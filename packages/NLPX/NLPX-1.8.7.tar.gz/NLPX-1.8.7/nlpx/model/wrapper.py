import numpy as np
import pandas as pd
import torch
from torch import nn
from torch import optim
from pathlib import Path
from typing import Union, List, Tuple, Collection
from sklearn.model_selection import train_test_split
from torch.optim.lr_scheduler import LRScheduler
from model_wrapper.utils import acc_predict
from model_wrapper.training import (
    ClassTrainer,
    SimpleClassTrainer,
    EvalClassTrainer,
    SimpleEvalClassTrainer,
)
from model_wrapper import (
    ModelWrapper,
    SimpleModelWrapper,
    ClassifyModelWrapper,
    SimpleClassifyModelWrapper,
    SplitClassifyModelWrapper,
    RegressModelWrapper,
    SimpleRegressModelWrapper,
    SplitRegressModelWrapper,
)

from nlpx.llm import TokenizeVec
from nlpx.dataset import TokenDataset, PaddingTokenCollator
from nlpx.tokenize import (
    BaseTokenizer,
    PaddingTokenizer,
    SimpleTokenizer,
    Tokenizer,
    TokenEmbedding,
)

__all__ = [
    "ModelWrapper",
    "SimpleModelWrapper",
    "ClassifyModelWrapper",
    "SimpleClassifyModelWrapper",
    "SplitClassifyModelWrapper",
    "TextModelWrapper",
    "SplitTextModelWrapper",
    "PaddingTextModelWrapper",
    "SplitPaddingTextModelWrapper",
    "RegressModelWrapper",
    "SimpleRegressModelWrapper",
    "SplitRegressModelWrapper",
]


class TextModelWrapper(SimpleClassifyModelWrapper):
    """
    Examples
    --------
    >>> from nlpx.model.wrapper import TextModelWrapper
    >>> model_wrapper = TextModelWrapper(model, tokenize_vec, classes=classes)
    >>> model_wrapper.train(train_texts, y_train val_data, collate_fn)
    >>> model_wrapper.predict(test_texts)
    >>> model_wrapper.evaluate(test_texts, y_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        tokenize_vec: Union[BaseTokenizer, TokenizeVec, TokenEmbedding],
        classes: Collection[str] = None,
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, classes, device)
        self.tokenize_vec = tokenize_vec

    def train(
        self,
        texts: Union[Collection[str], np.ndarray, pd.Series],
        y: Union[torch.LongTensor, np.ndarray, List],
        val_data: Tuple[
            Union[Collection[str], np.ndarray, pd.Series],
            Union[torch.LongTensor, np.ndarray, List],
        ] = None,
        max_length: int = None,
        collate_fn=None,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=64,
        eval_batch_size=128,
        num_workers=0,
        num_eval_workers=0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        n_jobs=-1,
        show_progress=True,
        eps=1e-5,
    ) -> dict:
        X = self.get_vec(texts, max_length=max_length, n_jobs=n_jobs)
        if val_data:
            val_data = (
                self.get_vec(val_data[0], max_length=max_length, n_jobs=-1),
                val_data[1],
            )
            trainer = SimpleEvalClassTrainer(
                epochs,
                optimizer,
                scheduler,
                lr,
                T_max,
                batch_size,
                eval_batch_size,
                num_workers,
                num_eval_workers,
                pin_memory,
                pin_memory_device,
                persistent_workers,
                early_stopping_rounds,
                print_per_rounds,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, X, y, val_data, collate_fn, show_progress, eps
            )
        else:
            trainer = SimpleClassTrainer(
                epochs,
                optimizer,
                scheduler,
                lr,
                T_max,
                batch_size,
                num_workers,
                pin_memory,
                pin_memory_device,
                persistent_workers,
                early_stopping_rounds,
                print_per_rounds,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, X, y, collate_fn, show_progress, eps
            )
        return histories

    def predict(
        self,
        texts: Collection[str],
        max_length: int = None,
        n_jobs=-1,
        threshold: int = 0.5,
    ) -> np.ndarray:
        """
        :param texts:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        logits = self.logits(texts, max_length, n_jobs=n_jobs)
        return acc_predict(logits, threshold)

    def predict_classes(
        self,
        texts: Collection[str],
        max_length: int = None,
        n_jobs=-1,
        threshold: int = 0.5,
    ) -> list:
        """
        :param texts:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        pred = self.predict(texts, max_length, n_jobs, threshold)
        return self._predict_classes(pred.ravel())

    def predict_proba(
        self,
        texts: Collection[str],
        max_length: int = None,
        n_jobs=-1,
        threshold: int = 0.5,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        :param texts:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        logits = self.logits(texts, max_length, n_jobs=n_jobs)
        return self._proba(logits, threshold)

    def predict_classes_proba(
        self,
        texts: Collection[str],
        max_length: int = None,
        n_jobs=-1,
        threshold: int = 0.5,
    ) -> Tuple[list, np.ndarray]:
        """
        :param texts:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        indices, values = self.predict_proba(texts, max_length, n_jobs, threshold)
        return self._predict_classes(indices.ravel()), values

    def logits(
        self, texts: Collection[str], max_length: int = None, n_jobs=-1
    ) -> torch.Tensor:
        X = self.get_vec(texts, max_length, n_jobs=n_jobs)
        return super().logits(X)

    def evaluate(
        self,
        texts: Union[str, Collection[str], np.ndarray, pd.Series],
        y: Union[torch.LongTensor, np.ndarray, List],
        batch_size=64,
        num_workers=0,
        max_length: int = None,
        collate_fn=None,
        n_jobs=-1,
        threshold: int = 0.5,
    ) -> float:
        """return accuracy"""
        X = self.get_vec(texts, max_length, n_jobs=n_jobs)
        if isinstance(y, (np.ndarray, List)):
            y = torch.tensor(y, dtype=torch.long)
        return super().evaluate(X, y, batch_size, num_workers, collate_fn, threshold)

    def get_vec(
        self,
        texts: Union[str, Collection[str], np.ndarray, pd.Series],
        max_length: int,
        n_jobs: int,
    ):
        if isinstance(texts, str):
            texts = [texts]

        if isinstance(self.tokenize_vec, TokenizeVec):
            return self.tokenize_vec.parallel_encode_plus(
                texts,
                max_length=max_length,
                padding="max_length",
                truncation=True,
                add_special_tokens=True,
                return_token_type_ids=True,
                return_attention_mask=True,
                return_tensors="pt",
                n_jobs=n_jobs,
            )

        elif isinstance(
            self.tokenize_vec, (PaddingTokenizer, SimpleTokenizer, Tokenizer)
        ):
            return torch.LongTensor(self.tokenize_vec.batch_encode(texts, max_length))

        elif isinstance(self.tokenize_vec, TokenEmbedding):
            return self.tokenize_vec(texts, max_length)

        raise ValueError(
            "Invalid tokenize_vec, it must be a TokenizeVec or TokenEmbedding."
        )


class SplitTextModelWrapper(TextModelWrapper):
    """
    Examples
    --------
    >>> from nlpx.model.wrapper import SplitTextModelWrapper
    >>> model_wrapper = SplitTextModelWrapper(model, tokenize_vec, classes=classes)
    >>> model_wrapper.train(texts, y, collate_fn)
    >>> model_wrapper.predict(test_texts)
    >>> model_wrapper.evaluate(test_texts, y_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        tokenize_vec: Union[BaseTokenizer, TokenizeVec, TokenEmbedding],
        classes: Collection[str] = None,
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, tokenize_vec, classes, device)

    def train(
        self,
        texts: Union[Collection[str], np.ndarray, pd.Series],
        y: Union[torch.LongTensor, np.ndarray, List],
        max_length: int = None,
        val_size=0.2,
        random_state=None,
        collate_fn=None,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=64,
        eval_batch_size=128,
        num_workers=0,
        num_eval_workers=0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        n_jobs=-1,
        show_progress=True,
        eps=1e-5,
    ) -> dict:
        X = self.get_vec(texts, max_length=max_length, n_jobs=n_jobs)
        if 0.0 < val_size < 1.0:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=val_size, random_state=random_state
            )
            trainer = SimpleEvalClassTrainer(
                epochs,
                optimizer,
                scheduler,
                lr,
                T_max,
                batch_size,
                eval_batch_size,
                num_workers,
                num_eval_workers,
                pin_memory,
                pin_memory_device,
                persistent_workers,
                early_stopping_rounds,
                print_per_rounds,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, X, y, (X_test, y_test), collate_fn, show_progress, eps
            )
        else:
            trainer = SimpleClassTrainer(
                epochs,
                optimizer,
                scheduler,
                lr,
                T_max,
                batch_size,
                num_workers,
                pin_memory,
                pin_memory_device,
                persistent_workers,
                early_stopping_rounds,
                print_per_rounds,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, X, y, collate_fn, show_progress, eps
            )
        return histories


class PaddingTextModelWrapper(ClassifyModelWrapper):
    """
    Examples
    --------
    >>> from nlpx.model.wrapper import PaddingTextModelWrapper
    >>> model_wrapper = PaddingTextModelWrapper(model, tokenizer, classes=classes)
    >>> model_wrapper.train(train_texts, y_train val_data)
    >>> model_wrapper.predict(test_texts)
    >>> model_wrapper.evaluate(test_texts, y_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        tokenizer: Union[PaddingTokenizer, SimpleTokenizer, Tokenizer],
        classes: Collection[str] = None,
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, classes, device)
        self.tokenizer = tokenizer

    def train(
        self,
        texts: Union[Collection[str], np.ndarray, pd.Series],
        y: Union[torch.LongTensor, np.ndarray, List],
        val_data: Tuple[
            Union[Collection[str], np.ndarray, pd.Series],
            Union[torch.LongTensor, np.ndarray, List],
        ] = None,
        max_length: int = None,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=64,
        eval_batch_size=128,
        num_workers=0,
        num_eval_workers=0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
    ) -> dict:
        X = self.tokenizer.batch_encode(texts, padding=False)
        train_set = TokenDataset(X, y)
        val_set = None
        if val_data:
            X_val = self.tokenizer.batch_encode(val_data[0], padding=False)
            val_set = TokenDataset(X_val, val_data[1])

        return super().train(
            train_set,
            val_set,
            collate_fn=PaddingTokenCollator(self.tokenizer.pad, max_length),
            epochs=epochs,
            optimizer=optimizer,
            scheduler=scheduler,
            lr=lr,
            T_max=T_max,
            batch_size=batch_size,
            num_workers=num_workers,
            pin_memory=pin_memory,
            pin_memory_device=pin_memory_device,
            persistent_workers=persistent_workers,
            early_stopping_rounds=early_stopping_rounds,
            print_per_rounds=print_per_rounds,
            checkpoint_per_rounds=checkpoint_per_rounds,
            checkpoint_name=checkpoint_name,
            show_progress=show_progress,
            eps=eps,
        )

    def predict(
        self, texts: Collection[str], max_length: int = None, threshold: int = 0.5
    ) -> np.ndarray:
        """
        :param texts:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        logits = self.logits(texts, max_length)
        return acc_predict(logits)

    def predict_classes(
        self, texts: Collection[str], max_length: int = None, threshold: int = 0.5
    ) -> list:
        """
        :param texts:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        pred = self.predict(texts, max_length, threshold)
        return self._predict_classes(pred.ravel())

    def predict_proba(
        self, texts: Collection[str], max_length: int = None, threshold: int = 0.5
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        :param texts:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        logits = self.logits(texts, max_length)
        return self._proba(logits)

    def predict_classes_proba(
        self, texts: Collection[str], max_length: int = None, threshold: int = 0.5
    ) -> Tuple[list, np.ndarray]:
        """
        :param texts:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        indices, values = self.predict_proba(texts, max_length, threshold)
        return self._predict_classes(indices.ravel()), values

    def logits(self, texts: Collection[str], max_length: int = None) -> torch.Tensor:
        X = self.tokenizer.batch_encode(texts, max_length)
        X = torch.tensor(X, dtype=torch.long)
        return super().logits(X)

    def evaluate(
        self,
        texts: Union[str, Collection[str], np.ndarray, pd.Series],
        y: Union[torch.LongTensor, np.ndarray, List],
        batch_size=64,
        num_workers=0,
        max_length: int = None,
        threshold: int = 0.5,
    ) -> float:
        """return accuracy"""
        X = self.tokenizer.batch_encode(texts, padding=False)
        if isinstance(y, (np.ndarray, List)):
            y = torch.tensor(y, dtype=torch.long)
        val_set = TokenDataset(X, y)
        return super().evaluate(
            val_set,
            batch_size=batch_size,
            num_workers=num_workers,
            collate_fn=PaddingTokenCollator(self.tokenizer.pad, max_length),
            threshold=threshold,
        )


class SplitPaddingTextModelWrapper(PaddingTextModelWrapper):
    """
    Examples
    --------
    >>> from nlpx.model.wrapper import SplitPaddingTextModelWrapper
    >>> model_wrapper = SplitPaddingTextModelWrapper(tokenizer, classes=classes)
    >>> model_wrapper.train(model, texts, y)
    >>> model_wrapper.predict(test_texts)
    >>> model_wrapper.evaluate(test_texts, y_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        tokenizer: Union[PaddingTokenizer, SimpleTokenizer, Tokenizer],
        classes: Collection[str] = None,
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, tokenizer, classes, device)

    def train(
        self,
        texts: Union[Collection[str], np.ndarray, pd.Series],
        y: Union[torch.LongTensor, np.ndarray, List],
        max_length: int = None,
        val_size=0.2,
        random_state=None,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=64,
        eval_batch_size=128,
        num_workers=0,
        num_eval_workers=0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
    ) -> dict:
        X = self.tokenizer.batch_encode(texts, padding=False)
        if 0.0 < val_size < 1.0:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=val_size, random_state=random_state
            )
            train_set = TokenDataset(X_train, y_train)
            val_set = TokenDataset(X_test, y_test)
            trainer = EvalClassTrainer(
                epochs,
                optimizer,
                scheduler,
                lr,
                T_max,
                batch_size,
                eval_batch_size,
                num_workers,
                num_eval_workers,
                pin_memory,
                pin_memory_device,
                persistent_workers,
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model,
                train_set,
                val_set,
                PaddingTokenCollator(self.tokenizer.pad, max_length),
                show_progress,
                eps,
            )
        else:
            train_set = TokenDataset(X, y)
            trainer = ClassTrainer(
                epochs,
                optimizer,
                scheduler,
                lr,
                T_max,
                batch_size,
                num_workers,
                pin_memory,
                pin_memory_device,
                persistent_workers,
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model,
                train_set,
                PaddingTokenCollator(self.tokenizer.pad, max_length),
                show_progress,
                eps,
            )
        return histories
