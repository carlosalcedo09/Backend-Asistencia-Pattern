document.addEventListener('DOMContentLoaded', function() {
    const searchField = document.querySelector('input[name="q"]');
    if (searchField) {
        searchField.setAttribute('placeholder', 'Escribe para buscar ...'); 
    }
  
    document.getElementById('import-toggle').addEventListener('click', function() {
      var importForm = document.getElementById('import-form');
      var exportForm = document.getElementById('export-form');
      importForm.style.display = (importForm.style.display === 'none' || importForm.style.display === '') ? 'block' : 'none';
      exportForm.style.display = 'none'; 
    });
  
    document.getElementById('export-toggle').addEventListener('click', function() {
      var exportForm = document.getElementById('export-form');
      var importForm = document.getElementById('import-form');
      exportForm.style.display = (exportForm.style.display === 'none' || exportForm.style.display === '') ? 'block' : 'none';
      importForm.style.display = 'none'; 
    });
  });
  