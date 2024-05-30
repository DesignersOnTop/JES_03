document.querySelector('.li-perfil').addEventListener('click', function() {
    document.querySelector('.modals-container').style.display = 'flex';
});
    document.querySelector('.modals-container').addEventListener('click', function(event) {
        // Check if the click is outside the modal content
        if (event.target === this) {
            this.style.display = 'none';
        }
    });