import torch

from .base_explainer import BaseExplainer


class AttentionExplainer(BaseExplainer):
    def explain(self, text):
        """
        Generates an explanation based on attention scores.
        """
        inputs = self.prepare_inputs(text)
        input_ids = inputs["input_ids"]
        with torch.no_grad():
            outputs = self.model(**inputs, output_attentions=True)
            attentions = outputs.attentions
        attention_scores = attentions[-1].mean(dim=1).squeeze(0).detach().cpu().numpy()
        tokens = self.tokenizer.convert_ids_to_tokens(input_ids[0])
        return tokens, attention_scores
