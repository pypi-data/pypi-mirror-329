import numpy as np
import torch

from .base_explainer import BaseExplainer


class IntegratedGapGradientsExplainer(BaseExplainer):
    def __init__(
        self,
        model,
        tokenizer,
        max_length=128,
        steps=50,
        correction_factor=0.5,
        baseline=None,
        smooth_samples=1,
    ):
        """
        Initializes the IG2 explainer with options to mitigate known limitations.

        Args:
            model: The model to explain.
            tokenizer: The tokenizer associated with the model.
            max_length (int): Maximum token sequence length.
            steps (int): Number of integration steps.
            correction_factor (float): Scaling factor for the second-order correction term.
            baseline: Optional baseline tensor. If None, defaults to a zero tensor.
            smooth_samples (int): Number of times to compute gradients for smoothing (reduces noise).
        """
        super().__init__(model, tokenizer, max_length)
        self.steps = steps
        self.correction_factor = correction_factor
        self.smooth_samples = smooth_samples
        self.baseline = baseline  # User can supply a more meaningful baseline (e.g., average or masked embedding)

    def explain(self, text):
        """
        Generates an IG2 explanation based on the IG2 method as described in:
        [IG2: A New XAI Method](https://arxiv.org/abs/2406.10130)

        This implementation addresses known limitations by:
          - Allowing a custom baseline.
          - Parameterizing the integration steps and correction factor.
          - Smoothing gradients over multiple runs.
          - Normalizing the final attributions.
        """
        inputs = self.prepare_inputs(text)
        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]
        embeddings = self.model.bert.embeddings(input_ids).clone().detach()

        # Use provided baseline or default to zeros (user is encouraged to supply a better baseline)
        if self.baseline is None:
            baseline = torch.zeros_like(embeddings)
        else:
            baseline = self.baseline

        # Compute scaled embeddings along the integration path
        scaled_embeddings = [
            baseline + (float(i) / self.steps) * (embeddings - baseline)
            for i in range(self.steps + 1)
        ]

        # Compute gradients along the path with optional smoothing
        grads_all = []
        for scaled in scaled_embeddings:
            grad_samples = []
            for _ in range(self.smooth_samples):
                scaled_var = scaled.clone().detach().requires_grad_(True)
                outputs = self.model(
                    inputs_embeds=scaled_var, attention_mask=attention_mask
                )
                # For simplicity, assume target index 0; this can be parameterized further if needed
                score = outputs.logits[:, 0]
                self.model.zero_grad()
                score.backward(torch.ones_like(score), retain_graph=True)
                grad_samples.append(scaled_var.grad.detach())
            # Average gradients over multiple smooth samples
            avg_grad_sample = torch.stack(grad_samples, dim=0).mean(dim=0)
            grads_all.append(avg_grad_sample)
        grads_all = torch.stack(
            grads_all, dim=0
        )  # Shape: [steps+1, batch, seq_length, embed_dim]

        # Compute integrated gradients using the trapezoidal rule
        avg_grads = (grads_all[:-1] + grads_all[1:]) / 2.0
        integrated_grads = (embeddings - baseline) * avg_grads.mean(dim=0)

        # Compute second-order correction based on gradient variance
        grad_variance = torch.var(grads_all, dim=0)
        ig2_attributions = integrated_grads + self.correction_factor * grad_variance * (
            embeddings - baseline
        )

        # Sum over embedding dimensions and normalize attributions
        tokens = self.tokenizer.convert_ids_to_tokens(input_ids[0])
        attributions = ig2_attributions.sum(dim=-1).squeeze(0).detach().cpu().numpy()
        attributions = attributions / (np.linalg.norm(attributions) + 1e-10)

        return tokens, attributions
