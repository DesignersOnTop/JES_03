document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById("agregarProfesorModal");
    const btn = document.getElementById("agg-profesor-btn");
    const span = document.getElementsByClassName("close")[0];
    const searchBtn = document.getElementById("searchBtn");
    const profesorList = document.getElementById("profesorList");
  
    // Abrir el modal
    btn.onclick = function() {
      modal.style.display = "block";
    }
  
    // Cerrar el modal
    span.onclick = function() {
      modal.style.display = "none";
    }
  
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }
  
    document.getElementById('searchBtn').addEventListener('click', function() {
      let searchOption = document.querySelector('input[name="searchOption"]:checked').value;
      let searchInput = document.getElementById('searchInput').value;
  
      fetch(`/admin/buscarProfesores?option=${searchOption}&query=${searchInput}`)
          .then(response => response.json())
          .then(data => {
              let profesorList = document.getElementById('profesorList');
              profesorList.innerHTML = '';
              data.forEach(profesor => {
                  profesorList.innerHTML += `
                      <div class="profesor-item">
                          <p>${profesor.nombre} ${profesor.apellido}</p>
                          <select>
                            {% for curso in cursos %}
                            <option value="{{ curso.id_curso }}">{{ curso.nombre }}</option>
                            {% endfor %}
                          </select>
                      </div>
                  `;
              });
          });
  });

  function selectProfesor(id_profesor) {
    // Mostrar el formulario de asignación
    let assignmentForm = document.getElementById('assignmentForm');
    assignmentForm.style.display = 'block';

    // Configurar el ID del profesor seleccionado
    document.getElementById('selectedProfesorId').value = id_profesor;

    // Obtener la lista de cursos y mostrarla en el formulario
    fetch('/admin/getCursos')
        .then(response => response.json())
        .then(data => {
            let cursosSelect = document.getElementById('cursosSelect');
            cursosSelect.innerHTML = '';
            data.forEach(curso => {
                cursosSelect.innerHTML += `<option value="${curso.id_curso}">${curso.nombre}</option>`;
            });
        });
}

document.getElementById('assignmentForm').addEventListener('submit', function(event) {
    event.preventDefault();
    let id_profesor = document.getElementById('selectedProfesorId').value;
    let id_curso = document.getElementById('cursosSelect').value;

    fetch('/admin/asignarProfesor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id_profesor: id_profesor,
            id_curso: id_curso
        })
    })
    .then(response => response.json())
    .then(data => {
        alert('Profesor asignado correctamente');
        document.getElementById('assignmentForm').reset();
        document.getElementById('assignmentForm').style.display = 'none';
    });
});
});
  