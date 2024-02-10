from fastapi import FastAPI, File, UploadFile
import os
from google.cloud import vision
import io
import requests


app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.post("/image/")
async def img(file: UploadFile):
    # file save
    with open(file.filename, "wb") as f:
        f.write(await file.read())

    detected_labels = detect_labels(file.filename)

    print('Ingredients detected in the image:')
    print(detected_labels)

    #Search for recipes based on the detected ingredients
    recipes = search_recipes(detected_labels)

    print('Recipes that can be made with the detected ingredients:')
    for recipe in recipes:
        print(recipe['title'])
        print(recipe['image'])
        print()

    
    return recipes



# Set the environment variable to the path of your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/tylertoo/downloads/chromatic-tree-413900-8ccd53eae0c8.json"

# Initialize a client
client = vision.ImageAnnotatorClient()

def detect_labels(image_path):
    # Load the image file
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Create an image object
    image = vision.Image(content=content)

    # Perform label detection on the image
    response = client.label_detection(image=image)
    labels = response.label_annotations

    # Return detected labels
    return [label.description.lower() for label in labels]


def search_recipes(ingredients):
    # Join the ingredients into a comma-separated string
    ingredients_str = ','.join(ingredients)
    
    # Make a request to the Spoonacular API to search for recipes
    api_key = '5e99f1a1094d46d5bd93ac977437f62f'
    url = f'https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients={ingredients_str}&number=5'
    response = requests.get(url)
    recipes = response.json()
    
    # Extract relevant information and include recipe URLs
    formatted_recipes = []
    for recipe in recipes:
        formatted_recipe = {
            'title': recipe['title'],
            'image': recipe['image'],
            'url': f"https://spoonacular.com/recipes/{recipe['title']}-{recipe['id']}"
        }
        formatted_recipes.append(formatted_recipe)
    
    return formatted_recipes


