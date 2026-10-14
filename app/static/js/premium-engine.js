/* ==========================================================================
   PREMIUM ENGINE JS - PALGRIMIZER AI
   Handles Canvas Particles, 3D Tilt, Magnetic Buttons, and UI Interactions
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initLoadingScreen();
    initParticleEngine();
    initMagneticButtons();
    init3DTilt();
    initScrollReveal();
    initAdvancedSearch();
    initRipples();
});

/* 1. LOADING SCREEN */
function initLoadingScreen() {
    const loader = document.getElementById('globalLoader');
    if (loader) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                loader.classList.add('hidden');
                setTimeout(() => loader.remove(), 500);
            }, 800); // Minimum display time for premium feel
        });
    }
}

/* 2. ADVANCED PARTICLE ENGINE (Canvas) */
function initParticleEngine() {
    const canvas = document.getElementById('particleCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width, height;
    let particles = [];
    
    // Config
    const particleCount = 100;
    const colors = ['#38bdf8', '#8b5cf6', '#22d3ee', '#ffffff'];

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }

    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.size = Math.random() * 2 + 0.5;
            this.speedX = Math.random() * 1 - 0.5;
            this.speedY = Math.random() * 1 - 0.5;
            this.color = colors[Math.floor(Math.random() * colors.length)];
            this.opacity = Math.random();
            this.glow = Math.random() * 10;
        }
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            if (this.x < 0 || this.x > width) this.speedX *= -1;
            if (this.y < 0 || this.y > height) this.speedY *= -1;
            
            // Twinkle
            this.opacity += (Math.random() - 0.5) * 0.1;
            if (this.opacity < 0.1) this.opacity = 0.1;
            if (this.opacity > 1) this.opacity = 1;
        }
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${hexToRgb(this.color)}, ${this.opacity})`;
            ctx.shadowBlur = this.glow;
            ctx.shadowColor = this.color;
            ctx.fill();
        }
    }

    function init() {
        resize();
        window.addEventListener('resize', resize);
        particles = [];
        for (let i = 0; i < particleCount; i++) {
            particles.push(new Particle());
        }
        animate();
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);
        particles.forEach(p => {
            p.update();
            p.draw();
        });
        requestAnimationFrame(animate);
    }

    function hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? 
            `${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)}` : null;
    }

    init();
}

/* 3. MAGNETIC BUTTONS */
function initMagneticButtons() {
    const buttons = document.querySelectorAll('.magnetic-btn');
    buttons.forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            // Move button slightly towards cursor
            btn.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px) scale(1.05)`;
        });
        
        btn.addEventListener('mouseleave', () => {
            btn.style.transform = 'translate(0px, 0px) scale(1)';
        });
    });
}

/* 4. 3D TILT EFFECT FOR CARDS */
function init3DTilt() {
    const cards = document.querySelectorAll('.premium-glass');
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = ((y - centerY) / centerY) * -5; // max 5 deg
            const rotateY = ((x - centerX) / centerX) * 5;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
        });
    });
}

/* 5. SCROLL REVEAL (Intersection Observer) */
function initScrollReveal() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Optional: stop observing once revealed
                // observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.premium-reveal').forEach(el => {
        observer.observe(el);
    });
}

/* 6. ADVANCED SEARCH TOGGLE */
function initAdvancedSearch() {
    const searchOverlay = document.getElementById('aiSearchOverlay');
    const searchInput = document.getElementById('aiSearchInput');
    const searchTriggers = document.querySelectorAll('.search-trigger');
    
    if (!searchOverlay) return;

    // Open Search
    searchTriggers.forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            searchOverlay.classList.add('active');
            setTimeout(() => searchInput.focus(), 100);
        });
    });

    // Close Search
    searchOverlay.addEventListener('click', (e) => {
        if (e.target === searchOverlay) {
            searchOverlay.classList.remove('active');
        }
    });

    // Keyboard Shortcut (Ctrl+K or Cmd+K)
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            searchOverlay.classList.add('active');
            setTimeout(() => searchInput.focus(), 100);
        }
        if (e.key === 'Escape' && searchOverlay.classList.contains('active')) {
            searchOverlay.classList.remove('active');
        }
    });
}

/* 7. RIPPLE CLICK EFFECT */
function initRipples() {
    const rippleButtons = document.querySelectorAll('.ripple-btn');
    rippleButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            let ripple = document.createElement('span');
            ripple.classList.add('ripple');
            this.appendChild(ripple);
            
            let rect = this.getBoundingClientRect();
            let x = e.clientX - rect.left;
            let y = e.clientY - rect.top;
            
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}
