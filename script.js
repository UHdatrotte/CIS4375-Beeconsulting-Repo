
        let selectedFormType = null;
        const form = document.getElementById('mainForm');
        const popup = document.getElementById('popup');
        const overlay = document.getElementById('overlay');
        const submitBtn = form.querySelector('.submit-btn');

        function selectFormType(type) {
            selectedFormType = type;
            
            // Update visual selection
            document.querySelectorAll('.type-option').forEach(opt => {
                opt.classList.remove('active');
            });
            event.target.closest('.type-option').classList.add('active');

            // Show appropriate form
            document.querySelectorAll('.form-section').forEach(section => {
                section.classList.remove('active');
            });

            if (type === 'review') {
                document.getElementById('reviewForm').classList.add('active');
                submitBtn.textContent = 'Submit Review';
                // Clear proposal fields
                document.querySelectorAll('#proposalForm input, #proposalForm textarea, #proposalForm select').forEach(field => {
                    field.removeAttribute('required');
                });
                // Set review fields as required
                document.querySelectorAll('#reviewForm input[required], #reviewForm textarea[required]').forEach(field => {
                    field.setAttribute('required', 'required');
                });
            } else if (type === 'proposal') {
                document.getElementById('proposalForm').classList.add('active');
                submitBtn.textContent = 'Submit Proposal';
                // Clear review fields
                document.querySelectorAll('#reviewForm input, #reviewForm textarea').forEach(field => {
                    field.removeAttribute('required');
                });
                // Set proposal fields as required
                document.querySelectorAll('#proposalForm input[required], #proposalForm textarea[required], #proposalForm select[required]').forEach(field => {
                    field.setAttribute('required', 'required');
                });
            }

            submitBtn.disabled = false;
        }

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (!selectedFormType) {
                alert('Please select a form type');
                return;
            }

            // Collect form data
            const formData = new FormData(form);
            const data = {
                type: selectedFormType,
                status: 'waiting',
                submittedAt: new Date().toISOString()
            };

            formData.forEach((value, key) => {
                if (value) data[key] = value;
            });

            console.log('Form submission data:', data);
            
            // In a real application, send data to server here
            // fetch('/api/submissions', { method: 'POST', body: JSON.stringify(data) })

            // Show popup
            popup.classList.add('show');
            overlay.classList.add('show');
            
            // Reset form
            form.reset();
            selectedFormType = null;
            document.querySelectorAll('.type-option').forEach(opt => {
                opt.classList.remove('active');
            });
            document.querySelectorAll('.form-section').forEach(section => {
                section.classList.remove('active');
            });
            submitBtn.disabled = true;
            submitBtn.textContent = 'Select a form type to continue';
        });

        function closePopup() {
            popup.classList.remove('show');
            overlay.classList.remove('show');
        }

        overlay.addEventListener('click', closePopup);
