$(document).ready(function () {
    $('.generate-payroll-btn').on('click', function () {
        const id = $(this).data('id');
        $('#confirm-payroll-btn').data('id', id);

        $.ajax({
            url: '/api/payroll/payroll_preview/?payroll=' + id,
            method: 'GET',
            success: function (data) {
                // Cabecera del modal
                $('#modal-content').html(`
                    <p><strong>${data.description}</strong> | Año: ${data.year} - Mes: ${data.month}</p>
                    <p>Total: ${formatDecimal(data.total)}</p>
                `);

                // Cabecera de la tabla
                let headerHtml = `
                    <tr>
                        <th>ID</th>
                        <th>DNI - Empleado</th>
                        <th>Área</th>
                        <th>Cargo</th>
                        <th>Fecha de ingreso</th>
                `;

                $.each(data.header_concepts, function (i, concept) {
                    headerHtml += `<th>${concept}</th>`;
                });

                headerHtml += '</tr>';
                $('#table-budget thead').html(headerHtml);

                // Cuerpo de la tabla
                let bodyHtml = '';

                $.each(data.employees, function (index, emp) {
                    bodyHtml += `
                        <tr>
                            <td>${index + 1}</td>
                            <td>${emp.employee_doc} - ${emp.employee_name}</td>
                            <td>${emp.area}</td>
                            <td>${emp.position}</td>
                            <td>${emp.employee_entry}</td>
                    `;

                    $.each(emp.concepts, function (j, concept) {
                        bodyHtml += `<td>${formatDecimal(concept.value)}</td>`;
                    });

                    bodyHtml += '</tr>';
                });

                $('#table-budget tbody').html(bodyHtml);

                // Carga el ID en botones si lo necesitas luego
                $('#save-budget-btn').data('id', id);

                // Mostrar el modal
                $('#budgetModal').modal('show');
            },
            error: function () {
                alert('Error al obtener los datos del presupuesto.');
            }
        });
    });
});

// Función para formato numérico con separador de miles
function formatDecimal(value) {
    if (value === null || value === undefined) return '';
    return parseFloat(value).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}


$(document).ready(function () {
    $('#confirm-payroll-btn').on('click', function () {
        const id = $(this).data('id');
        
        if (!id) {
            alert("No se encontró el ID de la nómina.");
            return;
        }

        $.ajax({
            url: `/admin/payroll/payroll/${id}/payroll/`,
            method: 'GET',
            success: function () {
                alert("Nómina aprobada exitosamente");
                location.reload(); 
            },
            error: function () {
                alert("Error al aprobar la nómina");
            }
        });
    });
});