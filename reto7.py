import random

alumnos = [
    {"nombre": "Carlos"},
    {"nombre": "Sofia"},
    {"nombre": "Miguel"}
]

def verificar_aprobacion(nota):
    
    if nota >= 60:
        return "Aprobado"
    else:
        return "Reprobado"
    
for alumno in alumnos:
    calificacion = random.randint(0, 100)
    alumno["calificacion"] = calificacion
    estado = verificar_aprobacion(calificacion)
    alumno["estado"] = estado

print(alumnos)    
