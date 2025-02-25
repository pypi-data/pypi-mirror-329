from typing import List
import os
import pandas as pd
from datasets import Dataset
from transformers import PreTrainedTokenizerBase

NONE_RATIONALE = []

class HealthFC:
    NAME = "HealthFC"

    def __init__(self, tokenizer: PreTrainedTokenizerBase, data_dir: str):
        """
        Initialize the HealthFC dataset class.

        Args:
            tokenizer (PreTrainedTokenizerBase): The tokenizer to use.
            data_dir (str): The directory containing train, validation, and test files.
        """
        self.tokenizer = tokenizer

        # Load datasets
        self.train_dataset = self._load_dataset(data_dir)
        self.validation_dataset = self._load_dataset(data_dir)
        # (os.path.join(data_dir, "validation.csv"))
        self.test_dataset = self._load_dataset(data_dir)

    def _load_dataset(self, file_path: str) -> Dataset:
        """
        Load a dataset from a CSV file.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            Dataset: A Hugging Face Dataset object.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)

        # Convert the DataFrame to a Hugging Face Dataset
        return Dataset.from_pandas(df)

    def __len__(self):
        return self.len()

    def len(self, split_type: str = "test") -> int:
        if split_type == "train":
            return len(self.train_dataset)
        elif split_type == "validation":
            return len(self.validation_dataset)
        elif split_type == "test":
            return len(self.test_dataset)
        else:
            raise ValueError(
                f"{split_type} not supported as split_type. Specify one among: train, validation, or test."
            )

    def _get_item(self, idx: int, split_type: str = "test"):
        if split_type == "train":
            return self.train_dataset[idx]
        elif split_type == "validation":
            return self.validation_dataset[idx]
        elif split_type == "test":
            return self.test_dataset[idx]
        else:
            raise ValueError(
                f"{split_type} not supported as split_type. Specify one among: train, validation, or test."
            )

    def __getitem__(self, idx):
        # Default to the TEST_SET
        return self.get_instance(idx)

    def get_instance(self, idx, split_type: str = "test"):
        item_idx = self._get_item(idx, split_type)
        text = self._get_text(item_idx)
        tokens = (
            [self.tokenizer.cls_token]
            + self.tokenizer.tokenize(text)
            + [self.tokenizer.sep_token]
        )
        rationale = self._get_rationale(item_idx)
        true_label = self._get_ground_truth(item_idx)
        return {
            "text": text,
            "tokens": tokens,
            "rationale": rationale,
            "label": true_label,
        }

    def _get_text(self, item_idx) -> str:
        return item_idx["en_text"]

    def _get_rationale(self, item_idx) -> List[int]:
        if "en_explanation" in item_idx:
            rationale = item_idx["en_explanation"]
            return self.get_true_rationale_from_words_to_tokens(item_idx["en_text"].split(), rationale)
        return NONE_RATIONALE

    def _get_ground_truth(self, item_idx) -> int:
        return item_idx["label"]

    def get_true_rationale_from_words_to_tokens(
        self, word_based_tokens: List[str], words_based_rationales: List[int]
    ) -> List[int]:
        token_rationale = []
        for t, rationale_t in zip(word_based_tokens, words_based_rationales):
            converted_token = self.tokenizer.encode(t, add_special_tokens=False)
            for _ in converted_token:
                token_rationale.append(rationale_t)
        return token_rationale
