alumnos = [
    {"nombre": "Carlos", "calificacion": 55},
    {"nombre": "Sofia", "calificacion": 92},
    {"nombre": "Miguel", "calificacion": 78}
]

def verificar_aprobacion(nota):
    
    if nota >= 60:
        return "Aprobado"
    else:
        return "Reprobado"
    
    
for alumno in alumnos:
    calificacion = alumno["calificacion"]

    estado = verificar_aprobacion(calificacion)

    alumno["estado"] = estado
        



print(alumnos)