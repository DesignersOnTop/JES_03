function sumarCalificaciones() {
    var filas = document.getElementsByClassName('fila-calificacion');

    for(var i = 0; i < filas.length; i++) {
        var inputs = filas[i].getElementsByTagName('input');
        var totalCalificaciones = 0;

        for(var j = 0; j < inputs.length - 1; j++) {
            var calificacion = parseFloat(inputs[j].value);
            totalCalificaciones += isNaN(calificacion) ? 0 : calificacion;
        }

        var cantidadCalificaciones = inputs.length - 1; 
        var promedioCalificaciones = totalCalificaciones / cantidadCalificaciones;
        var promedioCalificaciones = Math.round(promedioCalificaciones)

        filas[i].lastElementChild.textContent = promedioCalificaciones.toFixed(0);
    }
}