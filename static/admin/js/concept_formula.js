document.addEventListener('DOMContentLoaded', function () {
    const isCalculateCheckbox = document.querySelector('#id_is_calculate');
    const formulaField = document.querySelector('#id_formula').closest('.form-row');

    function toggleFormulaVisibility() {
        if (isCalculateCheckbox.checked) {
            formulaField.style.display = 'block';
        } else {
            formulaField.style.display = 'none';
        }
    }

    if (isCalculateCheckbox && formulaField) {
        toggleFormulaVisibility();
        isCalculateCheckbox.addEventListener('change', toggleFormulaVisibility);
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const conceptSelector = document.getElementById('concept-selector');
    const paramSelector = document.getElementById('param-selector');
    const formulaField = document.getElementById('id_formula');

    function insertAtCursor(field, value) {
        if (!field) return;
        const start = field.selectionStart;
        const end = field.selectionEnd;
        const text = field.value;

        // Insertar el texto en la posición del cursor
        field.value = text.slice(0, start) + value + text.slice(end);
        // Colocar el cursor después del texto insertado
        field.focus();
        field.selectionStart = field.selectionEnd = start + value.length;
    }

    if (conceptSelector && formulaField) {
        conceptSelector.addEventListener('change', function () {
            const val = this.value;
            if (val) {
                insertAtCursor(formulaField, val);
                this.selectedIndex = 0;  // reiniciar selección
            }
        });
    }

    if (paramSelector && formulaField) {
        paramSelector.addEventListener('change', function () {
            const val = this.value;
            if (val) {
                insertAtCursor(formulaField, val);
                this.selectedIndex = 0;
            }
        });
    }
});
