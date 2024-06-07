function calcularAsistencia() {
    var table = document.querySelector('.tabla-asistencia');
    var rows = table.getElementsByTagName('tr');

    for (var i = 1; i < rows.length; i++) {
        var inputs = rows[i].getElementsByTagName('input');
        var totalAsistencias = 0;

        for (var j = 0; j < inputs.length; j++) {
            var porcentaje = parseInt(inputs[j].value);
            if (!isNaN(porcentaje)) {
                totalAsistencias += porcentaje;
            }
        }

        // Calcular porcentaje de asistencia
        var porcentajeAsistencia = (totalAsistencias / (inputs.length - 1)).toFixed(2);

        // Agregar el total de asistencias y porcentaje de asistencia a la fila actual
        var totalAsistenciasCell = rows[i].getElementsByTagName('td')[8];
        var porcentajeAsistenciaCell = rows[i].getElementsByTagName('td')[9];

        // Llenar el atributo value si está vacío
        if (totalAsistenciasCell.getElementsByTagName('input')[0].value === "") {
            totalAsistenciasCell.getElementsByTagName('input')[0].value = totalAsistencias + '%';
        }

        if (porcentajeAsistenciaCell.getElementsByTagName('input')[0].value === "") {
            porcentajeAsistenciaCell.getElementsByTagName('input')[0].value = porcentajeAsistencia + '%';
        }
    }
}

// Llamar a la función al cargar la página
window.onload = function() {
    calcularAsistencia();
};