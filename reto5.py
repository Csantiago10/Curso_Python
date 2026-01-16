nota = 75

def verificar_aprobacion(nota):
    if nota >= 60:
        return "Aprobado"
    else:
        return "Reprobado"
    
estado = verificar_aprobacion(nota)

print(f"El estudiante está: {estado}")