import numpy as np
from utils.saliency_utils import top_k_selection

class IOUEvaluator:
    NAME = "Intersection Over Union (IOU)"
    """
    Class to evaluate faithfulness of saliency explanations using discrete metrics,
    including F1 IOU score.
    """

    def __init__(self, model, tokenizer):
        """
        Initialize the evaluator.

        Args:
            model: The model used for predictions.
            tokenizer: Tokenizer used to process text.
            explanations: Explanation object or list of Explanation objects.
        """
        self.model = model
        self.tokenizer = tokenizer
        self.requires_human_rationale = True
        self.avg_rationale_length=None 

    def calculate_avg_rationale_length(self,explanations):
        """
        Calculate the average length of human rationales across the explanations.

        Returns:
            int: Average length of rationales.
        """
        rationale_lengths = [
            len([r for r in exp.scores if r == 1]) for exp in explanations
        ]
        return int(np.mean(rationale_lengths)) if rationale_lengths else 0

    @staticmethod
    def calculate_discrete_metrics(predicted, ground_truth):
        """
        Calculate discrete metrics including IOU, Precision, Recall, and F1.

        Args:
            predicted: Predicted binary rationale array.
            ground_truth: Ground truth binary rationale array.

        Returns:
            dict: Metrics including IOU, Precision, Recall, and F1.
        """
        predicted_set = set(np.where(predicted == 1)[0])
        ground_truth_set = set(np.where(ground_truth == 1)[0])

        intersection = len(predicted_set & ground_truth_set)
        union = len(predicted_set | ground_truth_set)

        iou = intersection / union if union > 0 else 0.0
        precision = intersection / len(predicted_set) if predicted_set else 0.0
        recall = intersection / len(ground_truth_set) if ground_truth_set else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

        return {"IOU": iou, "Precision": precision, "Recall": recall, "F1": f1}

    def evaluate_instance(self, explanation, human_rationale, k=None):
        """
        Evaluate metrics for a single instance.

        Args:
            explanation: Explanation object for the instance.
            human_rationale: Human-provided rationale for the instance.
            k: Number of top tokens to select. Defaults to average rationale length.

        Returns:
            dict: Metrics including IOU, Precision, Recall, and F1.
        """

        saliency_scores = explanation.scores[1:-1]  # Exclude special tokens ([CLS], [SEP])
        ground_truth_rationale = human_rationale[:len(saliency_scores)]
        k = k or self.avg_rationale_length
        predicted_rationale = top_k_selection(np.array(saliency_scores), k)
        return self.calculate_discrete_metrics(predicted_rationale, np.array(ground_truth_rationale))

    def evaluate(self,explanations):
        """
        Evaluate metrics for the entire dataset or a single instance.

        Args:
            human_rationales: List of human rationales (dataset) or a single rationale (single instance).

        Returns:
            dict: Metrics for the dataset or a single instance.
        """
        if not isinstance(explanations, list):
            explanations = [explanations]  # Convert to list if it's a single Explanation       

        # Dataset evaluation
        metrics_list = []
        for exp in explanations:
            if exp.rationale is None:
                print("No rationale provided for the instance. Skipping evaluation.")
                continue
            metrics = self.evaluate_instance(exp, exp.rationale)
            metrics_list.append(metrics)

        # Compute average metrics
        average_metrics = {
            "IOU": np.mean([m["IOU"] for m in metrics_list]),
            "F1": np.mean([m["F1"] for m in metrics_list]),
        }
        IOU=np.mean([m["IOU"] for m in metrics_list])
        return IOU

    def compute(self,explanations):
        """
        Compute metrics for the entire dataset or a single instance.

        Args:
            human_rationales: List of human rationales or a single rationale.

        Returns:
            dict: Metrics for the dataset or a single instance.
        """
        explanations = explanations if isinstance(explanations, list) else [explanations]

        self.avg_rationale_length=self.calculate_avg_rationale_length(explanations)
        return self.evaluate(explanations)