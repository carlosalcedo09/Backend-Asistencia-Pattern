window.onload = function() {
    console.log("aea")
    const labels = document.querySelectorAll('.grp h2, .grp p');

    labels.forEach(function(label) {
        label.textContent = label.textContent
            .replace('Can add', 'Puede agregar')
            .replace('Can change', 'Puede editar')
            .replace('Can delete', 'Puede eliminar')
            .replace('Can view', 'Puede ver');
    });
};