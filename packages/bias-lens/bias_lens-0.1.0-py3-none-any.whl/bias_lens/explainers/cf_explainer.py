import torch

from .base_explainer import BaseExplainer


class CounterfactualExplainer(BaseExplainer):
    def explain(self, text, target_class=None):
        """
        Generates a counterfactual explanation by iteratively replacing tokens.
        Note: This method can be time- and memory-intensive.
        """
        original_inputs = self.prepare_inputs(text)
        original_input_ids = original_inputs["input_ids"]
        attention_mask = original_inputs["attention_mask"]

        with torch.no_grad():
            original_outputs = self.model(**original_inputs)
            aggregated_logits = original_outputs.logits.mean(dim=1)
        if target_class is None:
            target_class = torch.argmax(aggregated_logits, dim=-1)[0].item()

        counterfactual_text = text
        counterfactual_input_ids = original_input_ids.clone()

        # Iterate over token positions (skipping special tokens)
        for token_pos in range(1, original_input_ids.size(1) - 1):
            original_token_id = counterfactual_input_ids[0, token_pos].item()
            original_token = self.tokenizer.convert_ids_to_tokens([original_token_id])[
                0
            ]

            min_prob = float("inf")
            best_token_id = original_token_id

            for candidate_token_id in range(self.tokenizer.vocab_size):
                counterfactual_input_ids[0, token_pos] = candidate_token_id
                with torch.no_grad():
                    counterfactual_outputs = self.model(
                        input_ids=counterfactual_input_ids,
                        attention_mask=attention_mask,
                    )
                    aggregated_logits = counterfactual_outputs.logits.mean(dim=1)
                    counterfactual_probs = (
                        torch.softmax(aggregated_logits, dim=-1).cpu().numpy()
                    )
                prob = counterfactual_probs[0][target_class]
                if prob < min_prob:
                    min_prob = prob
                    best_token_id = candidate_token_id

            counterfactual_input_ids[0, token_pos] = best_token_id
            best_token = self.tokenizer.convert_ids_to_tokens([best_token_id])[0]
            counterfactual_text = counterfactual_text.replace(
                original_token, best_token, 1
            )

        return counterfactual_text
