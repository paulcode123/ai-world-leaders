// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all interactive features
    initDonationForm();
    initPayPalDonation();
    initSmoothScrolling();
    initAnimationOnScroll();
    initNavbarEffects();
    
    // Donation form functionality
    function initDonationForm() {
        const amountButtons = document.querySelectorAll('.amount-btn');
        const customAmountInput = document.getElementById('customAmount');
        
        if (amountButtons.length > 0) {
            amountButtons.forEach(button => {
                button.addEventListener('click', function(e) {
                    e.preventDefault();
                    
                    // Remove active class from all buttons
                    amountButtons.forEach(btn => btn.classList.remove('active'));
                    
                    // Add active class to clicked button
                    this.classList.add('active');
                    
                    // Set custom amount input value
                    const amount = this.getAttribute('data-amount');
                    if (customAmountInput) {
                        customAmountInput.value = amount;
                    }
                    
                    // Update PayPal button if available
                    updatePayPalButton();
                });
            });
        }
        
        // Handle custom amount input
        if (customAmountInput) {
            customAmountInput.addEventListener('input', function() {
                // Remove active class from all buttons when typing custom amount
                amountButtons.forEach(btn => btn.classList.remove('active'));
                // Update PayPal button with new amount
                updatePayPalButton();
            });
        }
    }
    
    // PayPal donation integration
    function initPayPalDonation() {
        // Only initialize if PayPal SDK is loaded and we're on the donate page
        if (typeof paypal === 'undefined' || !document.getElementById('paypal-button-container')) {
            return;
        }
        
        renderPayPalButton();
    }
    
    function renderPayPalButton() {
        const paypalContainer = document.getElementById('paypal-button-container');
        if (!paypalContainer) return;
        
        // Clear any existing buttons
        paypalContainer.innerHTML = '';
        
        paypal.Buttons({
            createOrder: function(data, actions) {
                const amount = getDonationAmount();
                const donorInfo = getDonorInfo();
                
                return actions.order.create({
                    purchase_units: [{
                        amount: {
                            value: amount,
                            currency_code: 'USD'
                        },
                        description: 'Donation to AI World Leaders Education Mission',
                        soft_descriptor: 'AI World Leaders'
                    }]
                });
            },
            onApprove: function(data, actions) {
                return actions.order.capture().then(function(details) {
                    // Show success message
                    showDonationSuccess(details);
                    
                    // Optional: Send donation details to your server
                    sendDonationToServer(details);
                });
            },
            onError: function(err) {
                console.error('PayPal Error:', err);
                showDonationError('There was an error processing your donation. Please try again.');
            },
            onCancel: function(data) {
                showDonationInfo('Donation cancelled. You can try again anytime.');
            },
            style: {
                color: 'gold',
                shape: 'rect',
                label: 'donate',
                height: 40
            }
        }).render('#paypal-button-container');
    }
    
    function updatePayPalButton() {
        // Re-render PayPal button when amount changes
        setTimeout(renderPayPalButton, 100);
    }
    
    function getDonationAmount() {
        const customAmount = document.getElementById('customAmount');
        const activeButton = document.querySelector('.amount-btn.active');
        
        if (customAmount && customAmount.value && parseFloat(customAmount.value) > 0) {
            return customAmount.value;
        } else if (activeButton) {
            return activeButton.getAttribute('data-amount');
        }
        return '25'; // Default amount
    }
    
    function getDonorInfo() {
        return {
            firstName: document.getElementById('firstName')?.value || '',
            lastName: document.getElementById('lastName')?.value || '',
            email: document.getElementById('email')?.value || '',
            message: document.getElementById('message')?.value || ''
        };
    }
    
    function showDonationSuccess(details) {
        // Show a brief success message
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-success alert-dismissible fade show';
        alertDiv.innerHTML = `
            <i class="fas fa-check-circle me-2"></i>
            <strong>Thank you for your donation!</strong> Redirecting you to see your impact...
        `;
        
        const container = document.querySelector('.paypal-section');
        container.insertBefore(alertDiv, container.firstChild);
        
        // Scroll to success message
        alertDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Redirect to thank you page after a brief delay
        setTimeout(() => {
            const amount = details.purchase_units[0].amount.value;
            window.location.href = `/thank-you?amount=${amount}`;
        }, 2000);
    }
    
    function showDonationError(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show';
        alertDiv.innerHTML = `
            <i class="fas fa-exclamation-circle me-2"></i>
            <strong>Donation Error:</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.paypal-section');
        container.insertBefore(alertDiv, container.firstChild);
    }
    
    function showDonationInfo(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-info alert-dismissible fade show';
        alertDiv.innerHTML = `
            <i class="fas fa-info-circle me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.paypal-section');
        container.insertBefore(alertDiv, container.firstChild);
    }
    
    function sendDonationToServer(details) {
        // Optional: Send donation details to your Flask server for record keeping
        const donorInfo = getDonorInfo();
        
        fetch('/donation-success', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                paypal_details: details,
                donor_info: donorInfo,
                amount: details.purchase_units[0].amount.value
            })
        }).catch(err => {
            console.log('Could not send donation details to server:', err);
        });
    }
    
    // Smooth scrolling for anchor links
    function initSmoothScrolling() {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                
                if (href === '#') return;
                
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    
                    const offsetTop = target.getBoundingClientRect().top + window.pageYOffset - 80;
                    
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
    
    // Animation on scroll functionality
    function initAnimationOnScroll() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);
        
        // Observe elements that should animate in
        const animateElements = document.querySelectorAll('.feature-card, .founder-card, .impact-card, .timeline-item, .story-item');
        
        animateElements.forEach((el, index) => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
            observer.observe(el);
        });
        
        // Number counter animation
        const countElements = document.querySelectorAll('.stat-number, .achievement-number');
        const countObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                    animateNumber(entry.target);
                    entry.target.classList.add('counted');
                }
            });
        }, observerOptions);
        
        countElements.forEach(el => {
            countObserver.observe(el);
        });
    }
    
    // Animate numbers counting up
    function animateNumber(element) {
        const text = element.textContent;
        const isInfinity = text.includes('∞');
        
        if (isInfinity) return; // Don't animate infinity symbol
        
        const finalNumber = parseInt(text.replace(/[^\d]/g, ''));
        if (isNaN(finalNumber)) return;
        
        let currentNumber = 0;
        const increment = finalNumber / 50; // Animate over 50 steps
        const duration = 2000; // 2 seconds
        const stepTime = duration / 50;
        
        const timer = setInterval(() => {
            currentNumber += increment;
            if (currentNumber >= finalNumber) {
                currentNumber = finalNumber;
                clearInterval(timer);
            }
            element.textContent = Math.round(currentNumber).toString();
        }, stepTime);
    }
    
    // Navbar effects on scroll
    function initNavbarEffects() {
        const navbar = document.querySelector('.navbar');
        let lastScrollTop = 0;
        
        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            // Add/remove background based on scroll position
            if (scrollTop > 50) {
                navbar.style.background = 'rgba(31, 41, 55, 0.98)';
                navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.15)';
            } else {
                navbar.style.background = 'rgba(31, 41, 55, 0.95)';
                navbar.style.boxShadow = '0 1px 20px rgba(0, 0, 0, 0.1)';
            }
            
            // Hide/show navbar on scroll (optional)
            if (scrollTop > lastScrollTop && scrollTop > 300) {
                // Scrolling down
                navbar.style.transform = 'translateY(-100%)';
            } else {
                // Scrolling up
                navbar.style.transform = 'translateY(0)';
            }
            
            lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
        });
    }
    
    // Form submission handlers
    const contactForm = document.querySelector('form[action*="contact"]');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            const originalText = submitButton.innerHTML;
            
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';
            submitButton.disabled = true;
            
            // Re-enable button after a delay (since we're not actually processing the form)
            setTimeout(() => {
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            }, 2000);
        });
    }
    
    // Add hover effects to cards
    const hoverCards = document.querySelectorAll('.feature-card, .founder-card, .impact-card, .achievement-card');
    hoverCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = this.style.transform.replace('translateY(0px)', '') + ' translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = this.style.transform.replace('translateY(-10px)', 'translateY(0px)');
        });
    });
    
    // Parallax effect for hero section
    const hero = document.querySelector('.hero-section');
    if (hero) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            
            if (hero.querySelector('.hero-content')) {
                hero.querySelector('.hero-content').style.transform = `translateY(${rate}px)`;
            }
        });
    }
    
    // Add typing effect to hero text (optional)
    const heroTitle = document.querySelector('.hero-section h1');
    if (heroTitle && heroTitle.textContent.includes('Artificial Intelligence')) {
        const text = heroTitle.innerHTML;
        const aiText = 'Artificial Intelligence';
        const newText = text.replace(aiText, '<span class="typing-effect">' + aiText + '</span>');
        heroTitle.innerHTML = newText;
        
        const typingElement = heroTitle.querySelector('.typing-effect');
        if (typingElement) {
            typingElement.style.borderRight = '2px solid rgba(255,255,255,0.7)';
            typingElement.style.animation = 'typing 3s steps(20, end), blink-caret 0.75s step-end infinite';
        }
    }
    
    // Add CSS for typing effect
    const style = document.createElement('style');
    style.textContent = `
        @keyframes typing {
            from { width: 0; }
            to { width: 100%; }
        }
        
        @keyframes blink-caret {
            from, to { border-color: transparent; }
            50% { border-color: rgba(255,255,255,0.7); }
        }
        
        .typing-effect {
            overflow: hidden;
            white-space: nowrap;
            display: inline-block;
        }
    `;
    document.head.appendChild(style);
    
    // Easter egg: Konami code
    let konamiCode = [];
    const targetCode = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65]; // Up Up Down Down Left Right Left Right B A
    
    document.addEventListener('keydown', function(e) {
        konamiCode.push(e.keyCode);
        
        if (konamiCode.length > targetCode.length) {
            konamiCode.shift();
        }
        
        if (konamiCode.length === targetCode.length && 
            konamiCode.every((code, index) => code === targetCode[index])) {
            
            // Easter egg activated!
            document.body.style.animation = 'rainbow 2s infinite';
            
            const style = document.createElement('style');
            style.textContent = `
                @keyframes rainbow {
                    0% { filter: hue-rotate(0deg); }
                    100% { filter: hue-rotate(360deg); }
                }
            `;
            document.head.appendChild(style);
            
            setTimeout(() => {
                document.body.style.animation = '';
            }, 5000);
            
            console.log('🎉 AI World Leaders Easter Egg Activated! 🎉');
        }
    });
    
    // Preloader (if present)
    const preloader = document.querySelector('.preloader');
    if (preloader) {
        window.addEventListener('load', function() {
            preloader.style.opacity = '0';
            setTimeout(() => {
                preloader.style.display = 'none';
            }, 500);
        });
    }
    
    // Add performance monitoring
    if ('performance' in window) {
        window.addEventListener('load', function() {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                console.log(`Page loaded in ${Math.round(perfData.loadEventEnd - perfData.loadEventStart)}ms`);
            }, 0);
        });
    }
    
});

// Utility functions
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
} 