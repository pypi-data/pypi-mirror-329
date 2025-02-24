import numpy as np
from captum.attr import Saliency
from .base_explainer import BaseExplainer


class SaliencyExplainer(BaseExplainer):
    def explain(self, text):
        """
        Generates a saliency map explanation.
        """
        inputs = self.tokenizer(
            text, return_tensors="pt", padding=True, truncation=True, max_length=128
        )
        input_ids = inputs["input_ids"].to(self.model.device)
        attention_mask = inputs["attention_mask"].to(self.model.device)

        embeddings = (
            self.model.bert.embeddings(input_ids).clone().detach().requires_grad_(True)
        )

        def forward_func(embeddings, attention_mask):
            outputs = self.model(
                inputs_embeds=embeddings, attention_mask=attention_mask
            )
            return outputs.logits[:, 0]

        saliency = Saliency(forward_func)
        attributions = saliency.attribute(
            embeddings, target=0, additional_forward_args=(attention_mask,)
        )

        tokens = self.tokenizer.convert_ids_to_tokens(input_ids[0])
        attributions = attributions.sum(dim=-1).squeeze(0).detach().cpu().numpy()
        attributions = attributions / (np.linalg.norm(attributions) + 1e-10)

        return tokens, attributions
