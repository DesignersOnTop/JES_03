// Selecciona todos los elementos con la clase 'btn-calificaciones' y 'btn-horario'
let botonesCalificaciones = document.getElementsByClassName('btn-calificaciones');
let botonesHorario = document.getElementsByClassName('btn-horario');
let scroll_calificaciones = document.getElementsByClassName('botones-container');

// Función para deseleccionar todos los botones
function deseleccionarBotones() {
    Array.from(botonesCalificaciones).forEach(boton => boton.classList.remove('btn-selected'));
    Array.from(botonesHorario).forEach(boton => boton.classList.remove('btn-selected'));
}

// Añade el evento 'click' a cada botón de calificaciones
Array.from(botonesCalificaciones).forEach((boton) => {
    boton.addEventListener('click', () => {
        document.querySelector('.ca-ho-scroll').scrollLeft -= 966;
        deseleccionarBotones(); // Deselecciona todos los botones
        boton.classList.add('btn-selected'); // Selecciona el botón actual
        scroll_calificaciones[0].style.display = 'flex'; // display flex para que se muestre
    });
});

// Añade el evento 'click' a cada botón de horario
Array.from(botonesHorario).forEach((boton) => {
    boton.addEventListener('click', () => {
        document.querySelector('.ca-ho-scroll').scrollLeft += 966;
        deseleccionarBotones(); // Deselecciona todos los botones
        boton.classList.add('btn-selected'); // Selecciona el botón actual
        scroll_calificaciones[0].style.display = 'none'; //display none para ocultar
    });
});
