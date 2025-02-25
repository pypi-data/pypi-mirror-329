import torch
import numpy as np
import pandas as pd


class ComplexityEvaluator:
    """
    Class to evaluate the complexity of token-level attributions for text data.

    Computes the entropy of the fractional contribution of each token
    to measure the complexity of the attributions.

    References:
        - `Evaluating and Aggregating Feature-based Model Explanations
        <https://arxiv.org/abs/2005.00631>`
    """
    NAME = "Complexity"


    def __init__(self, model, tokenizer, device="cpu"):
        """
        Initialize the evaluator.

        Args:
            model: The trained text classification model.
            tokenizer: Tokenizer used for the model.
            saliency_scores: Precomputed saliency scores for tokens.
            device: Device to run the evaluation (e.g., 'cuda' or 'cpu').
        """
        self.model = model.to(device)
        self.tokenizer = tokenizer
        self.requires_human_rationale=False
        self.device = device

    def _total_contribution(self, attributions: np.ndarray) -> np.ndarray:
        """
        Compute the total contribution for each instance.

        Args:
            attributions (np.ndarray): Saliency scores (batch_size, seq_len).

        Returns:
            np.ndarray: Total contribution for each instance (batch_size,).
        """
        return np.sum(np.abs(attributions), axis=1)

    def _fractional_contribution(
        self, attributions: np.ndarray, feature_index: int
    ) -> np.ndarray:
        """
        Compute the fractional contribution of a specific feature.

        Args:
            attributions (np.ndarray): Saliency scores (batch_size, seq_len).
            feature_index (int): Index of the feature.

        Returns:
            np.ndarray: Fractional contribution of the feature (batch_size,).
        """
        total_contrib = self._total_contribution(attributions)
        return np.abs(attributions[:, feature_index]) / (total_contrib + 1e-8)

    def compute_complexity(self, attributions: np.ndarray) -> np.ndarray:
        """
        Compute the complexity score for the given attributions.

        Args:
            attributions (np.ndarray): Saliency scores (batch_size, seq_len).

        Returns:
            float: Complexity score for the batch.
        """
        # Ensure attributions are 2D
        if attributions.ndim == 1:
            attributions = attributions.reshape(1, -1)  # Reshape to (1, seq_len)
        
        batch_size, seq_len = attributions.shape
        complexity = np.zeros(batch_size)

        for feature_index in range(seq_len):
            frac_contrib = self._fractional_contribution(attributions, feature_index)
            complexity += -frac_contrib * np.log(frac_contrib + 1e-8)

        complexity = complexity / seq_len
        return np.mean(complexity)

    def evaluate(self,explanations, split_type="test"):
        """
        Evaluate the complexity of attributions for the given dataset split.

        Args:
            split_type (str): Dataset split to evaluate (e.g., 'test').

        Returns:
            pd.DataFrame: DataFrame with complexity scores for each instance.
        """
        results = []
        for idx, exp in enumerate(explanations):
            # print(idx)
            text = exp.text
            attributions = np.array(exp.scores)

            # Compute complexity for the current instance
            complexity_score = self.compute_complexity(attributions)
            # print(f"score {complexity_score}")
            results.append({"Instance": idx, "Text": text, "Complexity": complexity_score})

        return pd.DataFrame(results)


    def compute(self, explanations):
        """
        Compute the average complexity across the dataset.

        Args:
            dataset: The dataset object (e.g., MovieReviews).
            model: The trained text classification model.
            tokenizer: Tokenizer used to tokenize inputs for the model.
            saliency_scores: Precomputed saliency scores for each sample in the dataset.
            device: Device to run the computations on (e.g., 'cuda' or 'cpu').

        Returns:
            float: The average complexity score across the dataset.
        """
        explanations= explanations if isinstance(explanations, list) else [explanations]
        # Perform the evaluation
        results_df = self.evaluate(explanations,split_type="test")
        # Calculate the average complexity score
        avg_complexity = results_df["Complexity"].mean()

        return avg_complexity
