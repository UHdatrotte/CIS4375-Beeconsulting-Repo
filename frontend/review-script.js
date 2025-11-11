// A global function for the popup's onclick
function closePopup() {
    // Adding 'show' to the class makes it compatible with CSS transitions
    document.getElementById('popup').classList.remove('show');
    document.getElementById('overlay').classList.remove('show');
}

document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('reviewForm');
    if (!reviewForm) return; // Exit if the form isn't on this page

    const popup = document.getElementById('popup');
    const overlay = document.getElementById('overlay');
    const closePopupBtn = document.querySelector('.popup-btn'); // Use a more specific selector
    
    if(closePopupBtn) {
        closePopupBtn.addEventListener('click', closePopup);
    }
    if(overlay) {
        overlay.addEventListener('click', closePopup);
    }

    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(reviewForm);

        // This transforms the simple form names into the keys the database needs.
        const data = {
            type: 'review',
            FNAME: formData.get('name'), // from <input name="name">
            LNAME: formData.get('lastname'), // from <input name="lastname">
            COMPANY_NAME: formData.get('company'),
            EMAIL: formData.get('email'),
            REVIEW: formData.get('message'),
            RATING: formData.get('rating')
        };

        console.log('Submitting CORRECTLY TRANSFORMED review data:', data);

        try {
            const response = await fetch('/api/submissions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();

            if (result.success) {
                reviewForm.reset();
                popup.classList.add('show');
                overlay.classList.add('show');
            } else {
                alert('There was an error submitting your review. Please try again.');
            }
        } catch (error) {
            console.error('Submission error:', error);
            alert('A network error occurred.');
        }
    });
});