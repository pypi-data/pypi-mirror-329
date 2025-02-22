
import numpy as np
from sklearn.metrics import auc, precision_recall_curve
from explanation import Explanation


class AUPRCEvaluator:
    """
    Class to evaluate saliency explanations using AUPRC (Area Under the Precision-Recall Curve).
    """
    NAME = "Area under PR Curve"

    def __init__(self, model, tokenizer):
        """
        Initialize the evaluator.

        Args:
            model: The model used for generating explanations.
            tokenizer: The tokenizer used for processing text.
            explanations: Precomputed saliency scores as a list or a single explanation object.
        """
        self.model = model
        self.tokenizer = tokenizer
        self.requires_human_rationale = True

    @staticmethod
    def calculate_auprc(saliency_scores: list[float], human_rationale: list[int]) -> float:
        """
        Calculate AUPRC for a single instance using sklearn's precision_recall_curve.

        Args:
            saliency_scores (list of float): Saliency scores for a single instance.
            human_rationale (list of int): Ground-truth rationale mask for the instance.

        Returns:
            float: AUPRC score for the instance.
        """
        if human_rationale is None or saliency_scores is None or len(saliency_scores) == 0 or len(human_rationale) == 0:
            return None  # Skip empty inputs
        
        # Remove [CLS] and [SEP] tokens
        saliency_scores = saliency_scores[1:-1]
        human_rationale = human_rationale[:len(saliency_scores)]
        # Compute precision-recall and AUC
        precision, recall, _ = precision_recall_curve(human_rationale, saliency_scores)
        return auc(recall, precision)

    def evaluate_instance(self, explanation: Explanation, human_rationale: list[int]) -> float:
        """
        Evaluate AUPRC for a single instance.

        Args:
            explanation (Explanation): Explanation object containing saliency scores.
            human_rationale (list of int): Ground-truth rationale for the instance.

        Returns:
            float: AUPRC score for the instance.
        """
        saliency_scores = explanation.scores
        return self.calculate_auprc(saliency_scores, human_rationale)

    def evaluate(self,explanations) -> float:
        """
        Evaluate AUPRC for all instances in the dataset or for a single instance.

        Args:
            human_rationales (list of list of int, optional): List of ground-truth rationales or a single rationale.

        Returns:
            float: Average AUPRC score across all instances.
        """        
        # Single instance evaluation
        if len(explanations) == 1:
            human_rationales = explanations[0].rationale
            if human_rationales is None:
                raise ValueError("Human rationale is required to compute this metric.")
            return self.evaluate_instance(explanations[0], human_rationales)

        # Dataset evaluation
        auprc_scores = []
        for exp in explanations:
            human_rationales = exp.rationale
            score = self.evaluate_instance(exp, exp.rationale)
            if score is not None:
                auprc_scores.append(score)

        # Average AUPRC across all instances
        return np.mean(auprc_scores) if auprc_scores else 0.0

    def compute(self, explanations) -> float:
        """
        Evaluate AUPRC for the entire dataset or a single instance.

        Args:
            human_rationales (list of list of int, optional): List of ground-truth rationales.

        Returns:
            float: Average AUPRC score across the dataset or for a single instance.
        """
     
        explanations = explanations if isinstance(explanations, list) else [explanations]

        # Compute AUPRC
        average_auprc = self.evaluate(explanations)
        return average_auprc
