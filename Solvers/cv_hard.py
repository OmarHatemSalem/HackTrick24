from PIL import Image
from transformers import pipeline

vqa_pipeline = pipeline("visual-question-answering")

image =  Image.open("../Riddles/cv_hard_example/cv_hard_sample_image.jpg")
print(type(image))
question = "How many are there?"

ans = vqa_pipeline(image, question, top_k=1)
print('---------')
print(type(int(ans[0]['answer'])))