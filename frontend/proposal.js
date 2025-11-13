// --- FIX FOR CLOSE BUTTON: Define this function globally ---
// This makes it visible to the `onclick="closePopup()"` in the HTML.
function closePopup() {
    document.getElementById('popup').classList.remove('show');
    document.getElementById('overlay').classList.remove('show');
}

document.addEventListener('DOMContentLoaded', () => {

    const proposalForm = document.getElementById('proposalForm');
    const popup = document.getElementById('popup');
    const overlay = document.getElementById('overlay');
    
    // Add a click listener to the overlay as well
    overlay.addEventListener('click', closePopup);

    if (proposalForm) {
        proposalForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const formData = new FormData(proposalForm);

            // --- FIX FOR MISSING DATA ---
            // Create the data object that the backend expects.
            // This now includes ALL fields from the form.
            const data = {
                type: 'proposal',
                proposal_firstname: formData.get('proposal_firstname'),
                proposal_lastname: formData.get('proposal_lastname'),
                proposal_company: formData.get('proposal_company'),
                proposal_company_street: formData.get('proposal_company_street'),
                proposal_company_city: formData.get('proposal_company_city'),
                proposal_company_state: formData.get('proposal_company_state'),
                proposal_company_zip: formData.get('proposal_company_zip'),
                proposal_email: formData.get('proposal_email'),
                proposal_phone: formData.get('proposal_phone'),
                proposal_position: formData.get('proposal_position'),
                proposal_street: formData.get('proposal_street'),
                proposal_city: formData.get('proposal_city'),
                proposal_state: formData.get('proposal_state'),
                proposal_zip: formData.get('proposal_zip'),
                proposal_type: formData.get('proposal_type'),
                proposal_start_date: formData.get('proposal_start_date'),
                proposal_timeline: formData.get('proposal_timeline'),
                proposal_budget: formData.get('proposal_budget'),
                proposal_marketing: formData.get('proposal_marketing'),
                proposal_description: formData.get('proposal_description')
            };

            console.log('Submitting complete proposal data:', data);

            try {
                const response = await fetch('http://127.0.0.1:5000/api/submissions', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await response.json();

                if (result.success) {
                    popup.classList.add('show');
                    overlay.classList.add('show');
                    proposalForm.reset();
                } else {
                    alert('Submission failed: ' + (result.message || 'Please try again.'));
                }
            } catch (error) {
                console.error('Submission error:', error);
                alert('A network error occurred.');
            }
        });
    }
});