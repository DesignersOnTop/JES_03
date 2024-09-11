document.getElementById('subir-tarea').addEventListener('change', function() {
    var archivo = this.files[0];
    var tipoArchivo = archivo.type;

    if (tipoArchivo === 'application/pdf') {
        // Si es un PDF, mostramos un enlace para descargarlo
        document.getElementById('previsualizacion').innerHTML = '<a href="' + URL.createObjectURL(archivo) + '" target="_blank">Ver PDF</a>';
    } else {
        // Si no es ni imagen ni PDF, mostramos un mensaje de error
        document.getElementById('previsualizacion').innerHTML = '<p>No se puede previsualizar este tipo de archivo.</p>';
    }
});