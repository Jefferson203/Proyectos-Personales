document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault();
    // Aquí puedes agregar lógica para manejar el inicio de sesión
    // Por ejemplo, enviar datos a un servidor, validar credenciales, etc.
    alert('Iniciando sesión...');
  });

  document.getElementById('forgotPassword').addEventListener('click', function (event) {
    event.preventDefault();
    // Aquí puedes agregar lógica para manejar la recuperación de contraseña
    // Por ejemplo, abrir un modal con un formulario para ingresar el correo, etc.
    alert('Recuperar contraseña...');
  });

  // Script para mostrar/ocultar la contraseña
  document.getElementById('togglePassword').addEventListener('click', function () {
    var passwordInput = document.getElementById('password');
    var icon = document.getElementById('togglePassword');

    if (passwordInput.type === 'password') {
      passwordInput.type = 'text';
      icon.classList.remove('fa-eye-slash');
      icon.classList.add('fa-eye');
    } else {
      passwordInput.type = 'password';
      icon.classList.remove('fa-eye');
      icon.classList.add('fa-eye-slash');
    }
  });