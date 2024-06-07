const rows = document.querySelectorAll('.tabla-asistencia tr');

// Función para actualizar el total de asistencias
function updateTotal() {
    rows.forEach(row => {
        const inputs = row.querySelectorAll('.input-row'); // Obtiene los inputs de la fila
        let total = 0;

        // Suma los valores de los inputs en la fila
        inputs.forEach(input => {
            total += parseInt(input.value) || 0; // Si el valor no es un número, se toma como 0
        });

        // Divide el total por 5 y lo asigna al input de la última celda de la fila
        const totalInput = row.querySelector('.total-row');
        totalInput.value = total / 5;
    });
}

// Asigna el evento input a todos los inputs
const inputFields = document.querySelectorAll('.input-row input');
inputFields.forEach(input => {
    input.addEventListener('input', updateTotal);
});