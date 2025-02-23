import torch


class BiasNERClassifier:
    def __init__(self, model, tokenizer, id2label, max_length=128):
        """
        Initializes the bias NER classifier.

        Args:
            model: A token classification model.
            tokenizer: The tokenizer corresponding to the model.
            id2label (dict): Mapping from label indices to string labels.
            max_length (int): Maximum token sequence length.
        """
        self.model = model
        self.tokenizer = tokenizer
        self.id2label = id2label
        self.max_length = max_length
        self.device = next(model.parameters()).device

    def predict(self, sentence):
        """
        Predicts bias NER tags for a given sentence.
        Returns a list of dictionaries with tokens and their associated labels.
        """
        inputs = self.tokenizer(
            sentence,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=self.max_length,
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probabilities = torch.sigmoid(logits)
            predicted_labels = (probabilities > 0.5).int()

        tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
        result = []
        for i, token in enumerate(tokens):
            if token not in self.tokenizer.all_special_tokens:
                label_indices = (
                    (predicted_labels[0][i] == 1).nonzero(as_tuple=False).squeeze(-1)
                )
                labels = (
                    [self.id2label[idx.item()] for idx in label_indices]
                    if label_indices.numel() > 0
                    else ["O"]
                )
                result.append({"token": token, "labels": labels})
        return result
