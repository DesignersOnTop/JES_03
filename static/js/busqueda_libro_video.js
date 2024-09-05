document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.querySelector('.search-input');
    if (!searchInput) return;

    searchInput.addEventListener('input', function () {
        const query = this.value.toLowerCase();
        if (document.querySelector('#libros-section')) {
            const libros = document.querySelectorAll('#libros-section .contenedor-material');
            libros.forEach(function (libro) {
                const nomAsignatura = libro.getAttribute('data-nom-asignatura');
                const titulo = libro.getAttribute('data-titulo');
                libro.style.display = (nomAsignatura.includes(query) || titulo.includes(query)) ? '' : 'none';
            });
        } else if (document.querySelector('#videos-table')) {
            const rows = document.querySelectorAll('#videos-table .video-row');
            rows.forEach(function (row) {
                const nomAsignatura = row.getAttribute('data-nom-asignatura');
                const titulo = row.getAttribute('data-titulo');
                row.style.display = (nomAsignatura.includes(query) || titulo.includes(query)) ? '' : 'none';
            });
        }
    });
});
