from diffusers import StableDiffusionPipeline
import torch
import uuid

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32
)

pipe = pipe.to("cpu")

def generate_background(prompt):
    image = pipe(prompt).images[0]
    filename = f"assets/{uuid.uuid4()}.jpg"
    image.save(filename)
    return filename