import utils
import numpy as np
from PIL import Image
import torch
from torchvision import transforms

def stegano_solver(img) -> str:
    image = Image.fromarray(img)

    # Define the transformation to convert the image to a tensor
    transform = transforms.Compose([
        transforms.ToTensor(),
    ])

    # Apply the transformation
    tensor_image = transform(image)
    tensor_image = tensor_image.unsqueeze(0)

    decoded_message = utils.decode(tensor_image)
    return decoded_message