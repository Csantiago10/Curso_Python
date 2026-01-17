def registro_alumnos(num_estudiantes):
    for i in range(num_estudiantes):
        estudiante = input(f"\nIngrese el nombre de estudiante: ")
    
        notas = []

        print(f"Ingrese las 3 notas de {estudiante}:")
        for  j in range(3):
            nota = input(f"Ingrese la nota {j+1}:")
            notas.append(float(nota))
        
        nuevo_alumno = {
            "nombre": estudiante,
            "notas": notas
        }

        registro_colegio.append(nuevo_alumno)

def imprimir_registro(registro_colegio):
    for alumno in registro_colegio:

        nombre = alumno["nombre"]
        notas = alumno["notas"]

        promedio = sum(notas) / len(notas)

        estado = 'Aprobado' if promedio >= 3.0 else 'Reprobado'

        print(f"\n{nombre:<15} | {str(notas):<20} | {promedio:.1f} | {estado:<} | ")


registro_colegio = []

cantidad_estudiantes = int(input("Ingrese la cantidad de estudiantes a registrar: "))

registro_alumnos(cantidad_estudiantes)


print("\n--- BOLETIN DE NOTAS ---")
print(f"\n{'Nombre':<15} | {'Notas':<20} | {'Promedio':<5} | {'Estado':<10} |")
print("-" * 60)

imprimir_registro(registro_colegio)