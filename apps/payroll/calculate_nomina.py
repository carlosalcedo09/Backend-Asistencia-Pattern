
from apps.payroll.models import PayrollEmployee, PayrrollEmployeeDetail
from apps.attendance.models import AttendanceMarking, Attendance
from apps.maintenance.models import Concept,ParameterHistory
from datetime import datetime, timedelta,date
from apps.employees.models import Employee
from django.db import transaction
from django.db.models import Q
import calendar
import re
from decimal import Decimal


def nombre_mes_a_numero(nombre_mes):
    meses = {
        "ENERO": 1,
        "FEBRERO": 2,
        "MARZO": 3,
        "ABRIL": 4,
        "MAYO": 5,
        "JUNIO": 6,
        "JULIO": 7,
        "AGOSTO": 8,
        "SETIEMBRE": 9,
        "SEPTIEMBRE": 9, 
        "OCTUBRE": 10,
        "NOVIEMBRE": 11,
        "DICIEMBRE": 12,
    }

    nombre_mes = nombre_mes.upper().strip()
    return meses.get(nombre_mes)

def to_decimal(valor):
    return valor if isinstance(valor, Decimal) else Decimal(str(valor))


def calculate_employee_data(month, year, employee):
    primer_dia = date(year, month, 1)
    _, dias_del_mes = calendar.monthrange(year, month)
    ultimo_dia = date(year, month, dias_del_mes)
    hoy = date.today()

    mes_actual = (month == hoy.month and year == hoy.year)

    fecha_limite = min(ultimo_dia, hoy) if mes_actual else ultimo_dia

    asistencias = Attendance.objects.filter(
        employee=employee,
        date__range=(primer_dia, fecha_limite)
    )

    total_horas = sum(a.hours_worked for a in asistencias)
    total_horas_extra = sum(a.overtime for a in asistencias)
    fechas_asistidas = set(a.date for a in asistencias)

    dias_trabajados = len(fechas_asistidas)
    faltas = 0
    sabados_extra = 0

    dia_actual = primer_dia
    while dia_actual <= fecha_limite:
        if dia_actual.weekday() < 6: 
            if dia_actual not in fechas_asistidas:
                if dia_actual.weekday() == 5:
                    sabados_extra += 1
                else:
                    faltas += 1
        dia_actual += timedelta(days=1)

    if dias_trabajados > 0:
        dias_trabajados += sabados_extra

    if mes_actual:
        dias_restantes = (ultimo_dia - hoy).days
    else:
        dias_restantes = 0

    return total_horas, dias_trabajados, faltas, total_horas_extra, dias_restantes

def evaluar_formula(formula, variables):

    def reemplazo(match):
        clave = match.group(1).strip()
        return str(variables.get(clave, 0))  

    formula_eval = re.sub(r'\[([^\]]+)\]', reemplazo, formula)
    print(formula_eval)

    try:
        resultado = eval(formula_eval, {}, {})  
        return round(float(resultado), 2)
    except Exception as e:
        print(f"Error evaluando fórmula '{formula}': {e}")
        return 0

def obtener_variables_para_empleado(empleado, payroll_employee, conceptos_dict, parametros_dict):
    variables = {}

    for nombre, monto in conceptos_dict.items():
        variables[nombre.upper()] = monto

    for nombre, valor in parametros_dict.items():
        variables[nombre] = valor

    variables["DIAS TRABAJADOS"] = payroll_employee.days_worked
    variables["HORAS TRABAJADAS"] = payroll_employee.total_hours
    variables["SUELDO BASICO"] = empleado.position.base_salary
    print(variables)

    return variables

def generate_payroll_data(payroll):
    anio_actual = str(datetime.now().year)
    month = nombre_mes_a_numero(payroll.month)
    year = int(payroll.year)

    conceptos_vigentes = Concept.objects.filter(
        start_validity__lte=anio_actual,
        end_validity__gte=anio_actual
    )

    parametros_vigentes = ParameterHistory.objects.filter(
        start_validity__lte=anio_actual,
        end_validity__gte=anio_actual
    )

    parametros_dict = {
        p.parameter.name: p.value for p in parametros_vigentes
    }

    empleados = Employee.objects.select_related("position").all()

    with transaction.atomic():
        for empleado in empleados:
            total_hours, days_worked, faults,total_horas_extra, dias_restantes = calculate_employee_data(month, year, empleado)
            base_salary = empleado.position.base_salary

            payroll_employee = PayrollEmployee.objects.create(
                payroll=payroll,
                employee=empleado,
                days_worked=days_worked,
                total_hours=total_hours,
                faults=faults,
                overtime= total_horas_extra
            )

            conceptos_dict = {}
            total_rem = total_desc = total_serv= 0

            for concepto in conceptos_vigentes:
                nombre_upper = concepto.name.upper()
                sueldo_dia = base_salary / (days_worked + faults)

                if nombre_upper == "SUELDO BASICO":
                    monto = base_salary
                elif nombre_upper == "HORAS EXTRAS":
                    monto = (sueldo_dia/8)*payroll_employee.overtime
                elif  nombre_upper == "FALTAS/TARDANZAS":
                    monto = sueldo_dia * faults
                elif concepto.is_calculate and concepto.formula:
                    
                    if nombre_upper == "GRATIFICACION" and  (month != 7 or month !=12):
                        monto = 0
                    elif nombre_upper == "CTS" and  (month != 5 or month !=11):
                        monto = 0
                    
                    elif nombre_upper == "ASIGNACIÓN FAMILIAR" and payroll_employee.employee.has_children==False:
                        monto = 0
                    else:
                        variables = obtener_variables_para_empleado(
                            empleado, payroll_employee, conceptos_dict, parametros_dict
                        )
                        monto = evaluar_formula(concepto.formula, variables)
                else:
                    monto = 0

                PayrrollEmployeeDetail.objects.create(
                    payroll_employee=payroll_employee,
                    concept=concepto,
                    calculated_amount=monto
                )

                conceptos_dict[nombre_upper] = monto

                monto = to_decimal(monto)

                if concepto.type == 'base':
                    total_rem += monto
                elif concepto.type == 'descuento':
                    total_desc += monto
                elif concepto.type == 'auxiliar':
                    total_serv += monto

            payroll_employee.total_remuneration = total_rem
            payroll_employee.total_discounts = total_desc
            payroll_employee.total_amount_services = total_serv
            payroll_employee.net_total = total_rem - total_desc
            payroll_employee.save()

        payroll.total_amount = sum(p.net_total for p in payroll.Nomina.all())
        payroll.total_amount_services = sum(p.total_amount_services for p in payroll.Nomina.all())
        payroll.state = "En revisión"
        payroll.save()
