from captum.attr import Occlusion

from .base_explainer import BaseExplainer


class OcclusionExplainer(BaseExplainer):
    def explain(self, text, sliding_window=1):
        """
        Generates an explanation by occluding one token at a time.
        """
        inputs = self.prepare_inputs(text)
        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]

        def forward_func(input_ids, attention_mask):
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            aggregated_logits = outputs.logits.mean(dim=1)
            return aggregated_logits[:, 0]

        occlusion = Occlusion(forward_func)
        attributions = occlusion.attribute(
            input_ids,
            additional_forward_args=(attention_mask,),
            sliding_window_shapes=(1,),
        )
        tokens = self.tokenizer.convert_ids_to_tokens(input_ids[0])
        attributions = attributions[0].detach().cpu().numpy()
        return tokens, attributions
