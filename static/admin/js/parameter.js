document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar los campos de cada fila del inline usando clases específicas de los inlines
    document.querySelectorAll('.dynamic-parameterhistory_set').forEach(function(inline) {


        // Obtener los campos value, denominator, date y type dentro de cada inline
        var typeField = inline.querySelector('[id$=type]');  // Campo type (busca por ID)
        var valueField = inline.querySelector('.field-value');  // Campo value
        var denominatorField = inline.querySelector('.field-denominator');  // Campo denominator
        var dateField = inline.querySelector('.field-date');  // Campo date

        // Función para alternar los campos según el tipo seleccionado
        function toggleFields() {
            var selectedType = typeField.value;

            if (selectedType === 'decimal') {
                valueField.style.display = 'block';
                denominatorField.style.display = 'block';
                dateField.style.display = 'none';
            } else if (selectedType === 'fecha') {
                valueField.style.display = 'none';
                denominatorField.style.display = 'none';
                dateField.style.display = 'block';
            }
        }

        // Ejecutar la función cuando se carga la página por primera vez
        toggleFields();

        // Escuchar cambios en el campo type dentro del inline
        typeField.addEventListener('change', toggleFields);
    });
});
