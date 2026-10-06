"""Sets the Gemma 4 image token budget used by Generate Text (ComfyUI's default is 280).

Put the "Gemma 4 Image Budget" node between the CLIP loader and Generate Text. Higher budgets keep more
of large images (1120 allows roughly 1600x1600 pixels, 280 roughly 800x800) at the cost of a longer prompt.
"""
import copy

from comfy_api.latest import ComfyExtension, io
from typing_extensions import override

from comfy.text_encoders.gemma4 import Gemma4Tokenizer

BUDGETS = ["70", "140", "280", "560", "1120"]


class Gemma4ImageBudget(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="Gemma4ImageBudget",
            display_name="Gemma 4 Image Budget",
            category="advanced/model_patches",
            description="Sets how many tokens Gemma 4 spends on each input image. Images larger than the budget allows are downscaled.",
            inputs=[
                io.Clip.Input("clip"),
                io.Combo.Input("max_image_tokens", options=BUDGETS, default="1120", tooltip="Image token budget per image. ComfyUI's default is 280; 1120 is the maximum. Video frames are not affected."),
            ],
            outputs=[io.Clip.Output()],
        )

    @classmethod
    def execute(cls, clip, max_image_tokens) -> io.NodeOutput:
        if not isinstance(clip.tokenizer, Gemma4Tokenizer):
            raise ValueError("Gemma 4 Image Budget needs a Gemma 4 text encoder")
        clip = clip.clone()
        clip.tokenizer = copy.copy(clip.tokenizer)
        tokenize = clip.tokenizer.tokenize_with_weights
        budget = int(max_image_tokens)

        def tokenize_with_weights(text, return_word_ids=False, **kwargs):
            if kwargs.get("video") is None:
                kwargs["max_soft_tokens"] = budget
            return tokenize(text, return_word_ids, **kwargs)

        clip.tokenizer.tokenize_with_weights = tokenize_with_weights
        return io.NodeOutput(clip)


class Gemma4ImageBudgetExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [Gemma4ImageBudget]


async def comfy_entrypoint() -> Gemma4ImageBudgetExtension:
    return Gemma4ImageBudgetExtension()
