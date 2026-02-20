let http = new XMLHttpRequest();
let allBooks = []; // Global variable to store all books

document.addEventListener('DOMContentLoaded', () => {
    const userInfo = JSON.parse(localStorage.getItem('loggedInUser '));

    console.log(userInfo);

    if (userInfo) {
        const welcomeMessage = document.getElementById('welcome-message');
        welcomeMessage.textContent = `${userInfo.username}`; 
    } else {
        console.log('No user is logged in.'); 
    }

    fetchBooks(); 
    const userProfileData = JSON.parse(localStorage.getItem(`userProfileData_${userInfo.userId}`));
            const imageElement = document.getElementById("imagee");
           

           
            if (userProfileData && userProfileData.imageUrl) {
                imageElement.src = userProfileData.imageUrl; 
            } else {
                // Use a simple default avatar - could be based on gender
                imageElement.src = 'https://ui-avatars.com/api/?name=' + encodeURIComponent(userInfo.username || 'User') + '&background=0D8ABC&color=fff';
            }
});

function fetchBooks() {
    // Fetch books from Flask API
    fetch('/api/books')
        .then(response => response.json())
        .then(data => {
            allBooks = data.books; // Store globally
            // Store in localStorage for offline access
            localStorage.setItem('books', JSON.stringify(allBooks));
            displayBooks(allBooks);
            setupSearch(); // Setup search after books are loaded
        })
        .catch(error => {
            console.error('Error fetching books:', error);
            // Fallback to localStorage if API fails
            allBooks = JSON.parse(localStorage.getItem('books')) || [];
            displayBooks(allBooks);
            setupSearch(); // Setup search after books are loaded
        });
}


function displayBooks(books) {
    let output = ""; 
    for (let i = 0; i < books.length; i++) {
        const item = books[i];
        output += `
        <a href="/book/${item.id}" class="boook" data-id="${item.id}">
            <div class="boooks">
                <img src="${item.image}" alt="${item.title}">
            </div>
        </a>`;
    }
    document.querySelector(".boooks").innerHTML = output;
}

function setupSearch() {
    // Search functionality
    const searchInput = document.querySelector('.search');
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        
        if (searchTerm === '') {
            // If search is empty, show all books
            displayBooks(allBooks);
        } else {
            // Filter books based on search term
            const filteredBooks = allBooks.filter(book => 
                book.title.toLowerCase().includes(searchTerm) ||
                book.author.toLowerCase().includes(searchTerm)
            );
            displayBooks(filteredBooks);
        }
    });
}