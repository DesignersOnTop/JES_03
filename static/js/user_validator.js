function usuario() {
    let user = document.getElementById("id").value;
    let password = document.getElementById("password").value;

    if (user === "" || password === "") {
        Swal.fire({
            html: '<span class="white">"Por favor, completa todos los campos."</span>',
            backdrop: true,
            customClass: {
                popup: 'emergente-class',
                confirmButton: 'confirm-eme',
                container: 'container-eme'
            },
            buttonsStyling: false,
            showCloseButton: false,
            allowOutsideClick: false,
            confirmButtonText: "Aceptar",
            imageUrl: '/static/imagenes/recursos/logo-jes.png',
            imageWidth: '140px',
            imageHeight: '120px'
        });
        return false; // Evita el envío del formulario
    }

    return true; // Permitir el envío del formulario
}

function showErrorAlert() {
    Swal.fire({
        html: '<span class="white">"Verifique que la matrícula y la contraseña son correctos e intente nuevamente."</span>',
        backdrop: true,
        customClass: {
            popup: 'emergente-class',
            confirmButton: 'confirm-eme',
            container: 'container-eme'
        },
        buttonsStyling: false,
        showCloseButton: false,
        allowOutsideClick: false,
        confirmButtonText: "Aceptar",
        imageUrl: '/static/imagenes/recursos/logo-jes.png',
        imageWidth: '140px',
        imageHeight: '120px'
    });
}
