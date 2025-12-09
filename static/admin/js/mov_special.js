document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar el checkbox
    var isSpecialMovCheckbox = document.getElementById('id_is_special_mov');

    // Seleccionar los campos que queremos mostrar/ocultar
    var specialMovementField = document.getElementById('id_special_movement').closest('.form-row');
    var vacationPayField = document.getElementById('id_vacation_pay').closest('.form-row');
    var policeDismissedField = document.getElementById('id_police_dismissed').closest('.form-row');
    var policeDismissedChildrenField = document.getElementById('id_police_dismissed_children').closest('.form-row'); 
    var greatGraceField = document.getElementById('id_great_grace').closest('.form-row');

    // Seleccionar los otros campos que queremos ocultar cuando el checkbox esté marcado
    var employeeField = document.getElementById('id_employee').closest('.form-row');
    var managementField = document.getElementById('id_management').closest('.form-row');
    var positionField = document.getElementById('id_position').closest('.form-row');
    var sedeField = document.getElementById('id_sede').closest('.form-row');
    var basicSalaryField = document.getElementById('id_basic_salary').closest('.form-row');
    var afpIncreaseField = document.getElementById('id_afp_increase').closest('.form-row');
    var grantField = document.getElementById('id_grant').closest('.form-row');
    var familyAllowanceField = document.getElementById('id_family_allowance').closest('.form-row');
    var haveChildrenField = document.getElementById('id_have_children').closest('.form-row');
    var haveBonusField = document.getElementById('id_have_bonus').closest('.form-row');
    var targetBonusField = document.getElementById('id_target_bonus').closest('.form-row');
    var haveCommissionField = document.getElementById('id_have_commission').closest('.form-row');
    var epsField = document.getElementById('id_eps').closest('.form-row');
    var sctrField = document.getElementById('id_sctr').closest('.form-row');
    var housingAllocationField = document.getElementById('id_housing_allocation').closest('.form-row');
    var commissionField = document.getElementById('id_commission').closest('.form-row');
    var mobilityField = document.getElementById('id_mobility').closest('.form-row');
    var overtimeField = document.getElementById('id_overtime').closest('.form-row');
    var longTermBonusField = document.getElementById('id_long_term_bonus').closest('.form-row');
    var medicField = document.getElementById('id_medic').closest('.form-row');
    var epsChildrenField = document.getElementById('id_eps_children').closest('.form-row');
    var epsRateField = document.getElementById('id_eps_rate').closest('.form-row');
    var severancePayField = document.getElementById('id_severance_pay').closest('.form-row');

    function toggleFields() {
        if (isSpecialMovCheckbox.checked) {
            specialMovementField.style.display = 'block';
            vacationPayField.style.display = 'block';
            policeDismissedField.style.display = 'block';
            policeDismissedChildrenField.style.display = 'block';
            greatGraceField.style.display='block';
            employeeField.style.display = 'none';
            managementField.style.display = 'none';
            positionField.style.display = 'none';
            sedeField.style.display = 'none';
            basicSalaryField.style.display = 'none';
            afpIncreaseField.style.display = 'none';
            grantField.style.display = 'none';
            familyAllowanceField.style.display = 'none';
            haveChildrenField.style.display = 'none';
            haveBonusField.style.display = 'none';
            targetBonusField.style.display = 'none';
            haveCommissionField.style.display = 'none';
            epsField.style.display = 'none';
            sctrField.style.display = 'none';
            housingAllocationField.style.display = 'none';
            commissionField.style.display = 'none';
            mobilityField.style.display = 'none';
            overtimeField.style.display = 'none';
            longTermBonusField.style.display = 'none';
            medicField.style.display = 'none';
            epsChildrenField.style.display = 'none';
            epsRateField.style.display = 'none';
        } else {
            specialMovementField.style.display = 'none';
            vacationPayField.style.display = 'none';
            policeDismissedField.style.display = 'none';
            policeDismissedChildrenField.style.display = 'none';
            greatGraceField.style.display='none';
            employeeField.style.display = 'block';
            managementField.style.display = 'block';
            positionField.style.display = 'block';
            sedeField.style.display = 'block';
            basicSalaryField.style.display = 'block';
            afpIncreaseField.style.display = 'block';
            grantField.style.display = 'block';
            familyAllowanceField.style.display = 'block';
            haveChildrenField.style.display = 'block';
            haveBonusField.style.display = 'block';
            targetBonusField.style.display = 'block';
            haveCommissionField.style.display = 'block';
            epsField.style.display = 'block';
            sctrField.style.display = 'block';
            housingAllocationField.style.display = 'block';
            commissionField.style.display = 'block';
            mobilityField.style.display = 'block';
            overtimeField.style.display = 'block';
            longTermBonusField.style.display = 'block';
            medicField.style.display = 'block';
            epsChildrenField.style.display = 'block';
            epsRateField.style.display = 'block';
        }
    }

    toggleFields();

    isSpecialMovCheckbox.addEventListener('change', function() {
        toggleFields();
    });
});
