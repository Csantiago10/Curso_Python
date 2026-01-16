# Códigos de colores ANSI
VERDE = '\033[92m'
ROJO = '\033[91m'
RESET = '\033[0m'  # Este es importante para quitar el color

class Alumno: #Definición de la clase Alumno
    def __init__(self, nombre, nota): #Constructor de la clase
        self.nombre = nombre #Atrubuto nombre
        self.nota = nota #Atributo nota

    def verificar_estado(self): #Método para verificar si el alumno está aprobado o reprobado
        if self.nota >= 60:
            return f"{self.nombre} | {self.nota} | {VERDE}Aprobado{RESET}"
        else:
            return f"{self.nombre} | {self.nota} | {ROJO}Reprobado{RESET}"
        

salon = []

while True:
    # 1. Mostrar el menú
    print("\n" + "="*30)
    print("      MENÚ PRINCIPAL")
    print("="*30)
    print("1. Registrar nuevo estudiante")
    print("2. Salir")
    print("="*30)

    # 2. Captura de la opción
    opcion = input(">>> Selecciona una opción (1-2): ")

    # 3. Lógica de decisiones
    if opcion == "1":
        nombre = input("Ingrese el nombre del estudiante: ")
        
        while True:
            try:
                nota = int(input("Ingrese la nota del estudiante (0-100): "))
                if 0 <= nota <= 100:
                    break
                else:
                    print("Por favor, ingrese una nota válida entre 0 y 100.")
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número entero.")

                continue

        nuevo_alumno = Alumno(nombre, nota)
        salon.append(nuevo_alumno)
        print(f"Estudiante {nombre} con nota {nota} registrado exitosamente.")
        

    
    elif opcion == "2":
        print("Saliendo del sistema. ¡Hasta luego!")
        break

    else:
        print("Opción inválida. Por favor, seleccione una opción del menú.")

print("\n" + "="*30)
print(f"{'NOMBRE':<15} | {'NOTA':<5} | ESTADO") # Formateo de columnas
print("-" * 30)

for estudiante in salon:
    # Mostrar el estado de todos los estudiantes registrados
    print(estudiante.verificar_estado())