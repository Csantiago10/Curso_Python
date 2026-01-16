print("Este programa determina si un número es positivo, negativo o cero, y si es par.")

numero =  int(input("Ingrese un número entero: "))

if numero == 0:
    print("El número es cero")

else:

    if numero > 0:
        print(f"El número {numero} es positivo")
    else:
        print(f"El número {numero} es negativo")

    if numero % 2 == 0:
        print(f"El número {numero} es par")
    else:
        print(f"El número {numero} es impar")
