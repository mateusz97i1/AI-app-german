// static/js/dictionary_searchbar.js

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const autocompleteList = document.getElementById('autocompleteList');
    const searchForm = searchInput.closest('form'); // Get the parent form

    // Function to perform the search (submit the form) and hide the list
    function performSearch(query) {
        console.log("DEBUG: performSearch called with query:", query); // For debugging
        searchInput.value = query; // Set the input value to the selected word
        searchForm.submit();       // Submit the form immediately
        autocompleteList.classList.add('hidden'); // Hide the autocomplete list
    }

    // Event listener for input changes in the search bar
    searchInput.addEventListener('input', function() {
        const query = this.value.trim();

        if (query.length > 0) {
            // Make an AJAX request to your Django view for autocomplete suggestions
            // Ensure this URL '/word_generator/autocomplete/' is correct for your project
            fetch(`/word_generator/autocomplete/?q=${query}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    autocompleteList.innerHTML = ''; // Clear previous suggestions
                    if (data.words && data.words.length > 0) { // Ensure data.words exists and is not empty
                        data.words.forEach(word => {
                            const listItem = document.createElement('li');
                            listItem.classList.add('p-2', 'cursor-pointer', 'hover:bg-gray-100');
                            listItem.textContent = word;
                            // When a list item is clicked, perform the search using that word
                            listItem.addEventListener('click', function() {
                                console.log("DEBUG: ListItem clicked for word:", word); // For debugging
                                performSearch(word);
                            });
                            autocompleteList.appendChild(listItem);
                        });
                        autocompleteList.classList.remove('hidden'); // Show the list if there are suggestions
                    } else {
                        autocompleteList.classList.add('hidden'); // Hide if no suggestions or empty array
                    }
                })
                .catch(error => console.error('Error fetching autocomplete suggestions:', error));
        } else {
            autocompleteList.classList.add('hidden'); // Hide the list if input is empty
            autocompleteList.innerHTML = ''; // Clear suggestions
        }
    });

    // Hide autocomplete list when clicking outside the search input or the list itself
    document.addEventListener('click', function(event) {
        if (!autocompleteList.contains(event.target) && !searchInput.contains(event.target)) {
            autocompleteList.classList.add('hidden');
        }
    });

    // Handle Enter key press
    searchInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            // If the autocomplete list is visible and has suggestions, prevent default submission.
            // This forces the user to click a suggestion if they want to use autocomplete.
            if (!autocompleteList.classList.contains('hidden') && autocompleteList.children.length > 0) {
                event.preventDefault();
                console.log("DEBUG: Enter key pressed with autocomplete list visible. Preventing default."); // For debugging
            } else {
                // If the list is hidden (no suggestions or input cleared), allow Enter to submit
                // the form with whatever is currently in the search input.
                searchForm.submit();
                console.log("DEBUG: Enter key pressed with autocomplete list hidden. Submitting form."); // For debugging
            }
        }
    });
});