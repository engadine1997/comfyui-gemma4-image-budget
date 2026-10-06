# comfyui-gemma4-image-budget

## What is this?

This is self-contained custom node containing a new node `Gemma 4 Image Budget`. It is a simple node that improves the visual image processing capability of the Gemma 4 family.

It supports selecting image token budgets of `70`, `140`, `280`, `560`, or `1120`.

## Well, why do I need it?

By default when using Gemma 4 to generate text with image input, you might have noticed the model (independent of size) seems pretty blind. When ComfyUI compresses an image down into image patches, it enforces a token budget of `280`. This is despite the Gemma 4 family supporting `70`, `140`, `280`, `560`, or `1120` tokens.

The effect of this that images are shrunk down to ~800x800 total pixels; at that resolution any text in input images becomes unreadable if it's small enough. At the maximum `1120` this becomes ~1600x1600, allowing models to see the image more clearly.

## Usage

Drop the node after your clip loader node and between your generate text node.

## Installation

Clone the repo into your comfyui `custom_nodes` folder. *fin*. The `__init__.py` script loads the requisite fix.
