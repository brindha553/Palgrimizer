/* ==========================================================================
   PALGRIMIZER THEME SWITCHER MODULE
   ========================================================================== */

(function () {
    const THEME_KEY = 'palgrimizer_theme';
    const COLOR_THEME_KEY = 'palgrimizer_color_theme';

    function getPreferredTheme() {
        const savedTheme = localStorage.getItem(THEME_KEY);
        if (savedTheme) {
            return savedTheme;
        }
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    function getPreferredColorTheme() {
        return localStorage.getItem(COLOR_THEME_KEY) || 'midnight-blue';
    }

    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem(THEME_KEY, theme);
        updateToggleIcons(theme);
    }

    function setColorTheme(colorTheme) {
        document.documentElement.setAttribute('data-color-theme', colorTheme);
        localStorage.setItem(COLOR_THEME_KEY, colorTheme);
    }

    function updateToggleIcons(theme) {
        const toggles = document.querySelectorAll('.theme-toggle-btn');
        toggles.forEach(btn => {
            if (theme === 'dark') {
                btn.innerHTML = '<i data-lucide="sun"></i>';
                btn.setAttribute('title', 'Switch to Light Mode');
            } else {
                btn.innerHTML = '<i data-lucide="moon"></i>';
                btn.setAttribute('title', 'Switch to Dark Mode');
            }
        });
        
        // Re-initialize Lucide icons for the newly injected HTML if lucide is available
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    document.addEventListener('DOMContentLoaded', () => {
        const currentTheme = getPreferredTheme();
        const currentColorTheme = getPreferredColorTheme();
        
        setTheme(currentTheme);
        setColorTheme(currentColorTheme);

        const toggles = document.querySelectorAll('.theme-toggle-btn');
        toggles.forEach(btn => {
            btn.addEventListener('click', () => {
                const activeTheme = document.documentElement.getAttribute('data-theme');
                const newTheme = activeTheme === 'dark' ? 'light' : 'dark';
                setTheme(newTheme);
            });
        });

        // Initialize color theme selectors if they exist on the page
        const colorSelectors = document.querySelectorAll('.color-theme-selector');
        colorSelectors.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const color = e.currentTarget.getAttribute('data-color');
                if (color) {
                    setColorTheme(color);
                }
            });
        });
    });
})();
