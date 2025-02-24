import numpy as np
from captum.attr import IntegratedGradients

from .base_explainer import BaseExplainer


class IntegratedGradientsExplainer(BaseExplainer):
    def explain(self, text):
        """
        Generates an Integrated Gradients explanation.
        """
        inputs = self.prepare_inputs(text)
        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]
        embeddings = (
            self.model.bert.embeddings(input_ids).clone().detach().requires_grad_(True)
        )

        def forward_func(embeddings, attention_mask):
            outputs = self.model(
                inputs_embeds=embeddings, attention_mask=attention_mask
            )
            return outputs.logits[:, 0]

        ig = IntegratedGradients(forward_func)
        attributions, _ = ig.attribute(
            embeddings,
            target=0,
            additional_forward_args=(attention_mask,),
            return_convergence_delta=True,
        )
        tokens = self.tokenizer.convert_ids_to_tokens(input_ids[0])
        attributions = attributions.sum(dim=-1).squeeze(0).detach().cpu().numpy()
        attributions = attributions / (np.linalg.norm(attributions) + 1e-10)
        return tokens, attributions
