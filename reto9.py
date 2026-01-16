class Alumno: #Definición de la clase Alumno
    def __init__(self, nombre, nota): #Constructor de la clase
        self.nombre = nombre #Atrubuto nombre
        self.nota = nota #Atributo nota

    def verificar_estado(self): #Método para verificar si el alumno está aprobado o reprobado
        if self.nota >= 60:
            return f"{self.nombre} está aprobado"
        else:
            return f"{self.nombre} está reprobado"
        

alumno1= Alumno("Pedro", 50) #Creación de instancia de la clase Alumno
alumno2= Alumno("Ana", 95) #Creación de instancia de la clase Alumno

print(alumno1.verificar_estado()) #Llamada al método verificar_estado para el primer alumno
print(alumno2.verificar_estado()) #Llamada al método verificar_estado para el segundo alumno
    