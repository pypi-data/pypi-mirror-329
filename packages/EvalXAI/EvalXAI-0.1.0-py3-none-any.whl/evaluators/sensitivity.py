# import torch
# import numpy as np
# from typing import Callable, Union, Optional
# from transformers import AutoTokenizer  # Assuming the use of Hugging Face transformers for tokenization

# class SensitivityEvaluator():
#     """Implementation of the sensitivity metric for text data.
    
#     Computes the sensitivity of the model's attributions for text data 
#     by adding noise to the input (perturbing individual tokens) and measuring
#     the change in attributions.

#     Attributes:
#         model (callable): model to explain
#         task (str): task to perform
#         device (str): device to use (CPU or GPU)
#         explainer (object): explainer to use
#         radius (float): radius for perturbation
#         tokenizer (AutoTokenizer): tokenizer for the text data

#     Methods:
#         get_noises: generates noise for perturbing the tokens
#         get_sens: computes the sensitivity score for text data
#     """
    
#     def __init__(
#         self,
#         model,
#         device: str,
#         explanations,
#         tokenizer,
#         radius: float = 0.5
#     ):
#         self.model = model.to(device)
#         self.tokenizer = tokenizer
#         self.device = device
#         self.requires_human_rationale=False
#         self.explanations = explanations if isinstance(explanations, list) else [explanations]
#         self.radius= radius

#     def get_noises(self, x_in: torch.Tensor, k: int = 5):
#         """Generate k perturbations (token-level noise) for the input text."""
#         n_shape = (k, x_in.shape[0], x_in.shape[1])  # k perturbations, batch size, sequence length
#         noise = torch.randint(0, len(self.tokenizer), n_shape, device=self.device)  # Random token indices
#         return noise

#     def get_sens(
#         self,
#         x_in: torch.Tensor,
#         label: Optional[Union[int, list, torch.Tensor]] = None,
#     ) -> float:
#         """Computes the sensitivity score for text data.
        
#         Args:
#             x_in (torch.Tensor): input text to compute the sensitivity score
#             label (Union[int, list, torch.Tensor], optional): labels of interest
#             attributions (torch.Tensor, optional): attributions for each instance
            
#         Returns:
#             float: sensitivity score
#         """
#         attributions = [explanation.scores for explanation in self.explanations]
#         attributions= torch.tensor(attributions)

#         self.check_shape(attributions, attributions)
        
#         # Generate noise (perturbations) for the text
#         noises = self.get_noises(attributions)
        
#         # If no attributions are provided, compute them using the explainer
#         if attributions is None:
#            raise ValueError("Attributions is None")
        
#         sensitivities = torch.zeros((len(noises), attributions.shape[0]), device=self.device)
        
#         # Loop over each perturbation (perturbed token sequence)
#         for j in range(len(noises)):
#             noise = noises[j]
#             pert_in = x_in.clone()
#             pert_in = pert_in.scatter_(1, noise, 0)  # Perturb tokens (e.g., replace with random tokens)
            
#             # Get the attributions for the perturbed input
#             pert_att = self.explainer.explain(pert_in, label=target)
            
#             # Calculate the difference in attributions (sensitivity)
#             sensitivity = torch.norm(attributions - pert_att, dim=1)
            
#             # Calculate the magnitude of the noise
#             rho = torch.norm(noise.flatten())
            
#             # Normalize the sensitivity by the noise magnitude
#             sensitivities[j] = sensitivity / rho
        
#         # Get the maximum sensitivity across all perturbations
#         all_sens = torch.max(sensitivities, dim=0).values
        
#         # Return the average sensitivity score
#         return 100 * torch.mean(all_sens, axis=0).item()


import torch
import numpy as np
from typing import Callable, Union, Optional
from transformers import AutoTokenizer  # Assuming the use of Hugging Face transformers for tokenization


class SensitivityEvaluator():
    """Implementation of the sensitivity metric for text data.
    
    Computes the sensitivity of the model's attributions for text data 
    by adding noise to the input (perturbing individual tokens) and measuring
    the change in attributions.

    Attributes:
        model (callable): model to explain
        task (str): task to perform
        device (str): device to use (CPU or GPU)
        explainer (object): explainer to use
        radius (float): radius for perturbation
        tokenizer (AutoTokenizer): tokenizer for the text data

    Methods:
        get_noises: generates noise for perturbing the tokens
        get_sens: computes the sensitivity score for text data
    """
    
    def __init__(
        self,
        model,
        tokenizer,
        explanations,
        device: str= "cpu",
        radius: float = 0.5
    ):
        self.model = model.to(device)
        self.tokenizer = tokenizer
        self.device = device
        self.requires_human_rationale=False
        self.explanations = explanations if isinstance(explanations, list) else [explanations]
        self.radius= radius

    def get_noises(self, x_in: torch.Tensor, k: int = 5):
        """Generate k perturbations (token-level noise) for the input text."""
        n_shape = (k, x_in.shape[0], x_in.shape[1])  # k perturbations, batch size, sequence length
        noise = torch.randint(0, len(self.tokenizer), n_shape, device=self.device)  # Random token indices
        return noise

    def compute(
        self
    ) -> float:
        """Computes the sensitivity score for text data from Explanation objects.
        
        Args:
            explanations (list): List of Explanation objects for each text
            attributions (torch.Tensor, optional): attributions for each instance
            
        Returns:
            float: sensitivity score
        """
        # Extract attributions (scores) directly from Explanation objects
        attributions = torch.tensor([explanation.scores for explanation in self.explanations], device=self.device)

        # Extract the labels (targets) directly from Explanation objects
        labels = [explanation.target for explanation in self.explanations]

        # Generate noise (perturbations) for the text
        noises = self.get_noises(attributions)

        sensitivities = torch.zeros((len(noises), len(self.explanations)), device=self.device)

        # Loop over each perturbation (perturbed token sequence)
        for j in range(len(noises)):
            noise = noises[j]
            
            # Perturb the text in each explanation (replace the tokens with noise)
            pert_in = []
            for i, explanation in enumerate(self.explanations):
                pert_tokens = explanation.tokens.copy()
                pert_tokens[explanation.target_pos_idx] = '<unk>'  # Example of perturbing the token
                pert_in.append(pert_tokens)

            # Get the attributions for the perturbed input for each label
            pert_attributions = []
            for i, pert_tokens in enumerate(pert_in):
                pert_text = ' '.join(pert_tokens)
                pert_attributions.append(self.explainer.explain(pert_text, label=labels[i]))

            pert_attributions = torch.tensor(pert_attributions, device=self.device)
            
            # Calculate the difference in attributions (sensitivity)
            sensitivity = torch.norm(attributions - pert_attributions, dim=1)
            
            # Calculate the magnitude of the noise
            rho = torch.norm(noise.flatten())
            
            # Normalize the sensitivity by the noise magnitude
            sensitivities[j] = sensitivity / rho
        
        # Get the maximum sensitivity across all perturbations
        all_sens = torch.max(sensitivities, dim=0).values
        
        # Return the average sensitivity score across the batch
        return 100 * torch.mean(all_sens, axis=0).item()
