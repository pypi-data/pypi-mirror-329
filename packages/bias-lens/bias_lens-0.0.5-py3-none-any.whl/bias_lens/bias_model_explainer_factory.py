from enum import Enum

from .explainers import (
    AttentionExplainer,
    CounterfactualExplainer,
    DeepLiftExplainer,
    IntegratedGapGradientsExplainer,
    IntegratedGradientsExplainer,
    LimeExplainer,
    LRPExplainer,
    OcclusionExplainer,
    SaliencyExplainer,
    ShapExplainer,
)


class ExplainerMethod(Enum):
    LIME = "lime"
    SHAP = "shap"
    INTEGRATED_GRADIENTS = "integrated_gradients"
    INTEGRATED_GAP_GRADIENTS = "integrated_gap_gradients"
    DEEPLIFT = "deeplift"
    ATTENTION = "attention"
    COUNTERFACTUAL = "counterfactual"
    LRP = "lrp"
    OCCLUSION = "occlusion"
    SALIENCY = "saliency"


class BiasModelExplainerFactory:
    def __init__(self, model, tokenizer, id2label, max_length=128):
        """
        Factory to generate different explainer instances.
        """
        self.explainers = {
            ExplainerMethod.LIME: LimeExplainer(model, tokenizer, id2label, max_length),
            ExplainerMethod.SHAP: ShapExplainer(model, tokenizer, id2label, max_length),
            ExplainerMethod.INTEGRATED_GRADIENTS: IntegratedGradientsExplainer(
                model, tokenizer, max_length
            ),
            ExplainerMethod.DEEPLIFT: DeepLiftExplainer(model, tokenizer, max_length),
            ExplainerMethod.ATTENTION: AttentionExplainer(model, tokenizer, max_length),
            ExplainerMethod.COUNTERFACTUAL: CounterfactualExplainer(
                model, tokenizer, max_length
            ),
            ExplainerMethod.LRP: LRPExplainer(model, tokenizer, max_length),
            ExplainerMethod.OCCLUSION: OcclusionExplainer(model, tokenizer, max_length),
            ExplainerMethod.SALIENCY: SaliencyExplainer(model, tokenizer, max_length),
            ExplainerMethod.INTEGRATED_GAP_GRADIENTS: IntegratedGapGradientsExplainer(
                model, tokenizer, max_length
            ),
        }

    def get_explainer(self, method):
        """
        Returns the explainer instance for the given method.
        """
        return self.explainers.get(method)
