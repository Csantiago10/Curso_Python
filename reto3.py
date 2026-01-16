print("Tabla de multiplicar del 1 al 10")

tabla_multiplicar = int(input(f"Ingrese el número de la tabla de multiplicar: "))

print(f"Tabla de multiplicar del {tabla_multiplicar}\n")
for i in range(1, 11):
    print(f"{tabla_multiplicar} x {i} = {tabla_multiplicar * i}")
    