/* ==========================================================================
   PALGRIMIZER MAIN JAVASCRIPT LOGIC
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Toast Notification Helper
    window.showToast = function (message, type = 'info') {
        const container = document.getElementById('toastContainer');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        let iconName = 'info';
        if (type === 'success') iconName = 'check-circle';
        if (type === 'danger') iconName = 'alert-circle';
        if (type === 'warning') iconName = 'alert-triangle';

        toast.innerHTML = `
            <i data-lucide="${iconName}"></i>
            <span>${message}</span>
        `;

        container.appendChild(toast);
        if (typeof lucide !== 'undefined') lucide.createIcons({root: toast});
        
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    };

    // 2. Counter Animations for Statistics
    const counters = document.querySelectorAll('.animate-counter');
    if (counters.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = entry.target;
                    const target = parseFloat(counter.getAttribute('data-target'));
                    const isDec = counter.getAttribute('data-decimal') === 'true';
                    const suffix = counter.getAttribute('data-suffix') || '';

                    let start = 0;
                    const duration = 1500;
                    const stepTime = 20;
                    const steps = duration / stepTime;
                    const increment = target / steps;

                    const timer = setInterval(() => {
                        start += increment;
                        if (start >= target) {
                            counter.innerText = (isDec ? target.toFixed(1) : Math.floor(target)) + suffix;
                            clearInterval(timer);
                        } else {
                            counter.innerText = (isDec ? start.toFixed(1) : Math.floor(start)) + suffix;
                        }
                    }, stepTime);

                    observer.unobserve(counter);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(c => observer.observe(c));
    }

    // 3. Navbar Sticky Shadow & Shrink Effect
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 20) {
                navbar.style.boxShadow = 'var(--shadow-md)';
                navbar.style.padding = '0.5rem 2rem';
                navbar.style.background = 'var(--navbar-bg)';
            } else {
                navbar.style.boxShadow = 'none';
                navbar.style.padding = '0.85rem 2rem';
                navbar.style.background = 'transparent';
            }
        });
    }

    // 3.5 Theme Customizer Toggle
    const themeCustomizerBtn = document.getElementById('themeCustomizerBtn');
    const themeCustomizer = document.getElementById('themeCustomizer');
    
    if (themeCustomizerBtn && themeCustomizer) {
        themeCustomizerBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const isVisible = themeCustomizer.style.display === 'block';
            if (isVisible) {
                themeCustomizer.style.opacity = '0';
                themeCustomizer.style.transform = 'translateY(-10px)';
                setTimeout(() => themeCustomizer.style.display = 'none', 300);
            } else {
                themeCustomizer.style.display = 'block';
                setTimeout(() => {
                    themeCustomizer.style.opacity = '1';
                    themeCustomizer.style.transform = 'translateY(0)';
                }, 10);
            }
        });

        document.addEventListener('click', (e) => {
            if (!themeCustomizer.contains(e.target) && e.target !== themeCustomizerBtn) {
                themeCustomizer.style.opacity = '0';
                themeCustomizer.style.transform = 'translateY(-10px)';
                setTimeout(() => themeCustomizer.style.display = 'none', 300);
            }
        });
    }

    // 4. Live Landing Page Demo Sandbox Handler
    const demoBtn = document.getElementById('runDemoBtn');
    const demoInput = document.getElementById('demoTextInput');
    const demoResultContainer = document.getElementById('demoResultContainer');

    if (demoBtn && demoInput && demoResultContainer) {
        demoBtn.addEventListener('click', async () => {
            const text = demoInput.value;
            demoBtn.innerHTML = '<i data-lucide="loader-2" class="lucide-spin"></i> Analyzing...';
            if (typeof lucide !== 'undefined') lucide.createIcons({root: demoBtn});
            demoBtn.disabled = true;

            try {
                const res = await fetch('/api/demo-analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    const result = data.result;
                    demoResultContainer.innerHTML = `
                        <div class="glass-card" style="padding: 1.25rem;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                                <h4 style="display: flex; align-items: center; gap: 0.5rem;"><i data-lucide="wand-2" class="text-primary"></i> Analysis Result</h4>
                                <span class="badge badge-success">Overall Score: ${result.scores.overall_score}%</span>
                            </div>
                            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; line-height: 1.6; margin-bottom: 1rem;">
                                <strong>Corrected Text:</strong><br>
                                <p style="color: var(--accent-emerald); background: var(--accent-emerald-bg); padding: 0.75rem; border-radius: 8px; margin-top: 0.4rem;">
                                    "${result.corrected_text}"
                                </p>
                            </div>
                            <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                                <span class="badge badge-info">Grammar Score: ${result.scores.grammar_score}%</span>
                                <span class="badge badge-info">Issues Found: ${result.corrections.length}</span>
                                <span class="badge badge-info">Words: ${result.statistics.word_count}</span>
                            </div>
                        </div>
                    `;
                    if (typeof lucide !== 'undefined') lucide.createIcons({root: demoResultContainer});
                }
            } catch (err) {
                showToast('Failed to run demo analysis.', 'danger');
            } finally {
                demoBtn.innerHTML = '<i data-lucide="zap"></i> Test AI Correction';
                if (typeof lucide !== 'undefined') lucide.createIcons({root: demoBtn});
                demoBtn.disabled = false;
            }
        });
    }
});
