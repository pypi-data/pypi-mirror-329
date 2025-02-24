from lime.lime_text import LimeTextExplainer

from .probability_explainer_mixin import ProbabilityExplainerMixin


class LimeExplainer(ProbabilityExplainerMixin):
    def __init__(self, model, tokenizer, id2label, max_length=128):
        super().__init__(model, tokenizer, max_length)
        self.id2label = id2label

    def explain(self, text, num_features=10, num_samples=100):
        """
        Generates a LIME explanation for the input text.
        """
        try:
            explainer = LimeTextExplainer(
                class_names=list(self.id2label.values()), split_expression=" "
            )
            exp = explainer.explain_instance(
                text,
                self.predict_proba,
                num_features=num_features,
                num_samples=num_samples,
                top_labels=len(self.id2label),
            )
            explanations = {
                self.id2label[label_id]: exp.as_list(label=label_id)
                for label_id in self.id2label
                if exp.as_list(label=label_id)
            }
            return explanations
        except Exception as e:
            print(f"Error in LIME explanation: {str(e)}")
            raise
