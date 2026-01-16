tareas = ["Aprender Python", "Subir a GitHub", "Dominar el mundo"]

with open("pendientes.txt", "w") as archivo:
    for tarea in tareas:
        archivo.write(tarea + "\n")


with open("pendientes.txt", "r") as archivo:
    for i, tarea in enumerate(archivo, 1):
        print(str(i) + ". " + tarea.strip())  
        i += 1