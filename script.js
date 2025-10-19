const form = document.getElementById('contactForm');
const popup = document.getElementById('popup');
const overlay = document.getElementById('overlay');

form.addEventListener('submit', function(e) {
    e.preventDefault();
    // Show popup and overlay
    popup.classList.add('show');
    overlay.classList.add('show');
    // Reset form
    form.reset();
});

function closePopup() {
    popup.classList.remove('show');
    overlay.classList.remove('show');
}

// Close popup when clicking overlay
overlay.addEventListener('click', closePopup);