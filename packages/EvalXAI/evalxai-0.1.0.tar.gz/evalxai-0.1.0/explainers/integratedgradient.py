from .baseexplainer import BaseExplainer
from typing import Optional, Tuple, Union
import torch
from captum.attr import InputXGradient, IntegratedGradients, Saliency
from explanation import Explanation
class IntegratedGradientsExplainer(BaseExplainer):
    NAME = "integratedgradient"

    def __init__(
        self,
        model,
        tokenizer,
        device= "cpu",
        **kwargs,
    ):
        super().__init__(model, tokenizer, **kwargs)

    def _generate_baselines(self, input_len):
        ids = (
            [self.text_classifier_engine.tokenizer.cls_token_id]
            + [self.text_classifier_engine.tokenizer.pad_token_id] * (input_len - 2)
            + [self.text_classifier_engine.tokenizer.sep_token_id]
        )
        embeddings = self.text_classifier_engine._get_embeddings_from_ids(
            torch.tensor(ids, device=self.device)
        )
        return embeddings.unsqueeze(0)

    def compute_feature_importance(
        self,
        text: Union[str, Tuple[str, str]],
        target: Union[int, str] = 1,
        target_token: Optional[Union[int, str]] = None,
        show_progress: bool = False,
        **kwargs,
    ):
      
        target_pos_idx = self.text_classifier_engine.validate_target(target)
        target_token_pos_idx = None
        text = self.text_classifier_engine.validate_input(text)

        def func(input_embeds):
            attention_mask = torch.ones(
                *input_embeds.shape[:2], dtype=torch.uint8, device=self.device
            )
            _, logits = self.text_classifier_engine._forward_with_input_embeds(
                input_embeds, attention_mask, show_progress=show_progress
            )
            return logits

        item = self._tokenize(text)
        input_len = item["attention_mask"].sum().item()
        dl = IntegratedGradients(
            func, **self.init_args, multiply_by_inputs=False
        )
        inputs = self.get_input_embeds(text)
        baselines = self._generate_baselines(input_len)
        attr = dl.attribute(inputs, baselines=baselines, target=target_pos_idx, **kwargs)

        attr = attr[0, :input_len, :].detach().cpu()

        # pool over hidden size
        attr = attr.sum(-1).numpy()
       
        # norm_attr = self._normalize_input_attributions(attr.detach())
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
