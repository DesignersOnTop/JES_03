let modals_container = document.getElementsByClassName('modals-container')[0];
let perfil = document.getElementsByClassName('modal-perfil')[0];

document.addEventListener('click', (event) => {
    // Aquí puedes agregar lógica para determinar cuándo mostrar el modal.
    // Por ejemplo, si haces clic en un botón específico:
    if (event.target.matches('.nav-perfil')) {
        modals_container.style.display = 'block';
    }
});
