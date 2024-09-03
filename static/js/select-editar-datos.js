function updateAsignaturaId() {
    var select = document.getElementById("nombre_asignatura");
    var selectedOption = select.options[select.selectedIndex];
    var idAsignatura = selectedOption.value;

    // Actualiza el campo oculto con el id_asignatura seleccionado
    document.getElementById("id_asignatura").value = idAsignatura;
}

function updateCursoId() {
    var select = document.getElementById("nombre_curso");
    var selectedOption = select.options[select.selectedIndex];
    var idCurso = selectedOption.value;
    
    // Actualiza el campo oculto con el id_curso seleccionado
    document.getElementById("id_curso").value = idCurso;
}