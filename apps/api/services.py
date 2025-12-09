from django.db import connection

def get_dashboard_asistencia(year, month):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM resumen_dashboard_asistencia(%s, %s);", [year, month])
        result = cursor.fetchone()

    return {
        "total_empleados": result[0],
        "total_asistencias": result[1],
        "total_ausencias": result[2],
        "total_tardanzas": result[3],
        "total_horas_extra": float(result[4]),
    }



def get_dashboard_ultimosmeses(year, month):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM resumen_asistencia_ultimos_4_meses(%s, %s);", [year, month])
            rows = cursor.fetchall()

        data = [
            {
                "name": row[0].capitalize(),  
                "Asistencias": row[1],
                "Ausencias": row[2]
            }
            for row in rows
        ]
        return data

def get_dashboard_ultimosmesespuntualidad(year, month):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM resumen_puntualidad_ultimos_4_meses(%s, %s);", [year, month])
            rows = cursor.fetchall()

        data = [
            {
                "name": row[0].capitalize(),  
                "A_tiempo": row[1],
                "Tardanzas": row[2]
            }
            for row in rows
        ]
        return data

def get_dashboard_mesasistenciaarea(year, month):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM resumen_radar_asistencia_por_area(%s, %s);", [year, month])
            rows = cursor.fetchall()

        data = [
            {
                "Area": row[0],  
                "Asistencia": row[1],
            }
            for row in rows
        ]
        return data

def get_dashboard_mestype_marking(year, month):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM resumen_marcaciones_por_tipo(%s, %s);", [year, month])
            result = cursor.fetchone()
        
        return {
            "Ingreso": result[0],
            "Salida": result[1],
            "Horas_Extra": result[2],
        }

def get_dashboard_nomina(year, month):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM resumen_nominas_ultimos_4_meses(%s, %s);", [year, month])
            rows = cursor.fetchall()

        data = [
            {
                "name": row[0].capitalize(),  
                "Aportes": row[1],
                "Sueldos": row[2]
            }
            for row in rows
        ]
        return data

