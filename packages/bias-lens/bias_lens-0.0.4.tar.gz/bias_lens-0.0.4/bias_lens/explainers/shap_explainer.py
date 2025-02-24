import matplotlib.pyplot as plt
import shap

from .probability_explainer_mixin import ProbabilityExplainerMixin


class ShapExplainer(ProbabilityExplainerMixin):
    def __init__(self, model, tokenizer, id2label, max_length=128):
        super().__init__(model, tokenizer, max_length)
        self.id2label = id2label

    def explain(self, text):
        """
        Generates a SHAP explanation for the input text.
        """
        try:
            masker = shap.maskers.Text(r"\s+")
            explainer = shap.Explainer(
                self.predict_proba, masker, output_names=list(self.id2label.values())
            )
            shap_values = explainer([text])
            plt.figure(figsize=(12, 8))
            shap.plots.text(shap_values, display=False)
            plt.tight_layout()

            shap_explanation = {
                "values": shap_values.values,
                "base_values": shap_values.base_values,
                "data": shap_values.data,
                "feature_names": text.split(),
            }
            return shap_explanation
        except Exception as e:
            print(f"Error in SHAP explanation: {str(e)}")
            raise
