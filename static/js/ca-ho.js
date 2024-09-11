// Selección de elementos
const btnHorario = document.querySelector('.btn-horario');
const btnCalificacion = document.querySelector('.btn-calificaciones');
const tablaCalificacion = document.querySelector('.tabla-calificacion');
const tablaHorario = document.querySelector('.tabla-horario');
const ch_scroll = document.querySelector('.ca-ho-scroll');

// Función para deseleccionar todos los botones
function deseleccionarBotones() {
    btnCalificacion.classList.remove('btn-selected');
    btnHorario.classList.remove('btn-selected');
}

// Función para mostrar la tabla correspondiente
function mostrarTabla(tablaMostrar, tablaOcultar, scrollPos) {
    tablaMostrar.style.display = 'table';
    tablaOcultar.style.display = 'none';
    ch_scroll.scrollTo({ top: scrollPos, behavior: 'smooth' });
}

// Manejador de clic para el botón de Horario
btnHorario.addEventListener('click', () => {
    deseleccionarBotones();
    btnHorario.classList.add('btn-selected');
    mostrarTabla(tablaHorario, tablaCalificacion, ch_scroll.scrollTop + 330);
});

// Manejador de clic para el botón de Calificaciones
btnCalificacion.addEventListener('click', () => {
    deseleccionarBotones();
    btnCalificacion.classList.add('btn-selected');
    mostrarTabla(tablaCalificacion, tablaHorario, 0);
});

document.addEventListener('DOMContentLoaded', () => {
    mostrarTabla(tablaCalificacion, tablaHorario, 0);
});
