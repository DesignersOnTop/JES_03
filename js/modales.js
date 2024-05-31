// Mostrar el modal de recordatorio
document.querySelector('.calendario-container').addEventListener('click', function() {
    document.querySelector('#modal-recordatorio').style.display = 'block';
    document.querySelector('.modals-container').style.display = 'flex';
    const perfilModal = document.querySelector('.modal-perfil');
    if (perfilModal) perfilModal.style.display = 'none';
});

// Mostrar el modal de perfil
document.querySelector('.li-perfil').addEventListener('click', function() {
    const perfilModal = document.querySelector('.modal-perfil');
    if (perfilModal) perfilModal.style.display = 'flex';
    document.querySelector('.modals-container').style.display = 'flex';
    document.querySelector('#modal-recordatorio').style.display = 'none';
});

// Cerrar los modales al hacer clic fuera
document.querySelector('.modals-container').addEventListener('click', function(event) {
    if (event.target === this) {
        this.style.display = 'none';
        const recordatorioModal = document.querySelector('#modal-recordatorio');
        if (recordatorioModal) recordatorioModal.style.display = 'none';
        const perfilModal = document.querySelector('.modal-perfil');
        if (perfilModal) perfilModal.style.display = 'none';
    }
});