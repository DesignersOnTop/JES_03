document.addEventListener('DOMContentLoaded', function() {
    const modalsContainer = document.querySelector('.modals-container');

    modalsContainer.addEventListener('click', function(event) {
        if (event.target === modalsContainer) {
            window.location.href = '/home/profesor';
        }
    });

    const modalPerfil = document.querySelector('.modal-perfil');

    modalPerfil.addEventListener('click', function(event) {
        event.stopPropagation();
    });

    const modalOverlay = document.getElementById('modalOverlay');
    function showModal() {
        modalOverlay.classList.add('active');
    }
    showModal();
});
