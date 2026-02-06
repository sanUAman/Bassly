// Shared auth modal functionality

let isSelectingText = false;

// Track text selection
document.addEventListener('mousedown', function(e) {
    if (e.button === 0) {
        isSelectingText = false;
    }
});

document.addEventListener('mousemove', function(e) {
    if (e.buttons === 1) {
        isSelectingText = true;
    }
});

// Modal functions
function openSigninModal() {
    document.getElementById('signinModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeSigninModal() {
    document.getElementById('signinModal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

function openSignupModal() {
    document.getElementById('signupModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeSignupModal() {
    document.getElementById('signupModal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

function switchToModal(target) {
    if (target === 'signup') {
        closeSigninModal();
        // Use setTimeout to ensure the signin modal is closed first
        setTimeout(function() {
            openSignupModal();
        }, 50);
    } else if (target === 'signin') {
        closeSignupModal();
        setTimeout(function() {
            openSigninModal();
        }, 50);
    }
}

// Handle switch modal links
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.switch-modal-link').forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            var target = this.getAttribute('data-target');
            switchToModal(target);
        });
    });
});

// Close modals when clicking outside
window.addEventListener('click', function(event) {
    const signinModal = document.getElementById('signinModal');
    const signupModal = document.getElementById('signupModal');
    
    // Only close if clicking directly on the modal backdrop and not selecting text
    if (!isSelectingText) {
        if (event.target === signinModal && signinModal.style.display === 'block') {
            closeSigninModal();
        }
        if (event.target === signupModal && signupModal.style.display === 'block') {
            closeSignupModal();
        }
    }
});

// Close modal on Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const signupModal = document.getElementById('signupModal');
        const signinModal = document.getElementById('signinModal');
        
        if (signupModal && signupModal.style.display === 'block') {
            closeSignupModal();
        } else if (signinModal && signinModal.style.display === 'block') {
            closeSigninModal();
        }
    }
});

// Auto-open modal if show_signin_modal is true
document.addEventListener('DOMContentLoaded', function() {
    const signinModal = document.getElementById('signinModal');
    const signupModal = document.getElementById('signupModal');
    
    if (signupModal && signupModal.dataset.showModal === 'true') {
        openSignupModal();
    } else if (signinModal && signinModal.dataset.showModal === 'true') {
        openSigninModal();
    }
});
