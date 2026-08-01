document.addEventListener('DOMContentLoaded', function () {
    
    // Mobile Navigation Toggle
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }

    // Delete Confirmation
    const deleteForms = document.querySelectorAll('form[action*="delete"]');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            if (confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                const btn = form.querySelector('button');
                if (btn) {
                    btn.innerHTML = '...';
                    btn.disabled = true;
                }
                form.submit();
            }
        });
    });

    // Loading State for Non-Delete Forms
    const forms = document.querySelectorAll('form:not([action*="delete"])');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Let HTML5 required validation trigger first
            if (!form.checkValidity()) return;
            
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                // Slight delay to ensure the request initiates
                setTimeout(() => {
                    submitBtn.innerHTML = 'Processing...';
                    submitBtn.disabled = true;
                    submitBtn.style.opacity = '0.7';
                }, 10);
            }
        });
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    // Set default date to today for Add Transaction form
    const dateInput = document.getElementById('date');
    if (dateInput && !dateInput.value) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.value = today;
    }

});