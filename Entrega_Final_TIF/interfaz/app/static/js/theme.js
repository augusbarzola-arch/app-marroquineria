/**
 * theme.js - Manejo del modo claro / oscuro con persistencia en localStorage
 */
(() => {
    'use strict';

    const getStoredTheme = () => localStorage.getItem('theme');
    const setStoredTheme = theme => localStorage.setItem('theme', theme);

    const getPreferredTheme = () => {
        const storedTheme = getStoredTheme();
        if (storedTheme) {
            return storedTheme;
        }
        return 'dark'; // Por defecto tema oscuro moderno con glassmorphism
    };

    const setTheme = theme => {
        document.documentElement.setAttribute('data-bs-theme', theme);
        const icon = document.getElementById('theme-icon');
        const text = document.getElementById('theme-text');
        if (icon) {
            if (theme === 'dark') {
                icon.className = 'bi bi-sun-fill text-warning';
                if (text) text.textContent = 'Modo Claro';
            } else {
                icon.className = 'bi bi-moon-stars-fill text-secondary';
                if (text) text.textContent = 'Modo Oscuro';
            }
        }
    };

    // Aplicar inmediatamente para evitar parpadeos
    setTheme(getPreferredTheme());

    window.addEventListener('DOMContentLoaded', () => {
        setTheme(getPreferredTheme());

        const toggleBtn = document.getElementById('theme-toggle-btn');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                const currentTheme = document.documentElement.getAttribute('data-bs-theme');
                const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                setStoredTheme(newTheme);
                setTheme(newTheme);
            });
        }
    });
})();
