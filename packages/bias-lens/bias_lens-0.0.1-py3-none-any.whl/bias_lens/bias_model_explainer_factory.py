from .explainers import (
    AttentionExplainer,
    CounterfactualExplainer,
    DeepLiftExplainer,
    IntegratedGradientsExplainer,
    LimeExplainer,
    LRPExplainer,
    OcclusionExplainer,
    ShapExplainer,
)


class BiasModelExplainerFactory:
    def __init__(self, model, tokenizer, id2label, max_length=128):
        """
        Factory to generate different explainer instances.
        """
        self.explainers = {
            "lime": LimeExplainer(model, tokenizer, id2label, max_length),
            "shap": ShapExplainer(model, tokenizer, id2label, max_length),
            "integrated_gradients": IntegratedGradientsExplainer(
                model, tokenizer, max_length
            ),
            "deeplift": DeepLiftExplainer(model, tokenizer, max_length),
            "attention": AttentionExplainer(model, tokenizer, max_length),
            "counterfactual": CounterfactualExplainer(model, tokenizer, max_length),
            "lrp": LRPExplainer(model, tokenizer, max_length),
            "occlusion": OcclusionExplainer(model, tokenizer, max_length),
        }

    def get_explainer(self, method):
        """
        Returns the explainer instance for the given method.
        """
        return self.explainers.get(method)
