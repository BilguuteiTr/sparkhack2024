function fetchData() {
    fetch("http://127.0.0.1:8000")
    .then(response => response.json())
    .then(data => {
        // Process the response data here
        console.log(data);
    })
    .catch(error => console.error('Error:', error));
}

function uploadFile() {
    var fileinput = document.getElementById('fileInput')
    var file = fileinput.files[0]

    var formData = new FormData();
    formData.append('file', file);

    fetch("http://127.0.0.1:8000/image/", {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        // Process the response data here
        console.log(data);

        // Display recipes
        displayRecipes(data);
    })
    .catch(error => console.error('Error:', error));
}

function displayRecipes(recipes) {
    var recipesContainer = document.getElementById('recipesContainer');
    recipesContainer.innerHTML = ''; // Clear previous content

    recipes.forEach(recipe => {
        var recipeElement = document.createElement('div');
        recipeElement.classList.add('recipe');
        recipeElement.innerHTML = `
            <h2><a href="${recipe.url}" target="_blank">${recipe.title}</a></h2>
            <img src="${recipe.image}" alt="${recipe.title}">
        `;
        recipesContainer.appendChild(recipeElement);
    });
}
