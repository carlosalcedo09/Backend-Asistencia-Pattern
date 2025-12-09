let fetchInProgress = false;

function brandChanged() {
    const brandField = document.querySelector("#id_brand");
    const selectedBrand = brandField.value;
    const positionField = document.querySelector("#id_position");
    const storeField = document.querySelector("#id_store");

    const currentValue = positionField.value;
    const currentText = positionField.options[positionField.selectedIndex]?.text || "";
    
    const currentStoreValue = storeField.value;
    const currentStoreText = storeField.options[storeField.selectedIndex]?.text || "";

    // Limpiar las opciones previas
    positionField.innerHTML = "";
    storeField.innerHTML = "";



    // Añadir la opción vacía
    const emptyOption = document.createElement("option");
    emptyOption.value = "";
    emptyOption.text = "---------";
    positionField.appendChild(emptyOption);

    const emptyOptionStore = document.createElement("option");
    emptyOptionStore.value = "";
    emptyOptionStore.text = "---------";
    storeField.appendChild(emptyOptionStore);

    if (!selectedBrand || fetchInProgress) {
        return;
    }

    fetchInProgress = true;

    fetch("/api/positionbrands/by_brand/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: JSON.stringify({ brand: selectedBrand }),
    })
    .then((response) => response.json())
    .then((data) => {
        const uniquePositions = [...new Map(data.map(item => [item.id, item])).values()];
        let currentValueExists = false;

        uniquePositions.forEach((position) => {
            const option = document.createElement("option");
            option.value = position.id;
            option.text = position.name;

            if (position.id.toString() === currentValue) {
                option.selected = true;
                currentValueExists = true;
            }

            positionField.appendChild(option);
        });

        // Si el valor actual no está en las opciones, lo agregamos manualmente
        if (currentValue && !currentValueExists) {
            const currentOption = document.createElement("option");
            currentOption.value = currentValue;
            currentOption.text = currentText + " (actual)";
            currentOption.selected = true;
            positionField.appendChild(currentOption);
        }

        console.log("Opciones de posición cargadas:");
        [...positionField.options].forEach(p =>
            console.log(`ID: ${p.value}, Nombre: ${p.text}${p.selected ? " [SELECCIONADO]" : ""}`)
        );
    })
    .catch((error) => {
        console.error("Error al cargar las posiciones:", error);
    })

    fetch(`/api/store/by-brand/?brand=${selectedBrand}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
    })
    .then((response) => response.json())
    .then((data) => {
        let currentStoreExists = false;

        data.forEach((store) => {
            const option = document.createElement("option");
            option.value = store.id;
            option.text = store.name;

            if (store.id.toString() === currentStoreValue) {
                option.selected = true;
                currentStoreExists = true;
            }

            storeField.appendChild(option);
        });

        if (currentStoreValue && !currentStoreExists) {
            const currentOption = document.createElement("option");
            currentOption.value = currentStoreValue;
            currentOption.text = currentStoreText + " (actual)";
            currentOption.selected = true;
            storeField.appendChild(currentOption);
        }
    })
    .catch((error) => {
        console.error("Error al cargar las tiendas:", error);
    })
    .finally(() => {
        fetchInProgress = false;
    });
}

window.brandChanged = brandChanged;

let initialized = false;

document.addEventListener("DOMContentLoaded", function () {
    if (initialized) return;

    const brandField = document.querySelector("#id_brand");
    if (brandField) {
        brandField.removeEventListener("change", brandChanged);
        brandField.addEventListener("change", brandChanged);

        if (brandField.value) {
            brandChanged();
        }

        initialized = true;
    }
});
