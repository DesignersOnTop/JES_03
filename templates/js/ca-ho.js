// Selecciona todos los botones con las clases 'btn-calificaciones' y 'btn-horario'
const botones = document.querySelectorAll('.btn-calificaciones, .btn-horario');
const scrollContainer = document.querySelector('.ca-ho-scroll'); // Selecciona el contenedor que se desplazará
const botonesContainer = document.querySelector('.botones-container'); // Selecciona el contenedor con la clase 'botones-container'

// Función para deseleccionar todos los botones
function deseleccionarBotones() {
    // Remueve la clase 'btn-selected' de cada botón en la lista 'botones'
    botones.forEach(boton => boton.classList.remove('btn-selected'));
}

// Función para manejar el clic en los botones
function manejarClick(event) {
    const boton = event.target; // Obtiene el botón que fue clickeado
    // Determina la dirección del desplazamiento basado en la clase del botón
    const desplazamiento = boton.classList.contains('btn-calificaciones') ? -966 : 966;
    
    // Desplaza el contenedor en la dirección determinada
    scrollContainer.scrollLeft += desplazamiento;
    deseleccionarBotones(); // Deselecciona todos los botones
    boton.classList.add('btn-selected'); // Selecciona (añade la clase) el botón clickeado

    // Si se hizo clic en un botón de horario, oculta el contenedor 'botones-container'
    if (boton.classList.contains('btn-horario')) {
        botonesContainer.style.display = 'none';
    } else {
        botonesContainer.style.display = 'flex';
    }
}

// Añade el evento 'click' a cada botón en la lista 'botones'
botones.forEach(boton => {
    boton.addEventListener('click', manejarClick);
});
