document.addEventListener('DOMContentLoaded', function() {
    const searchField = document.querySelector('input[name="q"]');
    if (searchField) {
        searchField.setAttribute('placeholder', 'Escribe para buscar ...'); 
    }
    });
  