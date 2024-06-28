document.getElementById('inputText').addEventListener('input', function() {
    const inputText = this.value;

    if (inputText.trim().length === 0) {
        // Clear suggestions if input is empty
        document.getElementById('suggestions').innerHTML = '';
        return;
    }

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input_text: inputText })
    })
    .then(response => response.json())
    .then(data => {
        const suggestionsDiv = document.getElementById('suggestions');
        suggestionsDiv.innerHTML = '';

        data.forEach(word => {
            const suggestionElement = document.createElement('div');
            suggestionElement.className = 'suggestion';
            suggestionElement.textContent = word;

            // Add click event to insert the suggestion into the input
            suggestionElement.addEventListener('click', () => {
                document.getElementById('inputText').value += ' ' + word;
                suggestionsDiv.innerHTML = ''; // Clear suggestions after selecting one
            });

            suggestionsDiv.appendChild(suggestionElement);
        });
    })
    .catch(error => console.error('Error:', error));
});
