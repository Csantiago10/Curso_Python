def tabla_multiplicacion(numero):
    for i in range(1, 11):
        resultado = numero * i
        print(f"{numero} x {i} = {resultado}")




numero = int(input("Ingrese el número de la tabla de multiplicar: "))
print("\n" + "="*30)
print(f"Tabla de multiplicar del {numero}")
print("="*30)


tabla_multiplicacion(numero)
