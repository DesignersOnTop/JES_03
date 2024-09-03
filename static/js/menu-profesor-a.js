const menu = document.querySelector('.menu');

menu.addEventListener('click',() => {
    Swal.fire({
        html: '<nav><ul class="ul-eme"><li class="li-eme"><a href="/profesor/perfil" class="a-eme home-eme">Perfil</a></li><li class="li-eme"><a href="/home/profesor/" class="a-eme home-eme">Home</a></li><li class="li-eme"><a href="/profesor/refuerzo/libros/" class="a-eme home-eme">Refuerzo de clase</a></li><li class="li-eme"><a href="/profesor/materiales/" class="a-eme home-eme">Material de estudio</a></li><li class="li-eme"><a href="/cerrar/session/" class="a-eme cerrar-eme">Cerrar Sesion</a></li></ul></nav>',
        backdrop: true,
        customClass: {
            popup: 'emergente-class classes-eme',
            confirmButton: 'confirm-eme',
            container: 'container-eme conta-eme',
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