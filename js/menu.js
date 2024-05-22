const menu = document.querySelector('.menu');

menu.addEventListener('click',() => {
    Swal.fire({
        html: '<ul><li><a href="#" class="a-eme report-eme">Reporte</a></li><li><a href="#" class="a-eme conf-eme">Configuraci&oacute;n</a></li><li><a href="index.html" class="a-eme cerrar-eme">Cerrar Sesion</a></li></ul>',
        backdrop: true,
        customClass: {
            popup: 'emergente-class classes-eme',
            confirmButton: 'confirm-eme',
            container: 'container-eme conta-eme'
        },
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