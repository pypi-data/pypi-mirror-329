import torch
import torch.nn.functional as F
from torch import nn
from transformers import BertTokenizerFast, BertForSequenceClassification
import numpy as np
from explainers import InputXGradientExplainer
import os
from dataset_loaders import MovieReviews
from tqdm import tqdm

class SoftSufficiencyEvaluator:
    
    NAME = "Soft Sufficiency"

    def __init__(self, model, tokenizer, max_len=512, device='cpu'):
        """
        Initializes the Soft Normalized Sufficiency computation.
        
        Args:
            model (nn.Module): The pre-trained model (e.g., BERT).
            tokenizer (transformers.Tokenizer): Tokenizer used to tokenize text inputs.
            max_len (int): Maximum token length to which the input should be padded/truncated.
            importance_scores (torch.Tensor): Importance scores for tokens (shape: batch_size, seq_len).
            device (str): Device to use for computation ('cuda' or 'cpu').
        """
        self.model = model.to(device)
        self.tokenizer = tokenizer
        self.max_len = max_len
        # self.explanations = explanations
        self.requires_human_rationale=False
        self.device = device

    def soft_perturb(self, embeddings, importance_scores, attention_mask):
        """
        Applies soft perturbation to the token embeddings based on the importance scores.
        
        Args:
            embeddings (torch.Tensor): The token embeddings (batch_size, seq_len, embedding_dim).
            importance_scores (torch.Tensor): Importance scores for each token in the sequence (batch_size, seq_len).
            attention_mask (torch.Tensor): Attention mask to indicate the padding positions (batch_size, seq_len).
        
        Returns:
            torch.Tensor: Perturbed token embeddings.
        """
        batch_size, seq_len, embed_dim = embeddings.size()  # Get dimensions of embeddings
        
        # Ensure that importance_scores is of shape (batch_size, seq_len)
        importance_scores = importance_scores.unsqueeze(-1)  # Shape: (batch_size, seq_len, 1)
        
        # Apply mask to ignore padding tokens during perturbation
        attention_mask = attention_mask.unsqueeze(-1).float()  # Shape: (batch_size, seq_len, 1)

        if importance_scores.size(1) != attention_mask.size(1):
            # Pad or truncate importance_scores to match attention_mask size
            padding_len = attention_mask.size(1) - importance_scores.size(1)
            if padding_len > 0:
                # Padding the importance scores
                padding = torch.zeros(importance_scores.size(0), padding_len, 1).to(self.device)
                importance_scores = torch.cat((importance_scores, padding), dim=1)
            elif padding_len < 0:
                # Truncating importance scores
                importance_scores = importance_scores[:, :attention_mask.size(1), :]
        
        normalized_importance_scores = (importance_scores - importance_scores.min()) / (importance_scores.max() - importance_scores.min())
        # Create a Bernoulli mask based on importance scores (probability of keeping each element)
        mask = torch.bernoulli(normalized_importance_scores).to(embeddings.device)  # Shape: (batch_size, seq_len, 1)
        
        # Apply the attention mask (this will zero out the padding tokens)
        mask = mask * attention_mask  # Shape: (batch_size, seq_len, 1)
       
        perturbed_embeddings = embeddings * mask

        return perturbed_embeddings

    def sufficiency_(self,full_text_probs : np.array, reduced_probs : np.array) -> np.array:
        sufficiency = 1 - np.maximum(0, full_text_probs - reduced_probs)

        return sufficiency


    def compute_sufficiency(self, original_input, perturbed_input, calculate_baseline=False):
        """
        Computes the soft sufficiency score based on the change in model predictions.

        Args:
            original_input (dict): The input dictionary for the model with original tokens.
            perturbed_input (dict): The input dictionary for the model with perturbed tokens.
            calculate_baseline (bool): If True, computes baseline sufficiency where all tokens are zeroed/masked.
        
        Returns:
            tuple: The computed sufficiency score and baseline sufficiency score (if requested).
        """
        # Get model prediction on original input
        original_output = self.model(**original_input)
        original_prediction = F.softmax(original_output.logits, dim=-1).detach().cpu().numpy()
        # print(f"original_prediction {original_prediction}")
        full_text_probs = original_prediction.max(-1)
        full_text_class = original_prediction.argmax(-1)
       
        rows= np.arange(original_input["input_ids"].size(0))
       
        if calculate_baseline:
            baseline_input = original_input.copy()
            baseline_input['input_ids'] = torch.zeros_like(original_input['input_ids']).long()
            batch= baseline_input
            # print(f"batch baseline{batch}")
        else:
            batch= perturbed_input
            # print(f"batch perturbed{batch}")

        yhat= self.model(**batch)
        yhat_probs = F.softmax(yhat.logits, dim=-1).detach().cpu().numpy()
        reduced_probs = yhat_probs[rows, full_text_class]
        # Compute sufficiency for perturbed input
        sufficiency = self.sufficiency_(full_text_probs, reduced_probs)
        
        return sufficiency

    def normalize_sufficiency(self, sufficiency, baseline_sufficiency):
        """
        Normalizes the sufficiency score to the range [0, 1].

        Args:
            sufficiency (float): The raw sufficiency score.
            baseline_sufficiency (float): The baseline sufficiency score (when no perturbation).
        
        Returns:
            float: The normalized sufficiency score.
        """
        baseline_sufficiency -= 1e-4 ## to avoid nan
        normalized_suff =  np.maximum(0,(sufficiency - baseline_sufficiency) / (1 - baseline_sufficiency)) 
        # print(f"normalized sufficiency {normalized_suff}")
        normalized_suff = np.clip(normalized_suff, 0, 1)  # Ensure it is between 0 and 1
        
        return normalized_suff

    def compute_single_instance(self, explanation, batch_size=1):
        """
        Computes Soft Normalized Sufficiency for the given input sentences.
        
        Args:
            original_sentences (list or torch.Tensor): List of raw sentences.
            batch_size (int): Number of sentences to process in each batch.
        
        Returns:
            tuple: The normalized sufficiency scores and model predictions.
        """
        original_sentences= explanation.text
        importance_scores= explanation.scores
        importance_scores = torch.tensor(importance_scores).unsqueeze(-1)
        # Tokenize the sentences
        original_input = self.tokenizer(original_sentences, padding=True, truncation=True, 
                                max_length=self.max_len, return_tensors="pt").to(self.device)
        
        # Get embeddings (using the model's outputs)
        with torch.no_grad():
            outputs = self.model(**original_input, output_hidden_states=True)
            original_embeddings = outputs.hidden_states[-1]

        
        # Apply soft perturbation based on importance scores
        perturbed_embeddings = self.soft_perturb(original_embeddings, importance_scores, original_input['attention_mask'])
        # Create a perturbed input dictionary (copy the original input and update input_ids)
        perturbed_input = original_input.copy()
        perturbed_input['input_ids'] = perturbed_embeddings.argmax(dim=-1)  # Convert embeddings to token IDs for input
        
        # Compute the sufficiency score based on the perturbed input
        baseline_sufficiency= self.compute_sufficiency(original_input, perturbed_input, calculate_baseline=True)
        sufficiency= self.compute_sufficiency(original_input, perturbed_input, calculate_baseline=False)

        # print(f"Sufficiency: {sufficiency}, Baseline Sufficiency: {baseline_sufficiency}")

        # Normalize the sufficiency score
        normalized_sufficiency = self.normalize_sufficiency(sufficiency, baseline_sufficiency)
        return [normalized_sufficiency]
        
    def compute(self,explanations):

        """
        Computes Soft Normalized Sufficiency for all samples in the dataset.
        
        Args:
            dataset (MovieReviews): The dataset object.
            model (nn.Module): The pre-trained model (e.g., BERT).
            tokenizer (transformers.Tokenizer): Tokenizer used to tokenize text inputs.
            precomputed_scores (list): List of precomputed saliency scores for each sample.
            max_len (int): Maximum token length to which the input should be padded/truncated.
            batch_size (int): Number of sentences to process in each batch.
        
        Returns:
            list: List of normalized sufficiency scores for all samples.
            list: List of model predictions for all samples.
        """
        explanations = explanations if isinstance(explanations, list) else [explanations]

        all_normalized_sufficiency = []
        all_predictions = []
        for i in range(0, len(explanations)):

            # Compute Soft Normalized Sufficiency for the batch
            normalized_sufficiency= self.compute_single_instance(explanations[i])
            # Append results to the lists
            all_normalized_sufficiency.extend(normalized_sufficiency)
            # all_predictions.extend(model_predictions)

        # Calculate the cumulative value (average) of sufficiency scores
        cumulative_sufficiency = np.mean(all_normalized_sufficiency)
        
        return cumulative_sufficiency

#    for i in tqdm(range(0, len(self.explanations)), desc="Computing Soft Sufficiency"):
#             original_sentence= self.explanations[i].text
#             print(original_sentence)
#         for i in range(0, len(precomputed_scores)): #len(precomputed_scores)
#             print(i)
#             instance = dataset.get_instance(i, split_type='test') 
#             original_sentence= instance['text']        
#             # Ensure the instance and entry are aligned
#             if instance["text"] != precomputed_scores[i]["text"][0]:
#                 print(f"Mismatch! Instance text: {instance['text']}, Saliency text: {precomputed_scores[i]['text'][0]}")
#                 return
#             # Extract the importance scores for each sample in the batch
#             saliency_scores = precomputed_scores[i]['saliency_scores']
#             #Pad the importance scores to the max_len (512)
#             padded_saliency_scores = []
    
#             if len(saliency_scores) < max_len:
#                 # Pad with zeros (assuming no importance for padding tokens)
#                 padded_score = torch.cat([torch.tensor(saliency_scores), torch.zeros(max_len - len(saliency_scores))])
#             else:
#                     # Truncate if the length exceeds max_len
#                 padded_score = torch.tensor(saliency_scores[:max_len])
            
#             # print(f"padded_score {padded_score}")
#             padded_saliency_scores.append(padded_score)

#             # Convert to a tensor and move to the correct device
#             importance_scores = torch.stack(padded_saliency_scores).to(model.device)

#             Initialize SoftNS with the importance scores
