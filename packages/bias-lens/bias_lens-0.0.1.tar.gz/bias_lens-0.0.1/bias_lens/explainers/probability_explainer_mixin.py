import numpy as np
import torch

from .base_explainer import BaseExplainer


class ProbabilityExplainerMixin(BaseExplainer):
    def predict_proba(self, texts):
        """
        Returns averaged probabilities per label for the given texts.
        This method is used by LIME and SHAP explainers.
        """
        if isinstance(texts, str):
            texts = [texts]
        all_probs = []
        for text in texts:
            inputs = self.prepare_inputs(text)
            with torch.no_grad():
                outputs = self.model(**inputs)
                probs = torch.sigmoid(outputs.logits)
                avg_probs = probs[0].mean(dim=0).cpu().numpy()
                all_probs.append(avg_probs)
        return np.array(all_probs)
