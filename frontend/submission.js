document.addEventListener('DOMContentLoaded', () => {

    // --- 1. GET ALL THE ELEMENTS ---
    const form = document.getElementById('mainForm');
    const popup = document.getElementById('popup');
    const overlay = document.getElementById('overlay');
    const submitBtn = form.querySelector('.submit-btn');
    const selectReviewBtn = document.getElementById('selectReviewBtn');
    const selectProposalBtn = document.getElementById('selectProposalBtn');
    
    // FIX: These now match the corrected IDs in your HTML
    const reviewFormSection = document.getElementById('reviewFormSection');
    const proposalFormSection = document.getElementById('proposalFormSection');
    
    const closePopupBtn = document.getElementById('closePopupBtn');
    
    let selectedFormType = null;

    // --- DEFINE WHICH FIELDS ARE REQUIRED FOR EACH FORM ---
    const requiredReviewFields = ['review_name', 'review_lastname', 'review_email', 'review_message', 'review_rating'];
    const requiredProposalFields = ['proposal_firstname', 'proposal_lastname', 'proposal_email', 'proposal_phone', 'proposal_type', 'proposal_description'];


    // --- 2. FUNCTION TO SWITCH BETWEEN FORMS ---
    function selectFormType(type, event) {
        selectedFormType = type;
        
        document.querySelectorAll('.type-option').forEach(opt => opt.classList.remove('active'));
        event.target.classList.add('active');

        // These variables are now correct and will not be null
        reviewFormSection.classList.remove('active');
        proposalFormSection.classList.remove('active');

        form.querySelectorAll('[required]').forEach(el => el.removeAttribute('required'));

        if (type === 'review') {
            reviewFormSection.classList.add('active');
            submitBtn.textContent = 'Submit Review';
            requiredReviewFields.forEach(name => {
                const field = form.querySelector(`[name="${name}"]`);
                if (field) field.setAttribute('required', '');
            });
        } else if (type === 'proposal') {
            proposalFormSection.classList.add('active');
            submitBtn.textContent = 'Submit Proposal';
            requiredProposalFields.forEach(name => {
                const field = form.querySelector(`[name="${name}"]`);
                if (field) field.setAttribute('required', '');
            });
        }
        submitBtn.disabled = false;
    }


    // --- 3. ATTACH CLICK LISTENERS TO BUTTONS ---
    selectReviewBtn.addEventListener('click', (event) => selectFormType('review', event));
    selectProposalBtn.addEventListener('click', (event) => selectFormType('proposal', event));


    // --- 4. HANDLE THE FINAL FORM SUBMISSION ---
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!selectedFormType) {
            alert('Please select a form type');
            return;
        }

        const formData = new FormData(form);
        let data = {};

        if (selectedFormType === 'review') {
            data = {
                type: 'review',
                FNAME: formData.get('review_name'),
                LNAME: formData.get('review_lastname'),
                COMPANY_NAME: formData.get('review_company'),
                EMAIL: formData.get('review_email'),
                REVIEW: formData.get('review_message'),
                RATING: formData.get('review_rating')
            };
        } else if (selectedFormType === 'proposal') {
            data = { type: 'proposal' };
            formData.forEach((value, key) => {
                if (key.startsWith('proposal_')) {
                    data[key] = value;
                }
            });
        }

        console.log('Submitting CORRECTLY TRANSFORMED data:', data);
        
        try {
            const response = await fetch('/api/submissions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            
            if (result.success) {
                popup.classList.add('show');
                overlay.classList.add('show');
                form.reset();
                selectedFormType = null;
                document.querySelectorAll('.type-option').forEach(opt => opt.classList.remove('active'));
                document.querySelectorAll('.form-section').forEach(section => section.classList.remove('active'));
                submitBtn.disabled = true;
                submitBtn.textContent = 'Select a form type to continue';
            } else {
                alert('Submission failed: ' + (result.message || 'Please try again.'));
            }
        } catch (error) {
            console.error('Submission error:', error);
            alert('A network error occurred.');
        }
    });


    // --- 5. POPUP CLOSE FUNCTIONALITY ---
    function closePopup() {
        popup.classList.remove('show');
        overlay.classList.remove('show');
    }
    closePopupBtn.addEventListener('click', closePopup);
    overlay.addEventListener('click', closePopup);
});