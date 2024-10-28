function loadContent(section, element) {
  // Cargar el contenido con AJAX
  fetch(`/content/${section}`)
      .then(response => response.text())
      .then(html => {
          // Colocar el contenido en el contenedor principal
          document.getElementById('main-content').innerHTML = html;
          
          // Guardar el contenido cargado y el id del elemento seleccionado en localStorage
          localStorage.setItem('loadedContent', html);
          localStorage.setItem('selectedSection', section); // Guardamos la sección actual
          localStorage.setItem('selectedOption', element.id); // Guardamos la opción seleccionada
          
          // Resaltar la opción seleccionada
          highlightSelectedOption();
      })
      .catch(error => {
          console.error('Error al cargar el contenido:', error);
          document.getElementById('main-content').innerHTML = '<p>Error al cargar el contenido.</p>';
      });
}

function highlightSelectedOption() {
  // Obtener el id de la opción seleccionada desde localStorage
  const selectedId = localStorage.getItem('selectedOption');
  
  // Remover la clase "selected" de todos los enlaces del menú
  document.querySelectorAll('#sidebar ul li a').forEach(link => {
      link.classList.remove('selected');
  });

  // Si hay una opción seleccionada en localStorage, añadirle la clase "selected"
  if (selectedId) {
      const selectedElement = document.getElementById(selectedId);
      if (selectedElement) {
          selectedElement.classList.add('selected');
      }
  }
}


window.onload = function() {
  // Restaurar la opción seleccionada
  highlightSelectedOption();

  // Verificar si hay contenido previamente cargado en localStorage
  const savedContent = localStorage.getItem('loadedContent');
  const savedSection = localStorage.getItem('selectedSection');
  
  if (savedContent && savedSection) {
      // Si hay contenido guardado, lo restauramos en el contenedor principal
      document.getElementById('main-content').innerHTML = savedContent;
  } else {
      // Si no hay nada en localStorage, cargar la página de inicio o una predeterminada
      loadContent('inicio', document.getElementById('inicio'));
  }

  const selectedItem = localStorage.getItem('selectedMenuItem');
  if (selectedItem) {
      document.querySelector(`#sidebar ul li[data-id="${selectedItem}"]`).classList.add('selected');
  }
};

function clearLocalStorage() {
  localStorage.removeItem('loadedContent');
  localStorage.removeItem('selectedOption');
  localStorage.removeItem('selectedSection');
}


document.querySelectorAll('#sidebar ul li').forEach(function(item) {
  item.addEventListener('click', function() {
      // Remover la clase 'selected' de todos los elementos
      document.querySelectorAll('#sidebar ul li').forEach(function(el) {
          el.classList.remove('selected');
      });
      // Agregar la clase 'selected' al elemento que fue clicado
      item.classList.add('selected');

      // Almacenar el id del elemento seleccionado en localStorage
      localStorage.setItem('selectedMenuItem', item.dataset.id);
  });
});

function toggleOptions() {
  const options = document.querySelector('.options');
  if (options.style.display === 'none' || options.style.display === '') {
      options.style.display = 'block'; // Mostrar opciones
  } else {
      options.style.display = 'none'; // Ocultar opciones
  }
}

function selectOption(element) {
  const selectedOption = element.innerText;
  console.log('Opción seleccionada:', selectedOption);
  // Aquí puedes agregar la lógica adicional que necesites al seleccionar una opción.
}