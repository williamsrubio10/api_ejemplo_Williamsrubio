console.log('¡JS CARGADO CORRECTAMENTE!');

document.addEventListener('DOMContentLoaded', () => {
    const formulario = document.querySelector('#formulario');

    if (formulario) {
        formulario.addEventListener('submit', validarLogin);
    }
});

async function validarLogin(e) {
    e.preventDefault();

    // ID exactamente como está en tu HTML: #usuario y #password
    const usuarioInput = document.querySelector('#usuario');
    const passwordInput = document.querySelector('#password');

    const usuario = usuarioInput ? usuarioInput.value.trim() : '';
    const password = passwordInput ? passwordInput.value.trim() : '';

    if (usuario === '' || password === '') {
        mostrarAlerta('Todos los campos son obligatorios');
        return;
    }

    try {
        const url = 'https://apiejemplowilliamsrubio-production.up.railway.app/usuario/login';

        const respuesta = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ usuario, password })
        });

        const resultado = await respuesta.json();

        if (!respuesta.ok || !resultado.exito) {
            mostrarAlerta(resultado.mensaje || 'Error al iniciar sesión');
            return;
        }

        // Guardar la información del usuario en el navegador
        localStorage.setItem('usuario', JSON.stringify(resultado.usuario));

        // Redirigir a la vista principal
        window.location.href = 'index.html';

    } catch (error) {
        console.error('Error de conexión:', error);
        mostrarAlerta('No se pudo conectar con el servidor');
    }
}

function mostrarAlerta(mensaje) {
    const alertaPrevia = document.querySelector('.alerta-error');
    if (alertaPrevia) alertaPrevia.remove();

    const alerta = document.createElement('div');
    alerta.className = 'alerta-error bg-red-100 border-l-4 border-red-500 text-red-700 p-4 my-4 rounded';
    alerta.textContent = mensaje;

    const formulario = document.querySelector('#formulario');
    if (formulario) {
        formulario.appendChild(alerta);
    }

    setTimeout(() => {
        alerta.remove();
    }, 3000);
}