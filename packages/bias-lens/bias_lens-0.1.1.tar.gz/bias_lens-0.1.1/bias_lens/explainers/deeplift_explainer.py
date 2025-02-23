import numpy as np
import torch
from captum.attr import DeepLift

from .base_explainer import BaseExplainer


class DeepLiftExplainer(BaseExplainer):
    def explain(self, text):
        """
        Generates a DeepLIFT explanation.
        """
        inputs = self.prepare_inputs(text)
        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]
        embeddings = (
            self.model.bert.embeddings(input_ids).clone().detach().requires_grad_(True)
        )
        wrapped_model = ModelWrapper(self.model)
        deeplift = DeepLift(wrapped_model)
        attributions = deeplift.attribute(
            embeddings,
            baselines=torch.zeros_like(embeddings),
            target=0,
            additional_forward_args=(attention_mask,),
            return_convergence_delta=False,
        )
        tokens = self.tokenizer.convert_ids_to_tokens(input_ids[0])
        attributions = attributions.sum(dim=-1).squeeze(0).detach().cpu().numpy()
        attributions = attributions / (np.linalg.norm(attributions) + 1e-10)
        return tokens, attributions


class ModelWrapper(torch.nn.Module):
    """
    Wraps the model to work with DeepLift.
    """

    def __init__(self, model):
        super(ModelWrapper, self).__init__()
        self.model = model

    def forward(self, embeddings, attention_mask):
        outputs = self.model(inputs_embeds=embeddings, attention_mask=attention_mask)
        return outputs.logits[:, 0]
