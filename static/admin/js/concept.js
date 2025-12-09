$(document).ready(function() {

    $('#id_concept').change(function() {
        var selectedValue = $(this).val();
        var formulaField = $('#id_formula');

        if (selectedValue) {
            $.ajax({
                url: '/api/concepts/concepts/?id=' + selectedValue,
                method: 'GET',
                dataType: 'json',
                success: function(data) {
                    var currentValue = formulaField.val();
                    formulaField.val(currentValue + "{{" + data.code + "}}"); 
                    $('#id_concept').val('');
                },
                error: function(xhr, status, error) {
                    console.error('Error en la solicitud AJAX:', error);
                }
                
            });
        } else {
            formulaField.val('');
        }
    });

    $('#id_parameter').change(function() {
        var selectedValue = $(this).val();
        var formulaField = $('#id_formula');

        if (selectedValue) {
            $.ajax({
                url: '/api/concepts/parameters/?id=' + selectedValue,
                method: 'GET',
                dataType: 'json',
                success: function(data) {
                    var currentValue = formulaField.val();
                    formulaField.val(currentValue + "{{" + data.code + "}}");
                    $('#id_parameter').val('');
                },
                error: function(xhr, status, error) {
                    console.error('Error en la solicitud AJAX:', error);
                }
            });
        } else {
            formulaField.val('');
        }
    });

    $('#id_extra').change(function() {
        var selectedValue = $(this).val();  // Obtiene el valor seleccionado
        var formulaField = $('#id_formula'); // El campo de texto donde colocaremos el resultado

        // Verifica si hay un valor seleccionado
        if (selectedValue) {

            var currentValue = formulaField.val();
            formulaField.val(currentValue + "{{" + selectedValue + "}}");
            $('#id_extra').val('');

        } else {
            formulaField.val('');
        }
    });
});