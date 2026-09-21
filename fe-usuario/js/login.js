document.addEventListener('DOMContentLoaded', () => {
    const formulario = document.querySelector('#formulario');

    if (formulario) {
        formulario.addEventListener('submit', validarLogin);
    }
});

async function validarLogin(e) {
    e.preventDefault();

    const email = document.querySelector('#email').value.trim();
    const password = document.querySelector('#password').value.trim();

    if (email === '' || password === '') {
        mostrarAlerta('Todos los campos son obligatorios');
        return;
    }

    try {
        // Apunta al endpoint de Flask definido en app.py
        const url = 'http://localhost:5000/login';

        const respuesta = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const resultado = await respuesta.json();

        if (!respuesta.ok) {
            mostrarAlerta(resultado.error || 'Error al iniciar sesión');
            return;
        }

        // Guardar la información del usuario devuelta por el servidor
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
    formulario.appendChild(alerta);

    setTimeout(() => {
        alerta.remove();
    }, 3000);
}