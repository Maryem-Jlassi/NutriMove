# utils.py
from transformers import AutoProcessor, AutoModelForImageClassification
import torch
from transformers import pipeline
from transformers import ViTForImageClassification, ViTImageProcessor
from PIL import Image
from gtts import gTTS
import os
from django.conf import settings


# Food classification function
#food_classification_pipeline = pipeline("image-classification", model="nateraw/vit-base-beans",  framework="pt")
#processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224")  # General ViT
#model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224")
'''processor = AutoProcessor.from_pretrained("htls003/food-101-vit")
model = AutoModelForImageClassification.from_pretrained("htls003/food-101-vit")'''
processor = AutoProcessor.from_pretrained("nateraw/food")
model = AutoModelForImageClassification.from_pretrained("nateraw/food")
calorie_map = {
    # Fruits
    "apple": 52,               # per 100g
    "banana": 96,              # per 100g
    "orange": 47,              # per 100g
    "grapes": 69,              # per 100g
    "strawberry": 32,          # per 100g
    "watermelon": 30,          # per 100g
    "mango": 60,               # per 100g
    # Vegetables
    "carrot": 41,              # per 100g
    "broccoli": 55,            # per 100g
    "spinach": 23,             # per 100g
    "potato": 77,              # per 100g
    "cucumber": 16,            # per 100g
    "tomato": 18,              # per 100g

    # Grains & Cereal
    "rice": 130,               # per 100g (cooked)
    "bread": 265,              # per 100g
    "oats": 68,                # per 100g

    # Dairy
    "milk": 42,                # per 100g
    "cheese": 402,             # per 100g
    "yogurt": 59,              # per 100g

    # Meat
    "chicken_breast": 165,     # per 100g (cooked)
    "beef": 250,               # per 100g (cooked)
    "salmon": 208,             # per 100g (cooked)

    # Fast Food & Snacks
    "burger": 295,             # per 100g
    "pizza": 266,              # per 100g
    "french_fries": 312,       # per 100g
    "chocolate": 546,          # per 100g
    "chips": 536,              # per 100g

    # Beverages
    "soda": 39,                # per 100g
    "coffee": 1,               # per 100g (without sugar/milk)
    "juice": 45,               # per 100g

    # Nuts & Seeds
    "almonds": 579,            # per 100g
    "peanuts": 567,            # per 100g
    "sunflower_seeds": 584,    # per 100g

    # Legumes
    "lentils": 116,            # per 100g (cooked)
    "chickpeas": 164,          # per 100g (cooked)
    "beans": 127,              # per 100g (cooked)

    # Sweets
    "ice_cream": 207,          # per 100g
    "cake": 350,               # per 100g
    "cookies": 502,            # per 100g
}


def classify_food(image_path):
    # Load the image
    image = Image.open(image_path)
    image = image.convert('RGB')
    
        

    # Preprocess the image using the processor
    inputs = processor(images=image, return_tensors="pt")

    # Get the model predictions
    outputs = model(**inputs)
    logits = outputs.logits

    # Get the predicted class
    predicted_class = logits.argmax(-1).item()
    food_labels = model.config.id2label  # This assumes your model has a config with id2label
    predicted_food = food_labels[predicted_class]

    # Map the predicted food to its calories
    calories = calorie_map.get(predicted_food.lower(), "Unknown")

    # Return the class label or any desired info
    return predicted_food,calories

text_generation_pipeline = pipeline("text-generation", model="gpt2")

# Generate a fitness tip based on detected food
def generate_fitness_tip(detected_food):
    # Create the prompt for the fitness tip generation
    prompt = f"Suggest a fitness tip based on the consumption of {detected_food}."
    
    try:
        # Générer le texte avec une longueur et une troncature appropriées
        result = text_generation_pipeline(prompt, max_length=450, truncation=True, num_return_sequences=1)
        fitness_tip = result[0]["generated_text"].strip()

        # Truncation supplémentaire si nécessaire
        if len(fitness_tip) > 450:  # Limite de 300 caractères pour un conseil clair
            fitness_tip = fitness_tip[:450].rsplit(' ', 1)[0] + "..."

        return fitness_tip

    except Exception as e:
        print(f"Erreur lors de la génération du conseil fitness : {e}")
        return "Unable to generate a fitness tip at the moment. Please try again."
def convert_to_audio(text, filename="fitness_tip.mp3"):
    try:
        # Chemin complet vers MEDIA_ROOT ou STATIC_ROOT
        audio_dir = os.path.join(settings.BASE_DIR, 'media')
        os.makedirs(audio_dir, exist_ok=True)  # Créez le répertoire s'il n'existe pas

        audio_path = os.path.join(audio_dir, filename)

        # Conversion du texte en audio
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(audio_path)

        # Retourne le chemin relatif pour l'usage dans les templates
        return  filename

    except Exception as e:
        print(f"Erreur lors de la conversion en audio : {e}")
        return None