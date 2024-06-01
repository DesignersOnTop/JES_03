document.addEventListener('DOMContentLoaded', function() {
    // Mostrar el modal de perfil
    document.querySelector('.li-perfil').addEventListener('click', function() {
        const perfilModal = document.querySelector('.modal-perfil');
        if (perfilModal) perfilModal.style.display = 'flex';
        document.querySelector('.modals-container').style.display = 'flex';
    });

    // Cerrar el modal al hacer clic fuera
    document.querySelector('.modals-container').addEventListener('click', function(event) {
        if (event.target === this) {
            this.style.display = 'none';
            const perfilModal = document.querySelector('.modal-perfil');
            if (perfilModal) perfilModal.style.display = 'none';
        }
    });
});