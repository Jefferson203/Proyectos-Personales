// Tu script actual para cambiar las opciones seleccionadas y mostrar el perfil
function toggleOptions() {
    const options = document.querySelector('#profile .options');
    options.classList.toggle('show');
  }
  
  function selectOption(selectedElement) {
    const listItems = document.querySelectorAll('#sidebar ul li');
    listItems.forEach(item => item.classList.remove('selected'));
    selectedElement.parentElement.classList.add('selected');
  
    const optionText = selectedElement.innerText.replace(/\s/g, '').toLowerCase();
    loadContent(optionText);
    // Guardar la opción seleccionada en localStorage
    localStorage.setItem('selectedOption', optionText);
  }
  
  // Función para cargar el contenido de otro HTML
  function loadContent(option) {
    fetch(`./templates/${option}.html`)
      .then(response => response.text())
      .then(html => {
        document.getElementById('main-content').innerHTML = html;
        // Guardar la opción y el contenido actual en localStorage
        localStorage.setItem('currentContent', html);
      })
      .catch(error => console.error('Error al cargar el contenido:', error));
  }
  
  // Evento de carga de la página
  document.addEventListener('DOMContentLoaded', () => {
    // Recuperar la opción seleccionada y el contenido actual de localStorage
    const selectedOption = localStorage.getItem('selectedOption') || 'inicio';
    const currentContent = localStorage.getItem('currentContent') || '';
  
    // Cargar el contenido de la última opción seleccionada al iniciar la página
    loadContent(selectedOption);
  
    // Restaurar la selección y el contenido actual después de cargar la página
    const listItems = document.querySelectorAll('#sidebar ul li');
    listItems.forEach(item => {
      if (item.innerText.replace(/\s/g, '').toLowerCase() === selectedOption) {
        item.classList.add('selected');
      }
    });
  });
  