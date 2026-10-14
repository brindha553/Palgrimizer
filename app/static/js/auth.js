/* ==========================================================================
   PALGRIMIZER AUTHENTICATION JAVASCRIPT
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Password Strength Meter
    const pwdInput = document.getElementById('passwordInput');
    const strengthBar = document.getElementById('strengthBar');
    const strengthText = document.getElementById('strengthText');

    if (pwdInput && strengthBar) {
        pwdInput.addEventListener('input', () => {
            const val = pwdInput.value;
            let score = 0;

            if (val.length >= 6) score += 25;
            if (val.length >= 10) score += 25;
            if (/[A-Z]/.test(val)) score += 20;
            if (/[0-9]/.test(val)) score += 15;
            if (/[^A-Za-z0-9]/.test(val)) score += 15;

            strengthBar.style.width = score + '%';

            if (score < 40) {
                strengthBar.style.backgroundColor = 'var(--accent-crimson)';
                if (strengthText) strengthText.innerText = 'Weak Password';
            } else if (score < 75) {
                strengthBar.style.backgroundColor = 'var(--accent-amber)';
                if (strengthText) strengthText.innerText = 'Moderate Password';
            } else {
                strengthBar.style.backgroundColor = 'var(--accent-emerald)';
                if (strengthText) strengthText.innerText = 'Strong Enterprise Password';
            }
        });
    }

    // 2. Show / Hide Password Toggle
    const pwdToggles = document.querySelectorAll('.pwd-toggle-btn');
    pwdToggles.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-target');
            const targetInput = document.getElementById(targetId);
            if (targetInput) {
                const isPassword = targetInput.type === 'password';
                targetInput.type = isPassword ? 'text' : 'password';
                const icon = btn.querySelector('i');
                if (icon) {
                    icon.className = isPassword ? 'fas fa-eye-slash' : 'fas fa-eye';
                }
            }
        });
    });

    // 3. Google Social Login Simulation
    const googleBtn = document.getElementById('googleLoginBtn');
    if (googleBtn) {
        googleBtn.addEventListener('click', async () => {
            googleBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Authenticating with Google...';
            try {
                const res = await fetch('/auth/google-login-sim', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name: 'Enterprise User', email: 'user.sso@palgrimizer.io' })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    window.location.href = data.redirect_url;
                }
            } catch (e) {
                window.showToast('Google login failed.', 'danger');
            }
        });
    }
});
