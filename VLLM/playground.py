
import torch
from diffusers import Lumina2Text2ImgPipeline

pipe = Lumina2Text2ImgPipeline.from_pretrained("Alpha-VLLM/Lumina-Image-2.0", torch_dtype=torch.bfloat16)
pipe.enable_model_cpu_offload() #save some VRAM by offloading the model to CPU. Remove this if you have enough GPU power

prompt = "A serene photograph capturing the golden reflection of the sun on a vast expanse of water. The sun is positioned at the top center, casting a brilliant, shimmering trail of light across the rippling surface. The water is textured with gentle waves, creating a rhythmic pattern that leads the eye towards the horizon. The entire scene is bathed in warm, golden hues, enhancing the tranquil and meditative atmosphere. High contrast, natural lighting, golden hour, photorealistic, expansive composition, reflective surface, peaceful, visually harmonious."
image = pipe(
    prompt,
    height=1024,
    width=1024,
    guidance_scale=4.0,
    num_inference_steps=50,
    cfg_trunc_ratio=0.25,
    cfg_normalization=True,
    generator=torch.Generator("cpu").manual_seed(0)
).images[0]
image.save("lumina_demo.png")


###################################


from vllm import LLM, SamplingParams

llm = LLM(model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
params = SamplingParams(temperature=0.7, max_tokens=100)
outputs = llm.generate(["Why is the sky blue?", "Explain entropy"], params)
for out in outputs:
    print(out.outputs[0].text)


