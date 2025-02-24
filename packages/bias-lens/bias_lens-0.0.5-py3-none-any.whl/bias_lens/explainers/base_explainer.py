class BaseExplainer:
    def __init__(self, model, tokenizer, max_length=128):
        """
        Base class for all explainers.
        """
        self.model = model
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.device = next(model.parameters()).device

    def prepare_inputs(self, text, padding="max_length", truncation=True):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=padding,
            truncation=truncation,
            max_length=self.max_length,
        )
        return {k: v.to(self.device) for k, v in inputs.items()}
