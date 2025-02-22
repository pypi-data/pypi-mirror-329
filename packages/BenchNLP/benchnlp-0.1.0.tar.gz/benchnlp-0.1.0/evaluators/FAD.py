import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from scipy.special import softmax
import torch
from scipy.integrate import trapz
from explanation import Explanation
from tqdm import tqdm

class FADEvaluator:
    """
    Class to evaluate the impact of feature (token) dropping on text data
    based on saliency scores (e.g., Gradient x Input).
    """
    NAME = "Feature Ablation Drop"

    def __init__(self, model, tokenizer, device="cpu", batch_size=32):
        """
        Initialize the evaluator.

        Args:
            model: The trained text classification model.
            tokenizer: Tokenizer used for the model.
            explanations: List of explanation objects.
            device: Device to run the evaluation (e.g., 'cuda' or 'cpu').
            batch_size: Number of samples to process in a batch.
        """
        self.model = model.to(device)
        self.tokenizer = tokenizer
        self.requires_human_rationale = False
        self.device = device
        self.batch_size = batch_size

    def _replace_tokens_with_baseline(self, tokens, saliency_scores, percent_to_drop):
        tokens_modified = tokens.copy()
        num_tokens_to_drop = int(len(tokens) * percent_to_drop / 100)
        saliency_sorted_indices = np.argsort(-np.abs(saliency_scores))
        tokens_to_replace = saliency_sorted_indices[:num_tokens_to_drop]

        baseline_token = self.tokenizer.mask_token
        for idx in tokens_to_replace:
            tokens_modified[idx] = baseline_token
        return tokens_modified

    def evaluate(self, explanations,percent_dropped_features):
        results = []
        for percent_to_drop in percent_dropped_features:
            # print(f"percent to drop {percent_to_drop}")
            predictions, labels = [], []

            for i in range(0, len(explanations), self.batch_size):
                batch_explanations = explanations[i:i + self.batch_size]
                batch_texts = []
                batch_labels = []

                for exp in batch_explanations:
                    tokens = exp.tokens
                    saliency_scores = np.array(exp.scores)
                    label = exp.target_pos_idx

                    modified_tokens = self._replace_tokens_with_baseline(tokens, saliency_scores, percent_to_drop)
                    modified_text = self.tokenizer.convert_tokens_to_string(modified_tokens)
                    batch_texts.append(modified_text)
                    batch_labels.append(label)

                encoded_inputs = self.tokenizer(batch_texts, return_tensors="pt", truncation=True, max_length=512, padding=True).to(self.device)
                with torch.no_grad():
                    logits = self.model(**encoded_inputs).logits
                batch_predictions = torch.argmax(logits, dim=1).cpu().numpy()

                predictions.extend(batch_predictions)
                labels.extend(batch_labels)

            accuracy = accuracy_score(labels, predictions)
            results.append({"Percent Dropped": percent_to_drop, "Accuracy": accuracy})

        return pd.DataFrame(results)

    def calculate_n_auc(self, results_df, percent_range=(0, 20)):
        filtered_results = results_df[(results_df["Percent Dropped"] >= percent_range[0]) &
                                      (results_df["Percent Dropped"] <= percent_range[1])]
        x = filtered_results["Percent Dropped"].values
        y = filtered_results["Accuracy"].values
        auc = trapz(y, x)
        max_auc = (x[-1] - x[0]) * max(y)
        return auc / max_auc if max_auc > 0 else 0.0

    def plot_results(self, results_df):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(8, 5))
        plt.plot(results_df["Percent Dropped"], results_df["Accuracy"], marker="o", label="Accuracy")
        plt.xlabel("Percent of Tokens Dropped")
        plt.ylabel("Accuracy")
        plt.title("Impact of Dropping Top Tokens on Accuracy")
        plt.grid()
        plt.legend()
        plt.show()

    def compute(self, explanations,percent_dropped_features=None, percent_range=(0, 20)):
        explanations= explanations if isinstance(explanations, list) else [explanations]
        if percent_dropped_features is None:
            percent_dropped_features = list(range(0, 41, 10))

        results_df = self.evaluate(explanations,percent_dropped_features)
        final_n_auc = self.calculate_n_auc(results_df, percent_range)
        # self.plot_results(results_df)
        return final_n_auc
