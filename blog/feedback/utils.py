# utils.py

from transformers import pipeline
from transformers import ViTForImageClassification, ViTImageProcessor
from PIL import Image
from gtts import gTTS
import os
from django.conf import settings


# Food classification function
#food_classification_pipeline = pipeline("image-classification", model="nateraw/vit-base-beans",  framework="pt")
processor = ViTImageProcessor.from_pretrained("nateraw/vit-base-beans")
model = ViTForImageClassification.from_pretrained("nateraw/vit-base-beans")

def classify_food(image_path):
    # Load the image
    image = Image.open(image_path)
    image = image.convert('RGB')
    image = image.resize((224, 224))
        

    # Preprocess the image using the processor
    inputs = processor(images=image, return_tensors="pt")

    # Get the model predictions
    outputs = model(**inputs)
    logits = outputs.logits

    # Get the predicted class
    predicted_class = logits.argmax(-1).numpy().item()

    # Return the class label or any desired info
    return predicted_class

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
def convert_to_audio(text, filename="media/fitness_tip.mp3"):
    try:
        # Chemin complet vers MEDIA_ROOT ou STATIC_ROOT
        audio_dir = os.path.join(settings.BASE_DIR, '/media/')
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
