
console.log('¡jJS cargado correctamente!');

document.addEventListener('DOMContentLoaded', () => {
    const formulario = document.querySelector('#formulario');

    if (formulario) {
        formulario.addEventListener('submit', validarLogin);
    } else {
        console.error('No se encontró el elemento #formulario');
    }
});

async function validarLogin(e) {
    // Evita que el formulario recargue la página
    e.preventDefault();
    console.log('Intento de submit capturado');

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
        console.log('Enviando datos a:', url);

        const respuesta = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ usuario, password })
        });

        console.log('Estatus de la respuesta HTTP:', respuesta.status);

        const resultado = await respuesta.json();
        console.log('Respuesta del servidor:', resultado);

        if (!respuesta.ok || !resultado.exito) {
            mostrarAlerta(resultado.mensaje || 'Error al iniciar sesión');
            return;
        }

        // Guardar sesión y redirigir
        localStorage.setItem('usuario', JSON.stringify(resultado.usuario));
        window.location.href = 'index.html';

    } catch (error) {
        console.error('Error de red o conexión:', error);
        mostrarAlerta('No se pudo conectar con el servidor. Revisa la consola.');
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
    }, 4000);
}