from .baseexplainer import BaseExplainer
from typing import Optional, Tuple, Union
from captum.attr import GuidedBackprop
from explanation import Explanation
import torch.nn as nn


class GuidedBackpropExplainer(BaseExplainer):
    NAME = "guidedbackprop"

    def __init__(
        self,
        model,
        tokenizer,
        device="cpu",
        **kwargs,
    ):
        super().__init__(model, tokenizer, **kwargs)

    class ForwardWrapper(nn.Module):
        """
        Wraps a custom forward function into an nn.Module.
        """

        def __init__(self, model):
            super().__init__()
            self.model = model

        def forward(self, inputs_embeds, attention_mask):
            outputs = self.model(inputs_embeds=inputs_embeds, attention_mask=attention_mask)
            return outputs.logits

    def compute_feature_importance(
        self,
        text: Union[str, Tuple[str, str]],
        target: Union[int, str] = 1,
        target_token: Optional[Union[int, str]] = None,
        show_progress: bool = False,
        **kwargs,
    ):
        """
        Compute feature importance using Guided Backpropagation.

        Args:
            text (Union[str, Tuple[str, str]]): Input text for which to compute importance.
            target (Union[int, str]): Target class or label.
            target_token (Optional[Union[int, str]]): Target token index for token-level tasks.
            show_progress (bool): Whether to show progress.
            **kwargs: Additional arguments passed to Guided Backpropagation.

        Returns:
            Explanation: An object containing tokens, scores, and metadata.
        """
        # Sanity checks
        target_pos_idx = self.text_classifier_engine.validate_target(target)
        target_token_pos_idx = None
        text = self.text_classifier_engine.validate_input(text)

        # Tokenize the input and get embeddings
        item = self._tokenize(text)
        input_ids = item["input_ids"]
        attention_mask = item["attention_mask"]
        input_len = item["attention_mask"].sum().item()

        # Get input embeddings
        inputs_embeds = self.model.get_input_embeddings()(input_ids)

        # Wrap the forward function into a PyTorch nn.Module
        forward_model = self.ForwardWrapper(self.model)

        # Initialize Guided Backpropagation
        gb = GuidedBackprop(forward_model)

        # Compute attributions
        attr = gb.attribute(
            inputs_embeds,
            target=target_pos_idx,
            additional_forward_args=(attention_mask,),
            **kwargs,
        )

        # Pool over hidden size to get a single score per token
        attr = attr[0, :input_len, :].detach().cpu().sum(-1).numpy()

        # Create Explanation object
        output = Explanation(
            text=text,
            tokens=self.get_tokens(text),
            scores=attr,
            explainer=self.NAME,
            target_pos_idx=target_pos_idx,
            target_token_pos_idx=target_token_pos_idx,
            target=self.text_classifier_engine.model.config.id2label[target_pos_idx],
            target_token= None
        )
        return output
