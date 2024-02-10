import os
from google.cloud import vision
import io
import requests
from flask import Flask, request

# Set the environment variable to the path of your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/tylertoo/downloads/chromatic-tree-413900-8ccd53eae0c8.json"

# Initialize a client
client = vision.ImageAnnotatorClient()

app = Flask(__name__)

def detect_labels(image_content):
    # Create an image object
    image = vision.Image(content=image_content)

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
    url = f'https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients={ingredients_str}'
    response = requests.get(url)
    recipes = response.json()
    
    # Return the list of recipes
    return recipes

@app.route('/detect-labels', methods=['POST'])
def detect_labels_from_image():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file:
        # Read the image file content
        image_content = file.read()

        # Detect labels from the image content
        detected_labels = detect_labels(image_content)

        # Search for recipes based on the detected ingredients
        recipes = search_recipes(detected_labels)

        # Return the list of recipes as a response
        return {'recipes': recipes}

if __name__ == '__main__':
    app.run(debug=True)












document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the default form submission
    var formData = new FormData();
    var imageFile = document.getElementById('image-input').files[0];
    formData.append('file', imageFile);

    // Update the URL to where your Flask app is hosted (localhost for development)
    fetch('/predict', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        document.getElementById('prediction-result').innerText = 
            'Prediction: ' + data.prediction + ', Probability: ' + data.probability;
    })
    .catch(error => console.error('Error:', error));
});
