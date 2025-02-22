function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const darkModeButton = document.getElementById('dark-mode-button');
    if (darkModeButton.textContent === '🌞') {
        darkModeButton.textContent = '🌙';
    } else {
        darkModeButton.textContent = '🌞';
    }
}