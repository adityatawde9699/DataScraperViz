// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // Mobile Navigation Toggle
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    hamburger?.addEventListener('click', function() {
        navLinks.classList.toggle('active');
        this.classList.toggle('open');
    });

    // Language Selection
    const langOptions = document.querySelectorAll('.lang-option');
    langOptions.forEach(option => {
        option.addEventListener('click', function() {
            const lang = this.getAttribute('data-lang');
            setLanguage(lang);
        });
    });

    // Career Cards Interaction
    const careerCards = document.querySelectorAll('.career-card');
    careerCards.forEach(card => {
        card.addEventListener('click', function() {
            const role = this.getAttribute('data-role');
            navigateToCareerPath(role);
        });
    });

    // Smooth Scrolling for Navigation Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Intersection Observer for Animations
    const observerOptions = {
        root: null,
        threshold: 0.1,
        rootMargin: '0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements with animation classes
    document.querySelectorAll('.usp-card, .career-card, .lang-option').forEach(el => {
        observer.observe(el);
    });

    // Header Scroll Effect
    let lastScroll = 0;
    const header = document.querySelector('header');

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll <= 0) {
            header.classList.remove('scroll-up');
            return;
        }

        if (currentScroll > lastScroll && !header.classList.contains('scroll-down')) {
            // Scrolling down
            header.classList.remove('scroll-up');
            header.classList.add('scroll-down');
        } else if (currentScroll < lastScroll && header.classList.contains('scroll-down')) {
            // Scrolling up
            header.classList.remove('scroll-down');
            header.classList.add('scroll-up');
        }
        lastScroll = currentScroll;
    });
});

// Language Selection Handler
function setLanguage(lang) {
    // Store language preference
    localStorage.setItem('preferredLanguage', lang);
    
    // Update UI to show selected language
    document.querySelectorAll('.lang-option').forEach(option => {
        option.classList.remove('default-lang');
        if (option.getAttribute('data-lang') === lang) {
            option.classList.add('default-lang');
        }
    });

    // Trigger language change event
    const event = new CustomEvent('languageChanged', { detail: { language: lang } });
    document.dispatchEvent(event);
}

// Career Path Navigation
function navigateToCareerPath(role) {
    // Add loading state
    const card = document.querySelector(`[data-role="${role}"]`);
    card.classList.add('loading');

    // Simulate API call delay
    setTimeout(() => {
        // Navigate to career path page
        window.location.href = `/career-path/${role}`;
    }, 300);
}

// Form Validation Helper
function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error');
            
            // Add error message
            const errorMsg = input.nextElementSibling?.classList.contains('error-message') 
                ? input.nextElementSibling 
                : document.createElement('span');
            
            errorMsg.className = 'error-message';
            errorMsg.textContent = `${input.getAttribute('placeholder') || 'This field'} is required`;
            
            if (!input.nextElementSibling?.classList.contains('error-message')) {
                input.parentNode.insertBefore(errorMsg, input.nextSibling);
            }
        } else {
            input.classList.remove('error');
            const errorMsg = input.nextElementSibling;
            if (errorMsg?.classList.contains('error-message')) {
                errorMsg.remove();
            }
        }
    });

    return isValid;
}

// Add CSS classes for animations
const css = `
    .scroll-down {
        transform: translateY(-100%);
        transition: transform 0.3s ease-in-out;
    }

    .scroll-up {
        transform: translateY(0);
        transition: transform 0.3s ease-in-out;
    }

    .loading {
        opacity: 0.7;
        pointer-events: none;
        position: relative;
    }

    .loading::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 20px;
        height: 20px;
        border: 2px solid var(--primary-color);
        border-top-color: transparent;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
    }

    @keyframes spin {
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }

    .error {
        border-color: #ff4444 !important;
    }

    .error-message {
        color: #ff4444;
        font-size: 12px;
        margin-top: 4px;
        display: block;
    }
`;

// Add styles to document
const styleSheet = document.createElement('style');
styleSheet.textContent = css;
document.head.appendChild(styleSheet);