const menu = document.querySelector('.menu');

menu.addEventListener('click',() => {
    Swal.fire({
        html: '<nav><ul class="ul-eme"><li class="li-eme"><a href="../estudiante/e-perfil.html" class="a-eme">Perfil</a></li><li class="li-eme"><a href="e-refuerzo-libros.html" class="a-eme home-eme">Refuerzo de curso</a></li><li class="li-eme"><a href="e-material_estudio.html" class="a-eme material-eme">Material de tareas</a></li><li class="li-eme"><a href="../index.html" class="a-eme cerrar-eme">Cerrar Sesion</a></li></ul></nav>',
        backdrop: true,
        customClass: {
            popup: 'emergente-class classes-eme',
            confirmButton: 'confirm-eme',
            container: 'container-eme conta-eme'
        },
        imageUrl: '../imagenes/recursos/logo-jes.png',
        imageWidth: '100px',
        imageHeight: '100px',
        imageAlt: 'Logo-JES',
        buttonsStyling: false,
        showCloseButton: false,
        // closeButtonAriaLabel: "cerrar",
        allowOutsideClick: true,
        confirmButtonText: "Aceptar",
        showConfirmButton: false,
        position: 'top-right',
        // grow: 'column'
    });
});