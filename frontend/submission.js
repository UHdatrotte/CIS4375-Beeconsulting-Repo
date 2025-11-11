
document.addEventListener('DOMContentLoaded', () => {
    const mainForm = document.getElementById('mainForm');
    const reviewSection = document.getElementById('reviewFormSection');
    const proposalSection = document.getElementById('proposalFormSection');
    const submitBtn = mainForm.querySelector('.submit-btn');

    const selectReviewBtn = document.getElementById('selectReviewBtn');
    const selectProposalBtn = document.getElementById('selectProposalBtn');

    const popup = document.getElementById('popup');
    const overlay = document.getElementById('overlay');
    const closePopupBtn = document.getElementById('closePopupBtn');

    let currentType = null; 

    function closePopup() {
        popup.classList.remove('show');
        overlay.classList.remove('show');
    }

    if (closePopupBtn) closePopupBtn.addEventListener('click', closePopup);
    if (overlay) overlay.addEventListener('click', closePopup);

    // ---- Button ----
    selectReviewBtn.addEventListener('click', () => {
        currentType = 'review';
        reviewSection.classList.add('active');
        proposalSection.classList.remove('active');

        selectReviewBtn.classList.add('active');
        selectProposalBtn.classList.remove('active');

        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit Review';
    });

    selectProposalBtn.addEventListener('click', () => {
        currentType = 'proposal';
        proposalSection.classList.add('active');
        reviewSection.classList.remove('active');

        selectProposalBtn.classList.add('active');
        selectReviewBtn.classList.remove('active');

        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit Proposal';
    });

    // ---- submit ----
    mainForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!currentType) {
            alert('First, select the Review or Proposal type.');
            return;
        }

        const formData = new FormData(mainForm);
        let data = {};

        if (currentType === 'review') {
            data = {
                type: 'review',
                FNAME: formData.get('review_name'),
                LNAME: formData.get('review_lastname'),
                COMPANY_NAME: formData.get('review_company'),
                EMAIL: formData.get('review_email'),
                REVIEW: formData.get('review_message'),
                RATING: formData.get('review_rating')
            };
        } else if (currentType === 'proposal') {
            data = {
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
                proposal_description: formData.get('proposal_description'),
                proposal_marketing: formData.get('proposal_marketing')
            };
        }

        console.log('Submitting data:', data);

        try {
            const response = await fetch('http://127.0.0.1:5000/api/submissions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            console.log('Server result:', result);

            if (result.success) {
                mainForm.reset();
                submitBtn.disabled = true;
                submitBtn.textContent = 'Select a form type to continue';

                reviewSection.classList.remove('active');
                proposalSection.classList.remove('active');
                selectReviewBtn.classList.remove('active');
                selectProposalBtn.classList.remove('active');

                popup.classList.add('show');
                overlay.classList.add('show');
            } else {
                alert(result.message || 'There was an error submitting the form.');
            }
        } catch (err) {
            console.error('Submission error:', err);
            alert('A network error occurred.');
        }
    });
});
