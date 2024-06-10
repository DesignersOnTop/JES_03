document.addEventListener('DOMContentLoaded', () => {
    // Selección de elementos del DOM por sus IDs
    const calendarBody = document.getElementById('calendario-body');
    const monthYear = document.getElementById('mes-reciente');
    const prevMonthButton = document.getElementById('mes-anterior');
    const nextMonthButton = document.getElementById('mes-siguiente');
    const modal = document.getElementById('modal');
    const modalContent = document.querySelector('.modal-content'); // Selecciona el contenido del modal
    const modalDate = document.getElementById('modal-date');
    const noteText = document.getElementById('note-text');
    const saveNoteButton = document.getElementById('save-note');
    const deleteNoteButton = document.getElementById('delete-note');
    
    // Variables para la fecha actual y las notas
    let currentDate = new Date(); // Fecha actual
    let currentNoteDate = null; // Fecha de la nota actual
    const notes = {}; // Objeto para almacenar las notas

    // Función para renderizar el calendario
    const renderCalendar = () => {
        // Limpia el cuerpo del calendario
        calendarBody.innerHTML = '';

        // Obtiene el mes y el año actuales
        const month = currentDate.getMonth();
        const year = currentDate.getFullYear();

        // Actualiza el texto del elemento que muestra el mes y el año
        monthYear.textContent = currentDate.toLocaleDateString('es-ES', { month: 'long', year: 'numeric' });

        // Obtiene el primer día del mes y el último día del mes
        const firstDayOfMonth = new Date(year, month, 1).getDay();
        const lastDateOfMonth = new Date(year, month + 1, 0).getDate();

        let date = 1; // Inicializa la fecha en 1

        // Crea las filas del calendario (6 filas como máximo)
        for (let i = 0; i < 6; i++) {
            const row = document.createElement('tr'); // Crea una fila

            // Crea las celdas del calendario (7 columnas para los días de la semana)
            for (let j = 0; j < 7; j++) {
                const cell = document.createElement('td'); // Crea una celda

                if (i === 0 && j < firstDayOfMonth) {
                    // Si es la primera fila y el día es anterior al primer día del mes, la celda está vacía
                    cell.textContent = '';
                } else if (date > lastDateOfMonth) {
                    // Si la fecha es mayor que el último día del mes, rompe el bucle
                    break;
                } else {
                    // Asigna la fecha a la celda
                    cell.textContent = date;

                    // Crea una cadena con la fecha en formato "año-mes-día"
                    const cellDate = `${year}-${month + 1}-${date}`;
                    cell.dataset.date = cellDate; // Establece la fecha como atributo de la celda

                    const today = new Date(); // Obtiene la fecha de hoy
                    if (date === today.getDate() && year === today.getFullYear() && month === today.getMonth()) {
                        // Si la fecha es hoy, cambia el estilo de la celda
                        Object.assign(cell.style, { backgroundColor: 'transparent', color: 'green', fontWeight: 'bold' });
                    }

                    if (notes[cellDate]) {
                        // Si hay una nota para esta fecha, agrega un icono de nota a la celda
                        const noteIcon = document.createElement('span');
                        noteIcon.textContent = '📝';
                        cell.appendChild(noteIcon);
                        cell.style.backgroundColor = 'transparent';
                    }

                    // Agrega un evento de clic a la celda para abrir el modal
                    cell.addEventListener('click', () => openModal(cellDate));
                    date++; // Incrementa la fecha
                }
                row.appendChild(cell); // Agrega la celda a la fila
            }
            calendarBody.appendChild(row); // Agrega la fila al cuerpo del calendario
        }
    };

    // Función para cambiar de mes
    const changeMonth = delta => {
        currentDate.setMonth(currentDate.getMonth() + delta); // Cambia el mes de la fecha actual
        renderCalendar(); // Renderiza el calendario con el nuevo mes
    };

    // Función para abrir el modal
    const openModal = date => {
        currentNoteDate = date; // Establece la fecha de la nota actual
        modalDate.textContent = `Nota para el ${new Date(date).toLocaleDateString('es-ES')}`; // Muestra la fecha en el modal
        noteText.value = notes[date] || ''; // Muestra la nota para la fecha seleccionada (si existe)
        modal.style.display = 'block'; // Muestra el modal
    };

    // Agrega eventos de clic a los botones de cambio de mes
    prevMonthButton.addEventListener('click', () => changeMonth(-1));
    nextMonthButton.addEventListener('click', () => changeMonth(1));

    // Agrega un evento de clic al botón de guardar nota
    saveNoteButton.addEventListener('click', () => {
        notes[currentNoteDate] = noteText.value; // Guarda la nota en el objeto notes
        modal.style.display = 'none'; // Oculta el modal
        renderCalendar(); // Vuelve a renderizar el calendario
    });

    // Agrega un evento de clic al botón de eliminar nota
    deleteNoteButton.addEventListener('click', () => {
        delete notes[currentNoteDate]; // Elimina la nota del objeto notes
        noteText.value = ''; // Limpia el área de texto
        modal.style.display = 'none'; // Oculta el modal
        renderCalendar(); // Vuelve a renderizar el calendario
    });

    // Evento para cerrar el modal al hacer clic fuera del contenido del modal
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none'; // Oculta el modal
            history.back(); // Vuelve a la página anterior en el historial
        }
    });

    // Evita que el clic dentro del contenido del modal cierre el modal
    modalContent.addEventListener('click', (event) => {
        event.stopPropagation(); // Detiene la propagación del evento de clic
    });

    renderCalendar(); // Renderiza el calendario al cargar la página
});
