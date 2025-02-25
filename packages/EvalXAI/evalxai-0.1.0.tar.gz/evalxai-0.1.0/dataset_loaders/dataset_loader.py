from dataclasses import dataclass
from datasets import load_dataset
from typing import List, Optional, Dict
import numpy as np

@dataclass
class LoadDatasetArgs:
    dataset_name: str  # The dataset name, e.g., "imdb", "ag_news"
    input_text_field: str  # The field containing the input text for classification (e.g., "text")
    label_field: str  # The field containing the label for classification (e.g., "label")
    rationale_field: Optional[str] = None
    dataset_config: Optional[str] = None  # The configuration for the dataset (if any)
    dataset_dir: Optional[str] = None  # Path to the dataset directory (if any)
    dataset_files: Optional[List[str]] = None  # Paths to the dataset files (if any)
    dataset_split: Optional[str] = "train"  # Dataset split to load (e.g., "train", "test", etc.)
    dataset_revision: Optional[str] = None  # The dataset revision (if any)
    dataset_auth_token: Optional[str] = None  # Auth token for the dataset if needed
    dataset_kwargs: Optional[Dict] = None  # Additional keyword arguments for loading the dataset


def load_fields_from_dataset(dataset_args: LoadDatasetArgs) -> Dict[str, List]:
        """
        Loads the text, labels, and optionally rationales from a text classification dataset, and returns them as a dictionary.

        Args:
            dataset_args (LoadDatasetArgs): Arguments for loading the dataset.

        Returns:
            Dict[str, List]: A dictionary containing lists of input texts, corresponding labels, and optionally rationales.
        """
        try:
            dataset = load_dataset(
                dataset_args.dataset_name,
                dataset_args.dataset_config,
                data_dir=dataset_args.dataset_dir,
                data_files=dataset_args.dataset_files,
                split=dataset_args.dataset_split,
                revision=dataset_args.dataset_revision,
                token=dataset_args.dataset_auth_token,
                **(dataset_args.dataset_kwargs or {}),
                trust_remote_code=True
            )

            df = dataset.to_pandas()

            if dataset_args.input_text_field not in df.columns:
                raise ValueError(f"The input text field '{dataset_args.input_text_field}' does not exist in the dataset.")

            input_texts = list(df[dataset_args.input_text_field])

            if dataset_args.label_field not in df.columns:
                raise ValueError(f"The label field '{dataset_args.label_field}' does not exist in the dataset.")

            labels = list(df[dataset_args.label_field])

            rationales = None
            if dataset_args.rationale_field and dataset_args.rationale_field in df.columns:
                rationales = list(df[dataset_args.rationale_field])

            return input_texts, labels, rationales
        except Exception as e:
            print(f"Error loading fields from dataset: {e}")
            return {}, [], []