document.addEventListener('DOMContentLoaded', function() {
    // Tab switching
    const tabs = document.querySelectorAll('.tab');
    const forms = document.querySelectorAll('.form');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.getAttribute('data-tab');
            
            // Toggle active class for tabs
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Toggle active class for forms
            forms.forEach(form => form.classList.remove('active'));
            document.getElementById(targetTab + 'Form').classList.add('active');
            
            // Update tagline
            const tagline = document.getElementById('tagline');
            if (targetTab === 'login') {
                tagline.textContent = 'Continue your Skill Path Journey';
            } else {
                tagline.textContent = "Let's build your SkillPath!";
            }
        });
    });
    
    // Show/Hide Password Toggle
    const togglePasswordBtns = document.querySelectorAll('.toggle-password');
    
    togglePasswordBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const passwordInput = this.previousElementSibling;
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
            // Toggle eye icon
            const icon = this.querySelector('i');
            icon.classList.toggle('fa-eye');
            icon.classList.toggle('fa-eye-slash');
        });
    });
    
    // Switch between login and signup
    const switchToSignup = document.querySelector('.switch-to-signup');
    switchToSignup.addEventListener('click', function(e) {
        e.preventDefault();
        tabs.forEach(t => t.classList.remove('active'));
        tabs[1].classList.add('active');
        
        forms.forEach(form => form.classList.remove('active'));
        document.getElementById('signupForm').classList.add('active');
        
        document.getElementById('tagline').textContent = "Let's build your SkillPath!";
    });
    
    // OTP Toggle
    const otpToggle = document.querySelector('.otp-toggle');
    otpToggle.addEventListener('click', function() {
        const passwordGroup = document.querySelector('#loginForm .form-group:nth-child(2)');
        const loginIdLabel = document.querySelector('#loginForm .form-group:nth-child(1) label');
        
        if (this.textContent === 'Switch to OTP Login') {
            passwordGroup.style.display = 'none';
            loginIdLabel.textContent = 'Phone Number';
            this.textContent = 'Switch to Password Login';
        } else {
            passwordGroup.style.display = 'block';
            loginIdLabel.textContent = 'Phone / Email';
            this.textContent = 'Switch to OTP Login';
        }
    });
    
    // Multi-step signup
    const nextBtns = document.querySelectorAll('.step-btn.next');
    const prevBtns = document.querySelectorAll('.step-btn.prev');
    const signupSteps = document.querySelector('.signup-steps');
    const stepDots = document.querySelectorAll('.step-dot');
    let currentStep = 0;
    
    nextBtns.forEach((btn, index) => {
        btn.addEventListener('click', function() {
            if (validateStep(currentStep)) {
                if (index < 2) { // Not the last step
                    currentStep++;
                    updateStepUI();
                } else {
                    // Handle form submission
                    handleSignup();
                }
            }
        });
    });
    
    prevBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            currentStep--;
            updateStepUI();
        });
    });
    
    function updateStepUI() {
        signupSteps.style.transform = `translateX(-${currentStep * 33.33}%)`;
        stepDots.forEach((dot, i) => {
            dot.classList.toggle('active', i === currentStep);
        });
    }
    
    function validateStep(step) {
        let isValid = true;
        
        switch(step) {
            case 0:
                // Validate full name and phone number
                const fullName = document.getElementById('fullName').value;
                const phoneNumber = document.getElementById('phoneNumber').value;
                const password = document.getElementById('signupPassword').value;
                
                if (!fullName || !phoneNumber || !password) {
                    isValid = false;
                    showError('Please fill in all required fields');
                }
                break;
                
            case 1:
                // Validate language and career interests
                const language = document.getElementById('preferredLanguage').value;
                const selectedCareers = document.querySelectorAll('.career-tag.selected');
                
                if (!language || selectedCareers.length === 0) {
                    isValid = false;
                    showError('Please select language and at least one career interest');
                }
                break;
                
            case 2:
                // Validate terms agreement
                const termsAgreed = document.getElementById('termsAgree').checked;
                
                if (!termsAgreed) {
                    isValid = false;
                    showError('Please agree to the terms and conditions');
                }
                break;
        }
        
        return isValid;
    }
    
    function showError(message) {
        // Create and show error toast
        const toast = document.createElement('div');
        toast.className = 'error-toast';
        toast.textContent = message;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }
    
    // Password strength meter
    const passwordInput = document.getElementById('signupPassword');
    const strengthMeter = document.querySelector('.password-strength-meter');
    const strengthText = document.querySelector('.password-strength-text');
    const passwordStrength = document.querySelector('.password-strength');
    
    passwordInput.addEventListener('input', function() {
        const val = this.value;
        
        if (val.length > 0) {
            passwordStrength.style.display = 'block';
        } else {
            passwordStrength.style.display = 'none';
            return;
        }
        
        let strength = calculatePasswordStrength(val);
        
        updatePasswordStrengthUI(strength);
    });
    
    function calculatePasswordStrength(password) {
        let strength = 0;
        
        if (password.length >= 8) strength += 25;
        if (/\d/.test(password)) strength += 25;
        if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) strength += 25;
        if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength += 25;
        
        return strength;
    }
    
    function updatePasswordStrengthUI(strength) {
        strengthMeter.style.width = `${strength}%`;
        
        if (strength < 25) {
            strengthMeter.style.backgroundColor = '#e74c3c';
            strengthText.textContent = 'Weak';
            strengthText.style.color = '#e74c3c';
        } else if (strength < 50) {
            strengthMeter.style.backgroundColor = '#f39c12';
            strengthText.textContent = 'Fair';
            strengthText.style.color = '#f39c12';
        } else if (strength < 75) {
            strengthMeter.style.backgroundColor = '#f1c40f';
            strengthText.textContent = 'Good';
            strengthText.style.color = '#f1c40f';
        } else {
            strengthMeter.style.backgroundColor = '#2ecc71';
            strengthText.textContent = 'Strong';
            strengthText.style.color = '#2ecc71';
        }
    }
    
    // Career tags selection
    const careerTags = document.querySelectorAll('.career-tag');
    
    careerTags.forEach(tag => {
        tag.addEventListener('click', function() {
            this.classList.toggle('selected');
        });
    });
    
    // Handle login
    const loginBtn = document.getElementById('loginBtn');
    loginBtn.addEventListener('click', handleLogin);
    
    function handleLogin() {
        const loginId = document.getElementById('loginId').value;
        const password = document.getElementById('loginPassword').value;
        
        if (!validateLogin(loginId, password)) {
            return;
        }
        
        // Show loader
        toggleLoginLoader(true);
        
        // Simulate API call
        setTimeout(() => {
            toggleLoginLoader(false);
            // Redirect to dashboard
            window.location.href = '/dashboard';
        }, 1500);
    }
    
    function validateLogin(loginId, password) {
        if (!loginId) {
            showError('Please enter your phone number or email');
            return false;
        }
        
        if (!password && !document.querySelector('.otp-toggle').textContent.includes('Password')) {
            showError('Please enter your password');
            return false;
        }
        
        return true;
    }
    
    function toggleLoginLoader(show) {
        const loginBtn = document.getElementById('loginBtn');
        loginBtn.querySelector('span').style.display = show ? 'none' : 'block';
        loginBtn.querySelector('.loader').style.display = show ? 'block' : 'none';
    }
    
    // Handle signup
    function handleSignup() {
        const createAccountBtn = document.getElementById('createAccountBtn');
        
        // Show loader
        createAccountBtn.innerHTML = '<div class="loader" style="display: block;"></div>';
        
        // Gather all form data
        const formData = {
            fullName: document.getElementById('fullName').value,
            phoneNumber: document.getElementById('phoneNumber').value,
            password: document.getElementById('signupPassword').value,
            language: document.getElementById('preferredLanguage').value,
            careers: Array.from(document.querySelectorAll('.career-tag.selected')).map(tag => tag.dataset.value),
            enableOffline: document.getElementById('enableOffline').checked
        };
        
        // Simulate API call
        setTimeout(() => {
            createAccountBtn.innerHTML = 'Create Account';
            // Redirect to onboarding
            window.location.href = '/onboarding';
        }, 1500);
    }
});
