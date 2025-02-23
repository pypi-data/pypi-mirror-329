import numpy as np
import torch
from captum.attr import LayerConductance

from .base_explainer import BaseExplainer


class LRPExplainer(BaseExplainer):
    def explain(self, text):
        """
        Generates an explanation using Layer-wise Relevance Propagation (LRP).
        """
        inputs = self.prepare_inputs(text)
        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]

        embeddings = (
            self.model.bert.embeddings(input_ids).clone().detach().requires_grad_(True)
        )
        with torch.no_grad():
            original_outputs = self.model(**inputs)
            aggregated_logits = original_outputs.logits.mean(dim=1)
        target = torch.argmax(aggregated_logits, dim=-1)[0].item()

        def forward_func(embeddings, attention_mask):
            outputs = self.model(
                inputs_embeds=embeddings, attention_mask=attention_mask
            )
            return outputs.logits[:, 0]

        lc = LayerConductance(forward_func, self.model.bert.embeddings)
        attributions = lc.attribute(
            embeddings, additional_forward_args=(attention_mask,), target=target
        )
        tokens = self.tokenizer.convert_ids_to_tokens(input_ids[0])
        attributions = attributions.sum(dim=-1).squeeze(0).detach().cpu().numpy()
        attributions = attributions / (np.linalg.norm(attributions) + 1e-10)
        return tokens, attributions
