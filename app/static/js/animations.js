/**
 * Palgrimizer Premium Animations & Interactions
 * Handles Parallax, Scroll Animations, Magnetic Buttons, and Ripple Effects.
 * Optimized with requestAnimationFrame for 60 FPS.
 */

document.addEventListener('DOMContentLoaded', () => {
    initParallax();
    initScrollAnimations();
    initMagneticButtons();
    initRippleEffect();
});

/**
 * Parallax Effect for 3D Hero Section
 */
function initParallax() {
    const container = document.querySelector('.parallax-container');
    const layers = document.querySelectorAll('.parallax-layer');
    
    if (!container || layers.length === 0) return;

    let mouseX = 0;
    let mouseY = 0;
    let currentX = 0;
    let currentY = 0;
    let ticking = false;

    // Easing factor
    const ease = 0.05;

    window.addEventListener('mousemove', (e) => {
        // Calculate mouse position relative to center of screen
        mouseX = e.clientX - window.innerWidth / 2;
        mouseY = e.clientY - window.innerHeight / 2;
    });

    function animateParallax() {
        // Smooth interpolation
        currentX += (mouseX - currentX) * ease;
        currentY += (mouseY - currentY) * ease;

        layers.forEach(layer => {
            const speed = parseFloat(layer.getAttribute('data-speed')) || 0;
            const x = currentX * speed;
            const y = currentY * speed;
            layer.style.transform = `translate3d(${x}px, ${y}px, 0)`;
        });

        requestAnimationFrame(animateParallax);
    }

    requestAnimationFrame(animateParallax);
}

/**
 * Scroll Animations (Fade, Slide Up, Scale, Blur Reveal)
 */
function initScrollAnimations() {
    const elements = document.querySelectorAll('.scroll-animate');
    
    if (elements.length === 0) return;

    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show');
                obs.unobserve(entry.target); // Animate only once
            }
        });
    }, observerOptions);

    elements.forEach(el => observer.observe(el));
}

/**
 * Magnetic Hover Effect for Buttons
 */
function initMagneticButtons() {
    const magneticBtns = document.querySelectorAll('.magnetic-btn');

    magneticBtns.forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;

            // Move the button slightly towards the cursor
            btn.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
        });

        btn.addEventListener('mouseleave', () => {
            // Reset to original position smoothly
            btn.style.transform = `translate(0px, 0px)`;
        });
    });
}

/**
 * Premium Ripple Click Effect
 */
function initRippleEffect() {
    const rippleBtns = document.querySelectorAll('.ripple-btn');

    rippleBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            let x = e.clientX - e.target.getBoundingClientRect().left;
            let y = e.clientY - e.target.getBoundingClientRect().top;

            let ripple = document.createElement('span');
            ripple.style.position = 'absolute';
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            ripple.style.width = '0px';
            ripple.style.height = '0px';
            ripple.style.transform = 'translate(-50%, -50%)';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.4)';
            ripple.style.animation = 'ripple-animation 0.6s linear';
            ripple.style.pointerEvents = 'none';

            this.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// Inject Ripple CSS globally
const style = document.createElement('style');
style.innerHTML = `
@keyframes ripple-animation {
    0% {
        width: 0px;
        height: 0px;
        opacity: 0.5;
    }
    100% {
        width: 500px;
        height: 500px;
        opacity: 0;
    }
}
.magnetic-btn {
    transition: transform 0.2s cubic-bezier(0.33, 1, 0.68, 1), box-shadow 0.2s, background-color 0.2s;
}
.ripple-btn {
    position: relative;
    overflow: hidden;
}
`;
document.head.appendChild(style);
