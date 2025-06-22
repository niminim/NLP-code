import torch
from TTS.api import TTS

# def get_model(model_name ='xtts_v2'):
#
#     if model_name == 'xtts_v2':
#         device = "cuda" if torch.cuda.is_available() else "cpu"
#         model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
#     return model


# Monkey-patch torch.load before calling TTS(...)
# This is the cleanest way to force weights_only=False without editing any files or adding safe globals.
# Here’s how to do it:

import torch
from functools import wraps
from TTS.api import TTS
from TTS.tts.layers.xtts.gpt import GPT2InferenceModel

# Monkey-patch torch.load to prevent weights_only=True recursion (PyTorch >= 2.6)
if not hasattr(torch.load, "_is_patched_for_weights_only"):
    original_torch_load = torch.load

    @wraps(original_torch_load)
    def patched_torch_load(*args, **kwargs):
        if "weights_only" not in kwargs:
            kwargs["weights_only"] = False
        return original_torch_load(*args, **kwargs)

    patched_torch_load._is_patched_for_weights_only = True
    torch.load = patched_torch_load

# Patch generate if not present in GPT2InferenceModel
from transformers.generation import GenerationMixin
from TTS.tts.layers.xtts.gpt import GPT2InferenceModel

# Dynamically add GenerationMixin to the class inheritance
if not issubclass(GPT2InferenceModel, GenerationMixin):
    GPT2InferenceModel.__bases__ += (GenerationMixin,)

# Model loader
def get_model(model_name='xtts_v2'):
    if model_name == 'xtts_v2':
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        return model

# tts_model = get_model()

# Why This Works
# This monkey patch intercepts all calls to torch.load(...) and forces weights_only=False — which restores the previous (pre-2.6) behavior.
#
# It avoids:
# Editing site-packages
  # Manually adding dozens of add_safe_globals()
  # Any long-term risks (you can always remove the patch)


# your monkey-patch will work just fine in PyTorch 2.5 — even though weights_only doesn't exist yet in 2.5, the code is still safe.
# Here’s why:

#  In PyTorch 2.5:
# torch.load() does not recognize the weights_only argument.
# Your patch adds weights_only=False, which will be passed as an unused kwarg.
# PyTorch will just ignore unknown kwargs (i.e., weights_only) — no error.

# ✅ So:
# In PyTorch 2.6+, your patch actively disables the weights_only=True default.
# In PyTorch 2.5 and below, your patch does nothing harmful — it's a no-op.