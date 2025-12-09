console.log("aeaa")
document.addEventListener("DOMContentLoaded", function() {
    let links = document.querySelectorAll('a');

    // Itera sobre los elementos <a>
    links.forEach(function(link) {
        // Selecciona el <span> dentro del <a>
        let span = link.querySelector('span');
    
        // Verifica si el <span> contiene el texto "visibility"
        if (span && span.textContent.trim() === 'visibility') {
            link.style.display = 'none'; // Ejemplo: Ocultar el <a>
        }
        if (span && span.textContent.trim() === 'edit') {
            link.style.display = 'none'; // Ejemplo: Ocultar el <a>
        }
        if (span && span.textContent.trim() === 'add') {
            link.style.display = 'none'; // Ejemplo: Ocultar el <a>
        }
        if (link.textContent.trim() === "Histórico") {
            link.style.display = "none";
        }

    });

    // var saveButton = document.querySelector('input[name="_save"]');

    // saveButton.addEventListener('click', function(event) {
    //     saveButton.disabled = true;
    //     saveButton.value = 'Guardando...';
    // });
});

