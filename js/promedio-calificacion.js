function sumarCalificaciones() {
        var filas = document.getElementsByClassName('fila-calificacion');
        
        for(var i = 0; i < filas.length; i++) {
            var inputs = filas[i].getElementsByTagName('input');
            var totalCalificaciones = 0;
            
            for(var j = 0; j < inputs.length; j++) {
                var calificacion = parseFloat(inputs[j].value);
                totalCalificaciones += isNaN(calificacion) ? 0 : calificacion;
            }
            
            filas[i].lastElementChild.textContent = totalCalificaciones;
        }
    }