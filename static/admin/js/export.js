function exportBudget(budgetId) {
    $.ajax({
        url: `/admin/payrolls/budget/${budgetId}/export/`,
        type: 'GET',
        success: function(response) {
            alert('Exportación exitosa');
        },
        error: function(xhr, status, error) {
            alert('Error en la exportación');
        }
    });
}
